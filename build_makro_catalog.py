# build_makro_catalog.py
import zipfile, xml.etree.ElementTree as ET, os, sys, json, io, base64
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

excel_file = 'สั่งของสหกรณ์-2_VBA.xlsm'
print(f'Reading {excel_file}...')
zf = zipfile.ZipFile(excel_file, 'r')
ns_main = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
ns_rd = '{http://schemas.microsoft.com/office/spreadsheetml/2017/richdata}'

ss_xml = zf.read('xl/sharedStrings.xml')
ss_root = ET.fromstring(ss_xml)
shared_strings = []
for si in ss_root.findall(f'{ns_main}si'):
    t = si.find(f'{ns_main}t')
    if t is not None and t.text:
        shared_strings.append(t.text)
    else:
        parts = [elem.text for elem in si.findall(f'.//{ns_main}t') if elem.text]
        shared_strings.append(''.join(parts))

rv_rels_xml = zf.read('xl/richData/_rels/richValueRel.xml.rels')
rv_rels = ET.fromstring(rv_rels_xml)
rid_to_target = {r.attrib['Id']: r.attrib['Target'].replace('../', 'xl/') for r in rv_rels}

rv_rel_xml = zf.read('xl/richData/richValueRel.xml')
rv_rel_root = ET.fromstring(rv_rel_xml)
rel_idx_to_target = []
for rel in rv_rel_root:
    rid = rel.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
    rel_idx_to_target.append(rid_to_target.get(rid))

rv_xml = zf.read('xl/richData/rdrichvalue.xml')
rv_root = ET.fromstring(rv_xml)
rv_idx_to_target = []
for rv in rv_root:
    vals = [v.text for v in rv]
    if vals and vals[0].isdigit():
        rel_i = int(vals[0])
        rv_idx_to_target.append(rel_idx_to_target[rel_i] if rel_i < len(rel_idx_to_target) else None)
    else:
        rv_idx_to_target.append(None)

meta_xml = zf.read('xl/metadata.xml')
meta_root = ET.fromstring(meta_xml)
future_meta = meta_root.find(f'{ns_main}futureMetadata')
fm_to_rv = []
if future_meta is not None:
    for bk in future_meta:
        rvb = bk.find(f'.//{ns_rd}rvb')
        fm_to_rv.append(int(rvb.attrib.get('i', 0)) if rvb is not None else None)

val_meta = meta_root.find(f'{ns_main}valueMetadata')
vm_to_img = []
if val_meta is not None:
    for bk in val_meta:
        rc = bk.find(f'{ns_main}rc')
        if rc is not None:
            v_idx = int(rc.attrib.get('v', 0))
            rv_i = fm_to_rv[v_idx] if v_idx < len(fm_to_rv) else None
            img_path = rv_idx_to_target[rv_i] if (rv_i is not None and rv_i < len(rv_idx_to_target)) else None
            vm_to_img.append(img_path)

wb_xml = zf.read('xl/workbook.xml')
wb_root = ET.fromstring(wb_xml)
sheet_map = {s.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'): s.attrib.get('name') for s in wb_root.findall(f'.//{ns_main}sheet')}
rels_xml = zf.read('xl/_rels/workbook.xml.rels')
rels_root = ET.fromstring(rels_xml)
rel_map = {r.attrib.get('Id'): r.attrib.get('Target') for r in rels_root.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')}

target_sheets = [
    ('ขนม', 'ขนม'),
    ('เครื่องดื่ม', 'เครื่องดื่ม'),
    ('เครื่องปรุง-ทั่วไป', 'เครื่องปรุง-ทั่วไป')
]

img_dir = 'makro_images'
os.makedirs(img_dir, exist_ok=True)

products = []
item_id = 1
total_img_bytes = 0

for s_code, s_name in target_sheets:
    r_id = [k for k, v in sheet_map.items() if v == s_code][0]
    target = rel_map.get(r_id)
    ws_path = 'xl/' + target if not target.startswith('xl/') else target
    ws_root = ET.fromstring(zf.read(ws_path))
    rows = ws_root.findall(f'.//{ns_main}row')
    sheet_count = 0
    for r in rows:
        r_idx = int(r.attrib.get('r', 0))
        if r_idx < 7: continue
        c_dict = {}
        c_vm = None
        for c in r.findall(f'.//{ns_main}c'):
            col = ''.join([ch for ch in c.attrib.get('r', '') if ch.isalpha()])
            v = c.find(f'{ns_main}v')
            val = v.text if v is not None else ''
            if c.attrib.get('t') == 's' and val.isdigit():
                val = shared_strings[int(val)]
            c_dict[col] = val
            if col == 'C':
                c_vm = c.attrib.get('vm')
        
        name = c_dict.get('D', '').strip()
        if not name: continue
        
        code = c_dict.get('B', '').strip()
        unit = c_dict.get('F', '').strip() or 'Pack'
        barcode = c_dict.get('G', '').strip()
        
        def parse_float(val):
            try:
                return round(float(str(val).replace(',', '').strip()), 2)
            except:
                return 0.0
        
        cost = parse_float(c_dict.get('H', 0))
        unit_cost = parse_float(c_dict.get('I', 0))
        price = parse_float(c_dict.get('J', 0))
        
        safe_code = ''.join(c for c in code if c.isalnum() or c in ('-', '_')) or 'no_code'
        img_filename = f'{item_id:03d}_{safe_code}.webp'
        img_rel_path = f'makro_images/{img_filename}'
        b64_data_uri = ''
        
        if c_vm and c_vm.isdigit():
            vm_int = int(c_vm)
            if 1 <= vm_int <= len(vm_to_img) and vm_to_img[vm_int - 1]:
                raw_img = zf.read(vm_to_img[vm_int - 1])
                try:
                    im = Image.open(io.BytesIO(raw_img))
                    im = im.convert('RGB')
                    im.thumbnail((200, 200), Image.Resampling.LANCZOS)
                    im.save(img_rel_path, format='WEBP', quality=78)
                    total_img_bytes += os.path.getsize(img_rel_path)
                    
                    buf = io.BytesIO()
                    im.save(buf, format='WEBP', quality=75)
                    b64_str = base64.b64encode(buf.getvalue()).decode('ascii')
                    b64_data_uri = f'data:image/webp;base64,{b64_str}'
                except Exception as ex:
                    print(f'Warning image {item_id}: {ex}')
        
        products.append({
            'id': item_id,
            'code': code,
            'barcode': barcode,
            'name': name,
            'category': s_name,
            'unit': unit,
            'cost': cost,
            'unitCost': unit_cost,
            'price': price,
            'image': img_rel_path,
            'imageThumb': b64_data_uri
        })
        item_id += 1
        sheet_count += 1
    print(f'Category {s_name}: {sheet_count} items')

with open('makro_products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f'Done! Total products: {len(products)}, Total images size: {total_img_bytes/1024/1024:.2f} MB')
