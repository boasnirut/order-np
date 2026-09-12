import openpyxl, sys, json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
wb = openpyxl.load_workbook('ไฟล์จดรับ-จ่าย-สหกรณ์.xlsx', data_only=True)

transactions = []
id_counter = 1001

sheet_config = {
    'พ.ย.': {'ym': '2026-05', 'start': 7, 'end': 63},
    'มิ.ย.': {'ym': '2026-06', 'start': 7, 'end': 48},
    'ก.ค.': {'ym': '2026-07', 'start': 7, 'end': 13}
}

for sheetname, cfg in sheet_config.items():
    if sheetname not in wb.sheetnames:
        continue
    ws = wb[sheetname]
    default_ym = cfg['ym']
    
    current_date = f'{default_ym}-01'
    for r in range(cfg['start'], cfg['end'] + 1):
        c0 = ws.cell(row=r, column=1).value
        if isinstance(c0, datetime):
            d = c0.day
            current_date = f'{default_ym}-{d:02d}'
        elif c0 is not None and str(c0).strip() != '':
            current_date = str(c0).strip()

        item = ws.cell(row=r, column=2).value
        income_shop = ws.cell(row=r, column=3).value
        exp_mall = ws.cell(row=r, column=6).value
        exp_market = ws.cell(row=r, column=7).value
        exp_wages = ws.cell(row=r, column=8).value
        exp_utilities = ws.cell(row=r, column=9).value
        exp_other = ws.cell(row=r, column=10).value
        doc = ws.cell(row=r, column=14).value

        has_inc = income_shop is not None and float(income_shop) > 0
        has_mall = exp_mall is not None and float(exp_mall) > 0
        has_mkt = exp_market is not None and float(exp_market) > 0
        has_wages = exp_wages is not None and float(exp_wages) > 0
        has_util = exp_utilities is not None and float(exp_utilities) > 0
        has_oth = exp_other is not None and float(exp_other) > 0

        if not (has_inc or has_mall or has_mkt or has_wages or has_util or has_oth):
            continue

        t_date = current_date
        if not t_date or not t_date.startswith(default_ym):
            t_date = f'{default_ym}-01'

        if has_inc:
            transactions.append({
                'id': id_counter,
                'date': t_date,
                'type': 'income',
                'category': 'income_shop',
                'categoryName': 'รายรับขายสินค้าหน้าร้าน',
                'item': str(item).strip() if item else 'ขายของได้ในโปรแกรม',
                'amount': float(income_shop),
                'doc': str(doc).strip() if doc else ''
            })
            id_counter += 1

        if has_mall:
            transactions.append({
                'id': id_counter,
                'date': t_date,
                'type': 'expense',
                'category': 'exp_mall',
                'categoryName': 'ซื้อจากห้าง (Makro/Lotus/Big C)',
                'item': str(item).strip() if item else 'ซื้อของเข้าร้าน',
                'amount': float(exp_mall),
                'doc': str(doc).strip() if doc else ''
            })
            id_counter += 1

        if has_mkt:
            transactions.append({
                'id': id_counter,
                'date': t_date,
                'type': 'expense',
                'category': 'exp_market',
                'categoryName': 'ซื้อจากตลาด/ร้านค้าส่ง',
                'item': str(item).strip() if item else 'ซื้อของเข้าร้าน',
                'amount': float(exp_market),
                'doc': str(doc).strip() if doc else ''
            })
            id_counter += 1

        if has_wages:
            transactions.append({
                'id': id_counter,
                'date': t_date,
                'type': 'expense',
                'category': 'exp_wages',
                'categoryName': 'ค่าแรง',
                'item': str(item).strip() if item else 'ค่าแรง',
                'amount': float(exp_wages),
                'doc': str(doc).strip() if doc else ''
            })
            id_counter += 1

        if has_util:
            transactions.append({
                'id': id_counter,
                'date': t_date,
                'type': 'expense',
                'category': 'exp_utilities',
                'categoryName': 'สาธารณูปโภค',
                'item': str(item).strip() if item else 'สาธารณูปโภค',
                'amount': float(exp_utilities),
                'doc': str(doc).strip() if doc else ''
            })
            id_counter += 1

        if has_oth:
            transactions.append({
                'id': id_counter,
                'date': t_date,
                'type': 'expense',
                'category': 'exp_other',
                'categoryName': 'ค่าใช้จ่ายอื่นๆ',
                'item': str(item).strip() if item else 'ค่าใช้จ่ายอื่นๆ',
                'amount': float(exp_other),
                'doc': str(doc).strip() if doc else ''
            })
            id_counter += 1

with open('initial_data.json', 'w', encoding='utf-8') as f:
    json.dump(transactions, f, ensure_ascii=False, indent=2)

print('Updated initial_data.json with exact rows:', len(transactions), 'transactions.')

# Verify sheet by sheet totals
for sheetname, ym in [('พ.ย.', '2026-05'), ('มิ.ย.', '2026-06'), ('ก.ค.', '2026-07')]:
    s_txs = [t for t in transactions if t['date'].startswith(ym)]
    inc = sum(t['amount'] for t in s_txs if t['type'] == 'income')
    cogs_mall = sum(t['amount'] for t in s_txs if t['category'] == 'exp_mall')
    cogs_mkt = sum(t['amount'] for t in s_txs if t['category'] == 'exp_market')
    cogs = cogs_mall + cogs_mkt
    profit = inc - cogs
    print(f'Sheet {sheetname} ({ym}): รายรับ = {inc:,.2f} | ต้นทุนขาย = {cogs:,.2f} (ห้าง: {cogs_mall:,.2f}, ตลาด: {cogs_mkt:,.2f}) | กำไร = {profit:,.2f}')
