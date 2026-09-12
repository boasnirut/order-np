import json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('makro_products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

products_json = json.dumps(products, ensure_ascii=False)

with open('template_makro.html', 'r', encoding='utf-8') as f:
    template = f.read()

final_html = template.replace('__MAKRO_PRODUCTS_JSON__', products_json)

out_root = 'สั่งของMakro.html'
with open(out_root, 'w', encoding='utf-8') as f:
    f.write(final_html)
print(f'Generated {out_root}: {os.path.getsize(out_root)/1024/1024:.2f} MB')

os.makedirs('Program', exist_ok=True)
out_prog = 'Program/สั่งของMakro.html'
with open(out_prog, 'w', encoding='utf-8') as f:
    f.write(final_html)
print(f'Generated {out_prog}: {os.path.getsize(out_prog)/1024/1024:.2f} MB')
