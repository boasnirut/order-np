import urllib.request
import urllib.parse
import json
import re
import time
import concurrent.futures
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

print("Starting Makro Pro Price Updater...")

with open('makro_products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products to check: {len(products)}")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'th,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

results = []
updated_count = 0
unchanged_count = 0
not_found_count = 0
price_changes = []

def fetch_product_price(product):
    code = (product.get('code') or '').strip()
    name = (product.get('name') or '').strip()
    query = code if code else name

    search_url = f'https://www.makro.pro/c/search?q={urllib.parse.quote(query)}'
    req = urllib.request.Request(search_url, headers=headers)
    
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                html = resp.read().decode('utf-8')
                next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
                if not next_data:
                    return {'id': product['id'], 'status': 'no_next_data'}
                
                data = json.loads(next_data.group(1))
                hits = data.get('props', {}).get('pageProps', {}).get('initialSearchResult', {}).get('hits', [])
                
                matched_doc = None
                if code:
                    for h in hits:
                        doc = h.get('document', {})
                        if str(doc.get('makroId', '')).strip() == code:
                            matched_doc = doc
                            break
                
                if not matched_doc and hits:
                    # fallback to first hit if query was name or exact match
                    matched_doc = hits[0].get('document', {})

                if matched_doc:
                    display_price = matched_doc.get('displayPrice')
                    original_price = matched_doc.get('originalPrice')
                    in_stock = matched_doc.get('inStock', True)
                    unit_factor = matched_doc.get('unitFactor')
                    makro_title = matched_doc.get('title')
                    
                    return {
                        'id': product['id'],
                        'status': 'success',
                        'displayPrice': float(display_price) if display_price is not None else None,
                        'originalPrice': float(original_price) if original_price is not None else None,
                        'inStock': in_stock,
                        'unitFactor': unit_factor,
                        'makroTitle': makro_title
                    }
                else:
                    return {'id': product['id'], 'status': 'not_found'}
        except Exception as e:
            if attempt == 1:
                return {'id': product['id'], 'status': 'error', 'error': str(e)}
            time.sleep(0.5)

# Run with ThreadPoolExecutor (4 concurrent workers)
max_workers = 4
completed = 0
total = len(products)

print(f"Checking prices using {max_workers} parallel workers...")

with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    future_to_prod = {executor.submit(fetch_product_price, p): p for p in products}
    for future in concurrent.futures.as_completed(future_to_prod):
        p = future_to_prod[future]
        res = future.result()
        completed += 1
        
        if completed % 25 == 0 or completed == total:
            print(f"Progress: {completed}/{total} items processed ({completed/total*100:.1f}%)")

        if res['status'] == 'success' and res['displayPrice'] is not None:
            new_cost = res['displayPrice']
            old_cost = p['cost']
            diff = round(new_cost - old_cost, 2)
            
            p['cost'] = new_cost
            if res.get('unitFactor') and res['unitFactor'] > 0:
                p['unitCost'] = round(new_cost / res['unitFactor'], 2)
            elif p.get('unitCost') and old_cost > 0:
                # scale unitCost proportionally
                ratio = new_cost / old_cost
                p['unitCost'] = round(p['unitCost'] * ratio, 2)
            
            p['inStock'] = res['inStock']
            
            if diff != 0:
                updated_count += 1
                price_changes.append({
                    'id': p['id'],
                    'code': p.get('code'),
                    'name': p['name'],
                    'category': p['category'],
                    'oldCost': old_cost,
                    'newCost': new_cost,
                    'diff': diff,
                    'inStock': res['inStock']
                })
            else:
                unchanged_count += 1
        else:
            not_found_count += 1

print("=" * 60)
print(f"Price Update Finished!")
print(f"Total checked: {total}")
print(f"Price updated (changed): {updated_count} items")
print(f"Price unchanged (same): {unchanged_count} items")
print(f"Not found or error: {not_found_count} items")
print("=" * 60)

# Save updated products to JSON
with open('makro_products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)
print("Saved updated makro_products.json")

# Save Price Changes Report
with open('price_update_report.json', 'w', encoding='utf-8') as f:
    json.dump({
        'updatedAt': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total': total,
        'changed': len(price_changes),
        'unchanged': unchanged_count,
        'notFound': not_found_count,
        'changes': price_changes
    }, f, ensure_ascii=False, indent=2)
print("Saved price_update_report.json")

# Re-generate the HTML apps
print("Recompiling HTML applications...")
os.system('python generate_app.py')
print("All applications updated with latest Makro Pro prices!")
