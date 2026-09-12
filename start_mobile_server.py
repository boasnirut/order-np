import socket
import http.server
import socketserver
import qrcode
import os
import sys
import urllib.request
import urllib.parse
import json
import re
import datetime

sys.stdout.reconfigure(encoding='utf-8')

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

local_ip = get_local_ip()
PORT = 8080
url = f"http://{local_ip}:{PORT}/สั่งของMakro.html"

# Generate QR code image
qr = qrcode.QRCode(box_size=8, border=2)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("mobile_qr.png")

print("=" * 65)
print("   🚀 เซิร์ฟเวอร์เปิดใช้งานระบบ Order NP สำหรับโทรศัพท์มือถือ")
print("=" * 65)
print(f"📱 วิธีเข้าใช้งานผ่านมือถือ (ต่อ Wi-Fi วงเดียวกับคอมพิวเตอร์):")
print(f"1. เปิดกล้องมือถือ หรือเปิดแอป LINE แล้วสแกนภาพ QR Code ที่ไฟล์ 'mobile_qr.png'")
print(f"2. หรือเปิดเบราว์เซอร์บนมือถือ (Chrome/Safari) แล้วพิมพ์ลิงก์นี้:")
print(f"   👉 {url}")
print("-" * 65)

try:
    qr_term = qrcode.QRCode(border=1)
    qr_term.add_data(url)
    qr_term.make(fit=True)
    qr_term.print_ascii(invert=True)
except Exception:
    pass

print("-" * 65)
print(f"กำลังเปิดบริการที่พอร์ต {PORT} ... (กด Ctrl+C เพื่อหยุดการทำงาน)")

def search_makro_api(q):
    q = q.strip().strip('"\'“”‘’[]()•-*#')
    url_match = re.search(r'makro\.pro/(?:[a-z]{2}/)?p/([0-9]+)', q, re.IGNORECASE)
    if url_match:
        q = url_match.group(1)
    else:
        url_search = re.search(r'makro\.pro/(?:[a-z]{2}/)?c/search\?.*?[?&]q=([^&]+)', q, re.IGNORECASE)
        if url_search:
            try:
                q = urllib.parse.unquote(url_search.group(1)).strip()
            except Exception:
                q = url_search.group(1).strip()
    
    def do_fetch(search_term):
        searchUrl = f"https://www.makro.pro/c/search?q={urllib.parse.quote(search_term)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'th,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        req = urllib.request.Request(searchUrl, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8')
        match = re.search(r'<script id="__NEXT_DATA__" type="application/json">([\s\S]*?)</script>', html)
        if not match:
            return []
        data = json.loads(match.group(1))
        return data.get('props', {}).get('pageProps', {}).get('initialSearchResult', {}).get('hits', [])

    try:
        hits = do_fetch(q)
        if not hits and ' ' in q:
            words = [w for w in q.split() if w]
            if len(words) > 2:
                hits = do_fetch(' '.join(words[:2]))
        
        results = []
        for h in hits:
            doc = h.get('document', {})
            cats = ' '.join(doc.get('categories', [])).lower()
            title = doc.get('title') or doc.get('productName') or ''
            
            category = 'เครื่องปรุง-ทั่วไป'
            if any(w in cats for w in ['snack', 'biscuit', 'candy', 'chocolate', 'chip']) or any(w in title for w in ['ขนม', 'ช็อก', 'เวเฟอร์', 'มันฝรั่ง', 'คุกกี้', 'ลูกอม']):
                category = 'ขนม'
            elif any(w in cats for w in ['beverage', 'drink', 'coffee', 'tea', 'water', 'milk', 'juice']) or any(w in title for w in ['น้ำ', 'นม', 'กาแฟ', 'ชา', 'โซดา', 'โออิชิ', 'โค้ก', 'เป๊ปซี่']):
                category = 'เครื่องดื่ม'
            
            raw_price = doc.get('displayPrice') if doc.get('displayPrice') is not None else doc.get('originalPrice', 0)
            try:
                price = float(raw_price)
            except Exception:
                price = 0.0
            
            images = doc.get('images', [])
            img_url = images[0] if images else (doc.get('image') or '')
            
            results.append({
                'code': str(doc.get('makroId') or '').strip(),
                'name': title.strip(),
                'price': price,
                'barcode': str(doc.get('itemBarCode') or '').strip(),
                'image': img_url,
                'category': category,
                'brand': doc.get('brand') or '',
                'unit': doc.get('unitType') or 'Pack'
            })
        
        # Smart ranking
        q_lower = q.lower()
        def rank_key(item):
            code = item['code'].lower()
            name = item['name'].lower()
            if code == q_lower:
                return (0, name)
            if name.startswith(q_lower):
                return (1, name)
            if q_lower in name:
                return (2, name)
            return (3, name)
        results.sort(key=rank_key)

        return {'success': True, 'query': q, 'count': len(results), 'hits': results}
    except Exception as e:
        return {'success': False, 'error': str(e)}

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ['/api/makro-search', '/.netlify/functions/makro-search']:
            qs = urllib.parse.parse_qs(parsed.query)
            q = qs.get('q', [''])[0].strip()
            data = search_makro_api(q)
            resp_body = json.dumps(data, ensure_ascii=False).encode('utf-8')
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(resp_body)))
            self.end_headers()
            self.wfile.write(resp_body)
            return

        if parsed.path == '/api/get-data':
            res_data = {'logs': [], 'catalog': []}
            if os.path.exists('activity_logs.json'):
                try:
                    with open('activity_logs.json', 'r', encoding='utf-8') as f:
                        res_data['logs'] = json.load(f)
                except Exception:
                    pass
            resp_body = json.dumps({'success': True, 'data': res_data}, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(resp_body)))
            self.end_headers()
            self.wfile.write(resp_body)
            return

        super().do_GET()

    def do_POST(self):
        if self.path == '/api/record-action':
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)
            try:
                payload = json.loads(post_body.decode('utf-8'))
            except Exception:
                payload = {}

            action_type = payload.get('action', 'general')
            title = payload.get('title', 'การกระทำ')
            details = payload.get('details', '')
            user = payload.get('user', 'ครูนฤทธิ์')
            data = payload.get('data', {})
            products = payload.get('products')

            log_entry = {
                'id': f'act-{int(datetime.datetime.now().timestamp()*1000)}',
                'timestamp': datetime.datetime.now().isoformat(),
                'type': action_type,
                'title': title,
                'details': details,
                'user': user,
                'data': data
            }

            # Update activity_logs.json
            current_logs = []
            if os.path.exists('activity_logs.json'):
                try:
                    with open('activity_logs.json', 'r', encoding='utf-8') as f:
                        current_logs = json.load(f)
                except Exception:
                    pass
            current_logs.insert(0, log_entry)
            current_logs = current_logs[:500]
            with open('activity_logs.json', 'w', encoding='utf-8') as f:
                json.dump(current_logs, f, ensure_ascii=False, indent=2)

            # Update makro_products.json if provided
            if isinstance(products, list) and len(products) > 0:
                with open('makro_products.json', 'w', encoding='utf-8') as f:
                    json.dump(products, f, ensure_ascii=False, indent=2)

            resp_body = json.dumps({'success': True, 'syncedToGitHub': False, 'message': 'บันทึกลงในเครื่องเรียบร้อยแล้ว', 'logEntry': log_entry}, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(resp_body)))
            self.end_headers()
            self.wfile.write(resp_body)
            return

        self.send_response(404)
        self.end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nหยุดการทำงานเซิร์ฟเวอร์เรียบร้อยแล้ว")
