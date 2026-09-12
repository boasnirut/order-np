import json

with open('price_update_report.json', 'r', encoding='utf-8') as f:
    report = json.load(f)

print('Total:', report['total'])
print('Changed:', report['changed'])
print('Unchanged:', report['unchanged'])
print('Not Found:', report['notFound'])

decreases = [c for c in report['changes'] if c['diff'] < 0]
increases = [c for c in report['changes'] if c['diff'] > 0]
print(f'Price decreases (ราคาถูกลง): {len(decreases)} รายการ')
print(f'Price increases (ราคาปรับขึ้น): {len(increases)} รายการ')

print('\nTop 5 รายการที่ราคาลดลงมากที่สุด:')
for c in sorted(decreases, key=lambda x: x['diff'])[:5]:
    print(f" - {c['name']} (#{c['code']}): {c['oldCost']} -> {c['newCost']} (ลดลง {abs(c['diff']):.2f} บาท)")

print('\nTop 5 รายการที่ราคาปรับขึ้น:')
for c in sorted(increases, key=lambda x: -x['diff'])[:5]:
    print(f" - {c['name']} (#{c['code']}): {c['oldCost']} -> {c['newCost']} (เพิ่มขึ้น {c['diff']:.2f} บาท)")
