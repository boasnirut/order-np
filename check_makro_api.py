import urllib.request
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request('https://www.makro.pro/', headers=headers)
html = urllib.request.urlopen(req).read().decode('utf-8')

scripts = re.findall(r'src="(/_next/static/[^"]+)"', html)
print(f'Total scripts found: {len(scripts)}')

# Look for API endpoints, graphql, or search paths
endpoints = set()
for s in scripts:
    if 'chunks' in s:
        script_url = 'https://www.makro.pro' + s
        try:
            s_req = urllib.request.Request(script_url, headers=headers)
            s_code = urllib.request.urlopen(s_req, timeout=5).read().decode('utf-8')
            found = re.findall(r'https://[a-zA-Z0-9\.\-_/]+(?:api|graphql|search)[a-zA-Z0-9\.\-_/]*', s_code)
            for f in found:
                endpoints.add(f)
            # also look for relative paths like /api/... or search
            rel = re.findall(r'"(/(?:api|search|c|p)/[^"]+)"', s_code)
            for r in rel:
                endpoints.add(r)
        except Exception as e:
            pass

print(f'Found {len(endpoints)} endpoints:')
for ep in list(endpoints)[:30]:
    print('  ', ep)
