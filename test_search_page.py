import urllib.request
import json
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'th,en;q=0.9'
}

test_codes = ['819218', '840135', '147344']

for code in test_codes:
    url = f'https://www.makro.pro/c/search?q={code}'
    req = urllib.request.Request(url, headers=headers)
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
            next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
            if next_data:
                data = json.loads(next_data.group(1))
                res = data.get('props', {}).get('pageProps', {}).get('initialSearchResult', {})
                hits = res.get('hits', [])
                print(f'Code {code}: found {len(hits)} hits in {time.time()-t0:.2f}s')
                if hits:
                    doc = hits[0].get('document', {})
                    print(f"  Title: {doc.get('title')}")
                    print(f"  Makro ID: {doc.get('makroId')}")
                    print(f"  Price: {doc.get('displayPrice')} (original: {doc.get('originalPrice')})")
    except Exception as e:
        print(f'Code {code} error:', e)
