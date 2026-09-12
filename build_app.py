import json

try:
    with open('pos_sales_data.json', 'r', encoding='utf-8') as f:
        pos_data = json.load(f)
except Exception as e:
    pos_data = []

try:
    with open('may_june_entries.json', 'r', encoding='utf-8') as f:
        may_june_data = json.load(f)
except Exception as e:
    may_june_data = []

pos_json_str = json.dumps(pos_data, ensure_ascii=False, indent=2)
may_june_json_str = json.dumps(may_june_data, ensure_ascii=False, indent=2)

html_content = f'''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ระบบรายรับ-รายจ่าย และสรุปกำไรขาดทุน สหกรณ์โรงเรียนบ้านน้ำพร</title>
    <!-- Google Fonts: Prompt -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Prompt:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <!-- FontAwesome 6 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- SheetJS for reading XLSX Excel Files -->
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>

    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Prompt', 'sans-serif'],
                    }},
                    colors: {{
                        coop: {{
                            50: '#ecfdf5',
                            100: '#d1fae5',
                            500: '#10b981',
                            600: '#059669',
                            700: '#047857',
                            800: '#065f46',
                            900: '#064e3b',
                        }}
                    }}
                }}
            }}
        }}
    </script>

    <style>
        body {{ font-family: 'Prompt', sans-serif; background-color: #f8fafc; }}
        
        /* Custom scrollbar */
        .custom-scrollbar::-webkit-scrollbar {{ height: 6px; width: 6px; }}
        .custom-scrollbar::-webkit-scrollbar-track {{ background: #f1f5f9; border-radius: 8px; }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 8px; }}
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {{ background: #94a3b8; }}

        /* Sortable header styling */
        .sortable-header {{ cursor: pointer; user-select: none; transition: background-color 0.2s; }}
        .sortable-header:hover {{ background-color: #e2e8f0; }}

        /* A4 Strict Print Layout Styling */
        @page {{
            size: A4 portrait;
            margin: 10mm 12mm 10mm 12mm;
        }}

        @media print {{
            * {{
                box-sizing: border-box !important;
            }}

            /* Hide all screen layout elements */
            header, nav, main, footer, .no-print, #toast, #csv-file-input, #pos-excel-file-input, #edit-modal, #delete-modal, #pos-import-modal, #wallet-modal {{
                display: none !important;
            }}

            html, body {{
                width: 210mm !important;
                height: auto !important;
                background: white !important;
                color: #000 !important;
                font-size: 9pt !important;
                line-height: 1.3 !important;
                margin: 0 !important;
                padding: 0 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}

            /* Ensure print modal wrapper is visible and acts as normal page block */
            #print-modal {{
                display: block !important;
                position: static !important;
                inset: auto !important;
                width: 100% !important;
                height: auto !important;
                background: white !important;
                padding: 0 !important;
                margin: 0 !important;
                overflow: visible !important;
                box-shadow: none !important;
                backdrop-filter: none !important;
                z-index: auto !important;
            }}

            /* Inner modal container reset */
            #print-modal > div {{
                max-width: 100% !important;
                max-height: none !important;
                padding: 0 !important;
                margin: 0 !important;
                border: none !important;
                box-shadow: none !important;
                background: white !important;
                border-radius: 0 !important;
                overflow: visible !important;
            }}

            /* Show printable document area */
            #print-area {{
                display: block !important;
                width: 100% !important;
                max-width: 100% !important;
                border: none !important;
                padding: 0 !important;
                margin: 0 !important;
                box-shadow: none !important;
                background: white !important;
            }}

            .section-block {{
                margin-bottom: 14px !important;
            }}

            /* Continuous flow layout (No forced page breaks) */
            .print-ledger-section {{
                padding-top: 8px !important;
            }}

            /* Strict Table & Grid Lines Integrity for All Print Margins */
            table, .print-table {{
                width: 100% !important;
                border-collapse: collapse !important;
                border: 1.5px solid #0f172a !important;
                margin-bottom: 4px !important;
            }}

            /* Repeat table headers at top of each printed A4 page */
            thead {{
                display: table-header-group !important;
            }}

            tbody {{
                display: table-row-group !important;
            }}

            /* Prevent individual rows from splitting mid-row */
            tr {{
                page-break-inside: avoid !important;
                break-inside: avoid !important;
            }}

            th, td {{
                border: 1px solid #1e293b !important;
                padding: 4px 6px !important;
                font-size: 8.5pt !important;
                color: #0f172a !important;
            }}

            /* Prevent category and metadata cells from wrapping awkwardly */
            .nowrap-cell {{
                white-space: nowrap !important;
            }}

            th {{
                background-color: #f1f5f9 !important;
                color: #0f172a !important;
                font-weight: 700 !important;
            }}

            /* Signature block stays together at the very end with generous spacing before 'ลงชื่อ...' */
            .signature-block {{
                page-break-inside: avoid !important;
                break-inside: avoid !important;
                margin-top: 45px !important;
                padding-top: 20px !important;
            }}
        }}

        .print-only {{ display: none; }}
    </style>
</head>
<body class="text-slate-800 antialiased min-h-screen flex flex-col selection:bg-emerald-500 selection:text-white">

    <!-- Hidden CSV File Input -->
    <input type="file" id="csv-file-input" accept=".csv" onchange="handleCSVFileSelect(event)" class="hidden">
    <!-- Hidden POS Excel File Input -->
    <input type="file" id="pos-excel-file-input" accept=".xlsx, .xls" onchange="handlePosExcelSelect(event)" class="hidden">

    <!-- Navbar Header -->
    <header class="bg-emerald-700 text-white shadow-lg sticky top-0 z-40 border-b border-emerald-800 no-print">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-20">
                <div class="flex items-center gap-3 sm:gap-4">
                    <img src="https://ik.imagekit.io/boasnirut/32.png?updatedAt=1773125993394" 
                         onerror="this.src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png'"
                         alt="โลโก้โรงเรียนบ้านน้ำพร" 
                         class="w-12 h-12 rounded-full bg-white p-1 shadow-md object-cover ring-2 ring-emerald-300">
                    <div>
                        <h1 class="font-bold text-lg sm:text-xl md:text-2xl leading-tight tracking-wide">สหกรณ์โรงเรียนบ้านน้ำพร</h1>
                        <p class="text-emerald-200 text-xs sm:text-sm font-light">ระบบบันทึกรายรับ-รายจ่าย และสรุปกำไรขาดทุน</p>
                    </div>
                </div>
                <div class="flex items-center gap-2 sm:gap-3">
                    <!-- Import May & June Excel Data Button -->
                    <button onclick="importMayJuneExcelData()" class="bg-blue-600 hover:bg-blue-500 text-white px-3 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all shadow-md flex items-center gap-2 transform hover:scale-105 border border-blue-400/40">
                        <i class="fas fa-file-excel text-amber-300"></i>
                        <span class="hidden md:inline">นำเข้าข้อมูล พ.ค.-มิ.ย. (94 รายการ)</span>
                    </button>
                    <!-- Manage Accounts / Wallets Button -->
                    <button onclick="openWalletModal()" class="bg-emerald-800 hover:bg-emerald-900 text-white px-3 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all shadow-md flex items-center gap-2 border border-emerald-600/50 transform hover:scale-105">
                        <i class="fas fa-wallet text-amber-300"></i>
                        <span class="hidden xl:inline">บัญชี/กระเป๋าเงินสด</span>
                    </button>
                    <!-- Dedicated POS Excel Import Button -->
                    <button onclick="openPosImportModal()" class="bg-amber-500 hover:bg-amber-400 text-slate-900 px-3 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all shadow-md flex items-center gap-2 transform hover:scale-105 border border-amber-300">
                        <i class="fas fa-cash-register text-sm"></i>
                        <span class="hidden lg:inline">นำเข้ารายรับ POS หน้าร้าน</span>
                    </button>
                    <button onclick="openPrintModal()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-3 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shadow-md flex items-center gap-2 border border-emerald-400/40 transform hover:scale-105">
                        <i class="fas fa-print text-sm"></i>
                        <span class="hidden sm:inline">พิมพ์รายงาน A4</span>
                    </button>
                    <!-- Import CSV Button -->
                    <button onclick="triggerCSVImport()" class="bg-white/10 hover:bg-white/20 text-white px-3 py-2 rounded-xl text-xs sm:text-sm font-medium transition-all backdrop-blur-sm flex items-center gap-1.5 border border-white/20" title="นำเข้าไฟล์ CSV">
                        <i class="fas fa-file-import text-amber-300"></i>
                        <span class="hidden md:inline">นำเข้า CSV</span>
                    </button>
                    <!-- Export CSV Button -->
                    <button onclick="exportToCSV()" class="bg-white/10 hover:bg-white/20 text-white px-3 py-2 rounded-xl text-xs sm:text-sm font-medium transition-all backdrop-blur-sm flex items-center gap-1.5 border border-white/20" title="ส่งออกไฟล์ CSV">
                        <i class="fas fa-file-excel text-emerald-300"></i>
                        <span class="hidden md:inline">ส่งออก CSV</span>
                    </button>
                    <button onclick="resetToBlankDatabase()" title="ล้างรายการทั้งหมดเป็นฐานข้อมูลเปล่า" class="bg-emerald-900/60 hover:bg-emerald-900 text-emerald-200 px-3 py-2 rounded-xl text-xs font-medium transition-all flex items-center gap-1.5 border border-emerald-700">
                        <i class="fas fa-trash-can"></i>
                        <span class="hidden xl:inline">ล้างฐานข้อมูล</span>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Workspace -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-8 flex-grow w-full no-print">

        <!-- Section 1: Filter Bar & KPI Cards -->
        <section class="space-y-6">
            <!-- Date & Dynamic Preset Period Filter Bar -->
            <div class="bg-white p-4 sm:p-5 rounded-2xl shadow-sm border border-slate-200/80 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
                <div class="flex items-center gap-2 text-slate-700 font-bold text-base sm:text-lg">
                    <i class="fas fa-filter text-emerald-600"></i>
                    <span>ช่วงเวลาข้อมูล:</span>
                </div>
                
                <!-- Dynamic Month Preset Buttons Container -->
                <div id="month-preset-buttons-container" class="flex flex-wrap items-center gap-2 w-full lg:w-auto">
                    <!-- Rendered dynamically by JS -->
                </div>
            </div>

            <!-- Custom Date Range Sub-bar -->
            <div id="custom-date-container" class="hidden bg-emerald-50/80 p-4 rounded-2xl border border-emerald-200 flex flex-col sm:flex-row items-end gap-3 transition-all">
                <div class="flex-1 w-full">
                    <label class="block text-xs font-semibold text-emerald-800 mb-1">ตั้งแต่วันที่</label>
                    <input type="date" id="filter-start" class="w-full bg-white border border-emerald-300 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                </div>
                <div class="flex-1 w-full">
                    <label class="block text-xs font-semibold text-emerald-800 mb-1">ถึงวันที่</label>
                    <input type="date" id="filter-end" class="w-full bg-white border border-emerald-300 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                </div>
                <button onclick="applyCustomDateFilter()" class="w-full sm:w-auto bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2 rounded-xl text-sm font-medium shadow-sm transition-all">
                    ค้นหา
                </button>
            </div>

            <!-- 3 Executive KPI Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-5 sm:gap-6">
                <!-- Card 1: Total Revenue -->
                <div class="bg-gradient-to-br from-emerald-500 to-emerald-700 rounded-3xl p-6 text-white shadow-lg shadow-emerald-500/10 relative overflow-hidden group transform hover:-translate-y-1 transition-all duration-300">
                    <div class="absolute -right-3 -bottom-3 text-white/15 group-hover:scale-110 transition-transform duration-500">
                        <i class="fas fa-hand-holding-dollar text-8xl"></i>
                    </div>
                    <div class="relative z-10 space-y-3">
                        <div class="flex items-center justify-between">
                            <span class="text-emerald-100 text-sm font-medium bg-white/10 px-3 py-1 rounded-full backdrop-blur-md">
                                <i class="fas fa-arrow-trend-up mr-1 text-emerald-200"></i> รายรับรวม (Total Revenue)
                            </span>
                        </div>
                        <h3 class="text-3xl xl:text-4xl font-bold tracking-tight" id="kpi-income">฿0.00</h3>
                        <p class="text-xs text-emerald-100/90 font-light flex items-center gap-1.5" id="kpi-income-sub">
                            <i class="far fa-clock"></i> ยอดรายรับจากการขายสินค้า
                        </p>
                    </div>
                </div>

                <!-- Card 2: Total Expenses -->
                <div class="bg-gradient-to-br from-rose-500 to-red-700 rounded-3xl p-6 text-white shadow-lg shadow-rose-500/10 relative overflow-hidden group transform hover:-translate-y-1 transition-all duration-300">
                    <div class="absolute -right-3 -bottom-3 text-white/15 group-hover:scale-110 transition-transform duration-500">
                        <i class="fas fa-receipt text-8xl"></i>
                    </div>
                    <div class="relative z-10 space-y-3">
                        <div class="flex items-center justify-between">
                            <span class="text-rose-100 text-sm font-medium bg-white/10 px-3 py-1 rounded-full backdrop-blur-md">
                                <i class="fas fa-arrow-trend-down mr-1 text-rose-200"></i> รายจ่ายรวม (Total Expenses)
                            </span>
                        </div>
                        <h3 class="text-3xl xl:text-4xl font-bold tracking-tight" id="kpi-expense">฿0.00</h3>
                        <p class="text-xs text-rose-100/90 font-light flex items-center gap-1.5" id="kpi-expense-sub">
                            <i class="far fa-clock"></i> ต้นทุนขายและค่าใช้จ่ายดำเนินงาน
                        </p>
                    </div>
                </div>

                <!-- Card 3: Net Profit / Loss -->
                <div id="card-profit-bg" class="bg-gradient-to-br from-indigo-600 to-blue-800 rounded-3xl p-6 text-white shadow-lg shadow-indigo-500/10 relative overflow-hidden group transform hover:-translate-y-1 transition-all duration-300">
                    <div class="absolute -right-3 -bottom-3 text-white/15 group-hover:scale-110 transition-transform duration-500">
                        <i class="fas fa-chart-line text-8xl"></i>
                    </div>
                    <div class="relative z-10 space-y-3">
                        <div class="flex items-center justify-between">
                            <span class="text-indigo-100 text-sm font-medium bg-white/10 px-3 py-1 rounded-full backdrop-blur-md" id="kpi-profit-badge">
                                <i class="fas fa-scale-balanced mr-1"></i> กำไร (ขาดทุน) สุทธิ
                            </span>
                            <span class="text-xs bg-white/20 px-2.5 py-1 rounded-lg font-semibold" id="kpi-margin-pct">0.0%</span>
                        </div>
                        <h3 class="text-3xl xl:text-4xl font-bold tracking-tight" id="kpi-profit">฿0.00</h3>
                        <p class="text-xs text-indigo-100/90 font-light flex items-center gap-1.5" id="kpi-profit-sub">
                            <i class="fas fa-check-circle"></i> ผลการดำเนินงานสุทธิ
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Cash Flow & Accounts/Wallets Summary (สรุปกระแสเงินสดและยอดเงินคงเหลือแยกตามกระเป๋า/บัญชี) -->
        <section class="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden space-y-4 p-5 sm:p-6">
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b pb-4 border-slate-100">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-2xl bg-amber-500 text-slate-900 flex items-center justify-center font-bold text-lg shadow-md shadow-amber-500/20">
                        <i class="fas fa-wallet"></i>
                    </div>
                    <div>
                        <h2 class="text-lg sm:text-xl font-bold text-slate-800">สรุปกระแสเงินสดคงเหลือ แยกตามบัญชี / กระเป๋าเงิน</h2>
                        <p class="text-xs text-slate-500">ติดตามยอดเงินสดหน้าร้าน บัญชีธนาคาร และเงินสำรองของสหกรณ์</p>
                    </div>
                </div>

                <button onclick="openWalletModal()" class="px-4 py-2 bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200 font-semibold rounded-xl text-xs sm:text-sm transition-all flex items-center gap-1.5">
                    <i class="fas fa-gear"></i> จัดการบัญชี / เพิ่มกระเป๋าเงิน
                </button>
            </div>

            <!-- Dynamic Wallet & Cash Flow Cards Grid -->
            <div id="cashflow-cards-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pt-2">
                <!-- Loaded dynamically by JS -->
            </div>
        </section>

        <!-- Section 2: Detailed Monthly Income Statement Table (งบกำไรขาดทุนแบบแจงรายละเอียดรายเดือน) -->
        <section class="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="p-5 sm:p-6 border-b border-slate-100 bg-slate-50/70 flex items-center justify-between flex-wrap gap-3">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-lg shadow-sm">
                        <i class="fas fa-file-invoice-dollar"></i>
                    </div>
                    <div>
                        <h2 class="text-lg sm:text-xl font-bold text-slate-800">สรุปงบกำไรขาดทุน (Income Statement)</h2>
                        <p class="text-xs text-slate-500" id="pnl-subtitle">รายงานผลการดำเนินงานเปรียบเทียบรายเดือน สหกรณ์โรงเรียนบ้านน้ำพร</p>
                    </div>
                </div>
                <span class="text-xs font-semibold px-3 py-1 bg-emerald-50 text-emerald-700 rounded-full border border-emerald-200/60" id="pnl-period-badge">
                    ช่วงเวลา: ทั้งหมด
                </span>
            </div>

            <div class="p-5 sm:p-6 overflow-x-auto custom-scrollbar">
                <table class="w-full text-left border-collapse min-w-[750px] text-sm sm:text-base">
                    <thead id="pnl-table-head">
                        <!-- Dynamic Month Headers -->
                    </thead>
                    <tbody id="pnl-table-body" class="divide-y divide-slate-100">
                        <!-- Loaded dynamically with monthly details -->
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Section 3: Visual Analytics (แผนภูมิเปรียบเทียบ รายรับ - รายจ่าย - กำไรสุทธิ แบบดั้งเดิม) -->
        <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Chart 1: Monthly Grouped Bar Chart (2 cols) -->
            <div class="lg:col-span-2 bg-white p-5 sm:p-6 rounded-3xl shadow-sm border border-slate-200 space-y-4">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b pb-3 border-slate-100">
                    <div>
                        <h3 class="font-bold text-slate-800 text-base sm:text-lg flex items-center gap-2">
                            <i class="fas fa-chart-bar text-emerald-600"></i>
                            <span>เปรียบเทียบ รายรับ - รายจ่าย - กำไรสุทธิ แต่ละเดือน</span>
                        </h3>
                        <p class="text-xs text-slate-500">แสดงแท่งเปรียบเทียบรายรับ รายจ่าย และกำไรสุทธิ แยกตามเดือน (Grouped Bar Chart)</p>
                    </div>
                </div>
                <div class="relative h-64 sm:h-80 w-full">
                    <canvas id="monthlyBarChart"></canvas>
                </div>
            </div>

            <!-- Chart 2: Expense Category Breakdown (1 col) -->
            <div class="bg-white p-5 sm:p-6 rounded-3xl shadow-sm border border-slate-200 space-y-4">
                <h3 class="font-bold text-slate-800 text-base sm:text-lg flex items-center gap-2">
                    <i class="fas fa-chart-pie text-rose-500"></i>
                    <span>สัดส่วนค่าใช้จ่ายตามหมวดหมู่</span>
                </h3>
                <div class="relative h-64 sm:h-80 w-full flex items-center justify-center">
                    <canvas id="expenseDoughnutChart"></canvas>
                </div>
            </div>
        </section>

        <!-- Section 4: Batch Entry Grid (ตารางกรอกหลายแถวพร้อมกัน Default: รายจ่าย + เลือกบัญชี/กระเป๋าเงิน) -->
        <section class="bg-white rounded-3xl shadow-sm border border-slate-200 p-5 sm:p-6 lg:p-8 space-y-6">
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b pb-4 border-slate-100">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-2xl bg-emerald-600 text-white flex items-center justify-center font-bold text-lg shadow-md shadow-emerald-600/20">
                        <i class="fas fa-table-cells"></i>
                    </div>
                    <div>
                        <h2 class="text-lg sm:text-xl font-bold text-slate-800">บันทึกรายการแบบหลายแถว (Batch Entry Grid)</h2>
                        <p class="text-xs text-slate-500">เริ่มต้นตั้งค่าเริ่มต้นเป็น <span class="text-rose-600 font-bold">🔴 รายจ่าย</span> (สามารถระบุบัญชีธนาคาร/กระเป๋าเงินสดได้)</p>
                    </div>
                </div>

                <div class="flex flex-wrap items-center gap-2 w-full sm:w-auto">
                    <button type="button" onclick="addBatchRow()" class="px-4 py-2 bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200 font-semibold rounded-xl text-xs sm:text-sm transition-all flex items-center gap-1.5">
                        <i class="fas fa-plus"></i> เพิ่ม 1 แถว
                    </button>
                    <button type="button" onclick="addMultipleBatchRows(5)" class="px-4 py-2 bg-slate-100 text-slate-700 hover:bg-slate-200 font-semibold rounded-xl text-xs sm:text-sm transition-all flex items-center gap-1.5">
                        <i class="fas fa-layer-group"></i> เพิ่ม 5 แถว
                    </button>
                    <button type="button" onclick="clearBatchRows()" class="px-3 py-2 text-slate-400 hover:text-rose-600 font-medium rounded-xl text-xs transition-all">
                        <i class="fas fa-trash-alt"></i> ล้างตาราง
                    </button>
                </div>
            </div>

            <!-- Batch Input Table with Wallet Selector -->
            <div class="overflow-x-auto custom-scrollbar pb-2">
                <table class="w-full text-left border-collapse min-w-[980px]">
                    <thead>
                        <tr class="bg-slate-100 text-slate-600 uppercase text-xs tracking-wider rounded-xl">
                            <th class="py-2.5 px-3 font-bold w-10 text-center">#</th>
                            <th class="py-2.5 px-3 font-bold w-36">วันที่</th>
                            <th class="py-2.5 px-3 font-bold w-32">ประเภท</th>
                            <th class="py-2.5 px-3 font-bold w-48">หมวดหมู่ทางบัญชี</th>
                            <th class="py-2.5 px-3 font-bold w-48">เข้า/ออกจากบัญชี</th>
                            <th class="py-2.5 px-3 font-bold">ชื่อรายการ / คำอธิบาย</th>
                            <th class="py-2.5 px-3 font-bold w-32">จำนวนเงิน (บาท)</th>
                            <th class="py-2.5 px-3 font-bold w-36">เอกสาร/หมายเหตุ</th>
                            <th class="py-2.5 px-3 font-bold w-10 text-center">ลบ</th>
                        </tr>
                    </thead>
                    <tbody id="batch-table-body" class="divide-y divide-slate-100 text-sm">
                        <!-- Dynamic Editable Rows -->
                    </tbody>
                </table>
            </div>

            <!-- Save All Button Bar -->
            <div class="flex flex-col sm:flex-row items-center justify-between gap-4 border-t pt-4 border-slate-100">
                <span class="text-xs text-slate-500 font-medium" id="batch-row-count-label">
                    มี 3 แถวพร้อมกรอก
                </span>

                <div class="flex items-center gap-3 w-full sm:w-auto">
                    <button type="button" onclick="addBatchRow()" class="flex-1 sm:flex-none px-5 py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-2xl text-sm transition-all flex items-center justify-center gap-2">
                        <i class="fas fa-plus"></i> เพิ่มแถว
                    </button>
                    <button type="button" onclick="saveAllBatchRows()" class="flex-1 sm:flex-none px-8 py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-2xl shadow-lg shadow-emerald-600/20 transition-all transform hover:-translate-y-0.5 flex items-center justify-center gap-2">
                        <i class="fas fa-floppy-disk text-base"></i>
                        <span id="batch-save-btn-text">บันทึกทั้งหมด</span>
                    </button>
                </div>
            </div>
        </section>

        <!-- Section 5: Ledger Transaction History Table (Sortable Columns & Wallet Display) -->
        <section class="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden space-y-4">
            <!-- Table Controls Header -->
            <div class="p-5 sm:p-6 border-b border-slate-100 bg-slate-50/50 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h2 class="text-lg sm:text-xl font-bold text-slate-800 flex items-center gap-2">
                        <i class="fas fa-list-check text-emerald-600"></i>
                        <span>สมุดบัญชีประวัติรายการ (Transaction Ledger)</span>
                    </h2>
                    <p class="text-xs text-slate-500" id="ledger-count">แสดง 0 รายการ</p>
                </div>

                <div class="flex flex-wrap items-center gap-3 w-full md:w-auto">
                    <button onclick="importMayJuneExcelData()" class="px-3.5 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl text-xs flex items-center gap-1.5 shadow-sm transition-all">
                        <i class="fas fa-file-excel"></i> นำเข้า พ.ค.-มิ.ย. (94 รายการ)
                    </button>

                    <!-- Search input -->
                    <div class="relative flex-1 sm:w-64">
                        <input type="text" id="search-input" oninput="renderLedgerTable()" placeholder="ค้นหารายการ / บิล / บัญชี..." class="w-full pl-9 pr-4 py-2 bg-white border border-slate-300 rounded-xl text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                        <i class="fas fa-search absolute left-3 top-2.5 text-slate-400 text-xs"></i>
                    </div>

                    <!-- Wallet Filter selector -->
                    <select id="ledger-wallet-filter" onchange="renderLedgerTable()" class="bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs sm:text-sm font-medium focus:outline-none focus:ring-2 focus:ring-emerald-500">
                        <option value="all">แสดงทุกบัญชี/กระเป๋า</option>
                    </select>

                    <!-- Type Filter selector -->
                    <select id="ledger-type-filter" onchange="renderLedgerTable()" class="bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs sm:text-sm font-medium focus:outline-none focus:ring-2 focus:ring-emerald-500">
                        <option value="all">แสดงประเภททั้งหมด</option>
                        <option value="income">เฉพาะ รายรับ 🟢</option>
                        <option value="expense">เฉพาะ รายจ่าย 🔴</option>
                    </select>

                    <button onclick="openPosImportModal()" class="px-3.5 py-2 bg-amber-500 hover:bg-amber-600 text-slate-900 font-bold rounded-xl text-xs flex items-center gap-1.5 shadow-sm transition-all">
                        <i class="fas fa-cash-register"></i> นำเข้า POS
                    </button>
                </div>
            </div>

            <!-- Ledger Table with Interactive Sortable Headers -->
            <div class="overflow-x-auto custom-scrollbar px-5 sm:px-6 pb-6">
                <table class="w-full text-left border-collapse min-w-[850px]">
                    <thead>
                        <tr class="bg-slate-100/90 text-slate-700 uppercase text-xs tracking-wider rounded-xl">
                            <th onclick="toggleSort('date')" class="py-3.5 px-4 font-bold rounded-l-xl sortable-header text-emerald-800 hover:text-emerald-900">
                                วันที่ <span id="sort-icon-date" class="ml-1 text-slate-400">▼</span>
                            </th>
                            <th onclick="toggleSort('type')" class="py-3.5 px-4 font-bold sortable-header hover:text-emerald-900">
                                ประเภท <span id="sort-icon-type" class="ml-1 text-slate-400">⇕</span>
                            </th>
                            <th onclick="toggleSort('category')" class="py-3.5 px-4 font-bold sortable-header hover:text-emerald-900">
                                หมวดหมู่ <span id="sort-icon-category" class="ml-1 text-slate-400">⇕</span>
                            </th>
                            <th class="py-3.5 px-4 font-bold">
                                บัญชี/กระเป๋า
                            </th>
                            <th onclick="toggleSort('item')" class="py-3.5 px-4 font-bold sortable-header hover:text-emerald-900">
                                รายการ <span id="sort-icon-item" class="ml-1 text-slate-400">⇕</span>
                            </th>
                            <th onclick="toggleSort('doc')" class="py-3.5 px-4 font-bold sortable-header hover:text-emerald-900">
                                เอกสาร/หมายเหตุ <span id="sort-icon-doc" class="ml-1 text-slate-400">⇕</span>
                            </th>
                            <th onclick="toggleSort('amount')" class="py-3.5 px-4 font-bold text-right sortable-header hover:text-emerald-900">
                                จำนวนเงิน (บาท) <span id="sort-icon-amount" class="ml-1 text-slate-400">⇕</span>
                            </th>
                            <th class="py-3.5 px-4 font-bold text-center rounded-r-xl w-24">จัดการ</th>
                        </tr>
                    </thead>
                    <tbody id="ledger-table-body" class="divide-y divide-slate-100 text-sm">
                        <!-- Data dynamically loaded -->
                    </tbody>
                </table>
            </div>
        </section>

    </main>

    <!-- Wallet / Account Management Modal (จัดการกระเป๋าเงินสด / บัญชีธนาคาร) -->
    <div id="wallet-modal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4 transition-opacity">
        <div class="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl space-y-6 transform transition-all border border-slate-100">
            <div class="flex justify-between items-center border-b pb-4 border-slate-100">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-2xl bg-emerald-600 text-white flex items-center justify-center font-bold text-lg shadow-md shadow-emerald-600/20">
                        <i class="fas fa-wallet"></i>
                    </div>
                    <div>
                        <h3 class="text-lg font-bold text-slate-800">จัดการบัญชีธนาคาร / กระเป๋าเงินสด</h3>
                        <p class="text-xs text-slate-500">กำหนดชื่อบัญชี เลขที่บัญชี และยอดยกมาเริ่มต้น</p>
                    </div>
                </div>
                <button onclick="closeWalletModal()" class="text-slate-400 hover:text-slate-600 transition-colors">
                    <i class="fas fa-xmark text-xl"></i>
                </button>
            </div>

            <!-- List of Current Accounts/Wallets -->
            <div class="space-y-3 max-h-60 overflow-y-auto custom-scrollbar pr-1" id="wallet-list-container">
                <!-- Loaded dynamically by JS -->
            </div>

            <!-- Add / Edit Account Form -->
            <form id="wallet-form" onsubmit="handleWalletSubmit(event)" class="bg-slate-50 p-4 rounded-2xl border border-slate-200 space-y-3">
                <h4 class="text-xs font-bold text-slate-700 uppercase flex items-center gap-1.5" id="wallet-form-title">
                    <i class="fas fa-plus-circle text-emerald-600"></i> เพิ่มบัญชี / กระเป๋าเงินใหม่
                </h4>
                <input type="hidden" id="wallet-edit-id">

                <div>
                    <label class="block text-[11px] font-semibold text-slate-700 mb-1">ชื่อบัญชี/กระเป๋าเงิน (กำหนดชื่อเองได้)</label>
                    <input type="text" id="wallet-name" required placeholder="เช่น เงินสดหน้าร้าน, บัญชีออมทรัพย์ กรุงไทย" class="w-full bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500">
                </div>

                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-[11px] font-semibold text-slate-700 mb-1">หมวดหมู่/ประเภท</label>
                        <select id="wallet-type" onchange="toggleBankFields()" required class="w-full bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500">
                            <option value="cash">💵 กระเป๋าเงินสด (Cash Wallet)</option>
                            <option value="bank">🏦 บัญชีธนาคาร (Bank Account)</option>
                            <option value="other">👛 เงินสำรอง / อื่นๆ (Other)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-[11px] font-semibold text-slate-700 mb-1">ยอดยกมาเริ่มต้น (บาท)</label>
                        <input type="number" step="0.01" id="wallet-init-balance" placeholder="0.00" class="w-full bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs font-bold text-right focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    </div>
                </div>

                <!-- Conditional Bank Details Fields -->
                <div id="bank-fields-container" class="hidden grid grid-cols-2 gap-3 pt-1 border-t border-slate-200">
                    <div>
                        <label class="block text-[11px] font-semibold text-slate-700 mb-1">ชื่อธนาคาร / ชื่อบัญชี</label>
                        <input type="text" id="wallet-bank-name" placeholder="เช่น ธนาคารกรุงไทย สหกรณ์โรงเรียน" class="w-full bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    </div>
                    <div>
                        <label class="block text-[11px] font-semibold text-slate-700 mb-1">เลขที่บัญชีธนาคาร</label>
                        <input type="text" id="wallet-account-no" placeholder="เช่น 123-4-56789-0" class="w-full bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs font-mono focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    </div>
                </div>

                <div class="flex gap-2 pt-2">
                    <button type="button" onclick="resetWalletForm()" class="px-3 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 rounded-xl text-xs font-medium">ยกเลิก/ล้างฟอร์ม</button>
                    <button type="submit" class="flex-1 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold shadow-md shadow-emerald-600/20">บันทึกบัญชี</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Dedicated Modal: POS Sales Export.xlsx Importer -->
    <div id="pos-import-modal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4 transition-opacity">
        <div class="bg-white rounded-3xl max-w-xl w-full p-6 sm:p-8 shadow-2xl space-y-6 transform transition-all border border-slate-100">
            <div class="flex justify-between items-center border-b pb-4 border-slate-100 no-print">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-2xl bg-amber-500 text-slate-900 flex items-center justify-center font-bold text-lg shadow-md shadow-amber-500/20">
                        <i class="fas fa-cash-register"></i>
                    </div>
                    <div>
                        <h3 class="text-lg font-bold text-slate-800">นำเข้ารายรับหน้าร้านจาก POS (Sales_Export.xlsx)</h3>
                        <p class="text-xs text-slate-500">รองรับไฟล์ Excel ต้นฉบับจากโปรแกรม POS หน้าร้าน</p>
                    </div>
                </div>
                <button onclick="closePosImportModal()" class="text-slate-400 hover:text-slate-600 transition-colors">
                    <i class="fas fa-xmark text-xl"></i>
                </button>
            </div>

            <!-- Import Options -->
            <div class="space-y-4 no-print">
                <div class="bg-amber-50/80 p-4 rounded-2xl border border-amber-200 space-y-3">
                    <label class="block text-xs font-bold text-amber-900 uppercase">รูปแบบการนำเข้าข้อมูล POS</label>
                    <div class="space-y-2 text-xs sm:text-sm">
                        <label class="flex items-center gap-2 cursor-pointer font-semibold text-slate-800">
                            <input type="radio" name="pos-mode" value="summary" checked class="w-4 h-4 text-emerald-600 focus:ring-emerald-500">
                            <span>รวมยอดขายสรุปรายวัน (Daily Summary - แนะนำ)</span>
                        </label>
                        <p class="text-xs text-slate-500 pl-6">รวมยอดขายของแต่ละวันเป็น 1 รายการ ช่วยให้สมุดบัญชีเป็นระเบียบ เรียบง่าย</p>

                        <label class="flex items-center gap-2 cursor-pointer font-semibold text-slate-800 pt-2">
                            <input type="radio" name="pos-mode" value="detail" class="w-4 h-4 text-emerald-600 focus:ring-emerald-500">
                            <span>นำเข้าแยกรายใบเสร็จ (Detailed Receipts)</span>
                        </label>
                        <p class="text-xs text-slate-500 pl-6">นำเข้าแยกย่อยทุกใบเสร็จ INV (เหมาะกับการตรวจสอบประวัติแบบรายละเอียด)</p>
                    </div>
                </div>

                <!-- Target Account/Wallet selection for POS Import -->
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">บันทึกรายรับ POS เข้าบัญชี/กระเป๋าเงิน:</label>
                    <select id="pos-target-wallet" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs font-medium">
                        <!-- Loaded dynamically -->
                    </select>
                </div>

                <!-- Two Ways to Import -->
                <div class="space-y-3 pt-2">
                    <!-- Option 1: Choose File -->
                    <button onclick="triggerPosExcelSelect()" class="w-full py-3.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-2xl shadow-md shadow-emerald-600/20 transition-all flex items-center justify-center gap-2">
                        <i class="fas fa-file-excel text-lg"></i>
                        <span>เลือกไฟล์ Sales_Export.xlsx จากเครื่อง...</span>
                    </button>

                    <!-- Option 2: 1-Click Shortcut -->
                    <button onclick="importBundledPosData()" class="w-full py-3 px-4 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold rounded-2xl border border-slate-200 transition-all flex items-center justify-center gap-2 text-xs sm:text-sm">
                        <i class="fas fa-bolt text-amber-500"></i>
                        <span>นำเข้าจากไฟล์ Sales_Export.xlsx ในระบบสหกรณ์ทันที (45 วัน)</span>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal 1: Edit Modal -->
    <div id="edit-modal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4 transition-opacity">
        <div class="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl space-y-6 transform transition-all">
            <div class="flex justify-between items-center border-b pb-4 border-slate-100 no-print">
                <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
                    <i class="fas fa-pen-to-square text-amber-500"></i>
                    <span>แก้ไขรายการ</span>
                </h3>
                <button onclick="closeEditModal()" class="text-slate-400 hover:text-slate-600 transition-colors">
                    <i class="fas fa-xmark text-xl"></i>
                </button>
            </div>

            <form id="edit-form" onsubmit="handleEditSubmit(event)" class="space-y-4 no-print">
                <input type="hidden" id="edit-id">
                
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">วันที่</label>
                    <input type="date" id="edit-date" required class="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm">
                </div>

                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">ประเภท</label>
                        <select id="edit-type" onchange="updateEditCategoryOptions()" required class="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm">
                            <option value="expense">รายจ่าย (Expense)</option>
                            <option value="income">รายรับ (Income)</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">บัญชี/กระเป๋าเงิน</label>
                        <select id="edit-wallet" required class="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm">
                            <!-- Loaded dynamically -->
                        </select>
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">หมวดหมู่</label>
                    <select id="edit-category" required class="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm"></select>
                </div>

                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">ชื่อรายการ</label>
                    <input type="text" id="edit-item" required class="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm">
                </div>

                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">จำนวนเงิน (บาท)</label>
                    <input type="number" id="edit-amount" required min="0.01" step="0.01" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm font-semibold">
                </div>

                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">เอกสารอ้างอิง</label>
                    <input type="text" id="edit-doc" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm">
                </div>

                <div class="flex gap-3 pt-4 border-t border-slate-100">
                    <button type="button" onclick="closeEditModal()" class="flex-1 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-sm font-medium transition-colors">ยกเลิก</button>
                    <button type="submit" class="flex-1 py-2.5 bg-amber-500 hover:bg-amber-600 text-white rounded-xl text-sm font-bold shadow-md shadow-amber-500/20 transition-all">บันทึกการแก้ไข</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Modal 2: Delete Modal -->
    <div id="delete-modal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4 transition-opacity">
        <div class="bg-white rounded-3xl max-w-sm w-full p-6 text-center shadow-2xl space-y-4">
            <div class="w-14 h-14 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center mx-auto text-2xl">
                <i class="fas fa-trash-alt"></i>
            </div>
            <h3 class="text-lg font-bold text-slate-800">ยืนยันการลบรายการ?</h3>
            <p class="text-xs text-slate-500">คุณกำลังจะลบรายการนี้ออกจากระบบ การกระทำนี้ไม่สามารถย้อนกลับได้</p>
            <div class="flex gap-3 pt-2">
                <button onclick="closeDeleteModal()" class="flex-1 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-sm font-medium">ยกเลิก</button>
                <button id="confirm-delete-btn" class="flex-1 py-2.5 bg-rose-600 hover:bg-rose-700 text-white rounded-xl text-sm font-bold shadow-md shadow-rose-600/20">ลบรายการ</button>
            </div>
        </div>
    </div>

    <!-- Modal 3: Print Preview & Official Report Window (Strict A4 Layout + Dynamic Doughnut/Bar Chart Switch) -->
    <div id="print-modal" class="fixed inset-0 bg-slate-900/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-2 sm:p-4 overflow-y-auto">
        <div class="bg-white rounded-3xl max-w-4xl w-full p-6 sm:p-8 shadow-2xl space-y-6 max-h-[92vh] overflow-y-auto custom-scrollbar">
            <div class="flex items-center justify-between border-b pb-4 border-slate-200 no-print">
                <div class="flex items-center gap-3">
                    <i class="fas fa-print text-2xl text-emerald-600"></i>
                    <div>
                        <h3 class="text-lg font-bold text-slate-800">ตัวอย่างรายงานมาตรฐานขนาด A4 (Print Preview)</h3>
                        <p class="text-xs text-slate-500">จัดหน้าพอดีกระดาษ A4 รายงานต่อเนื่อง สลับกราฟโดนัทเว้นระยะเมื่อพิมพ์รายเดือน</p>
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="triggerPrint()" class="bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded-xl text-sm font-bold shadow-md flex items-center gap-2">
                        <i class="fas fa-print"></i> สั่งพิมพ์ A4 / บันทึก PDF
                    </button>
                    <button onclick="closePrintModal()" class="text-slate-400 hover:text-slate-600 p-2">
                        <i class="fas fa-xmark text-xl"></i>
                    </button>
                </div>
            </div>

            <!-- Signatory Inputs Section (3 Signers) -->
            <div class="bg-emerald-50/80 p-4 rounded-2xl border border-emerald-200 space-y-3 no-print">
                <h4 class="font-bold text-xs text-emerald-900 uppercase flex items-center gap-1.5">
                    <i class="fas fa-file-pen text-emerald-600"></i> กรอกชื่อผู้ลงนามรับรองรายงาน (3 ท่าน)
                </h4>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <div>
                        <label class="block text-[11px] font-semibold text-slate-700 mb-1">1. ผู้จัดทำรายงาน / เจ้าหน้าที่สหกรณ์</label>
                        <input type="text" id="signer-1-input" oninput="saveAndApplySigners()" placeholder="เช่น นายสมชาย ใจดี" class="w-full bg-white border border-slate-300 rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    </div>
                    <div>
                        <label class="block text-[11px] font-semibold text-slate-700 mb-1">2. ผู้ตรวจสอบ / ครูผู้รับผิดชอบ</label>
                        <input type="text" id="signer-2-input" oninput="saveAndApplySigners()" placeholder="เช่น นางสมศรี สุขใจ" class="w-full bg-white border border-slate-300 rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    </div>
                    <div>
                        <label class="block text-[11px] font-semibold text-slate-700 mb-1">3. ผู้อำนวยการโรงเรียนบ้านน้ำพร</label>
                        <input type="text" id="signer-3-input" oninput="saveAndApplySigners()" placeholder="เช่น นายวิจัย รักเรียน" class="w-full bg-white border border-slate-300 rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    </div>
                </div>
            </div>

            <!-- Print Document Container (Optimized A4 Dimension Container - Clean Continuous Flow) -->
            <div id="print-area" class="bg-white p-6 rounded-2xl border border-slate-200 space-y-6 text-slate-900">
                <!-- 1. Header Section with Centered Logo -->
                <div class="text-center pb-2 space-y-1 section-block">
                    <img src="https://ik.imagekit.io/boasnirut/32.png?updatedAt=1773125993394" 
                         onerror="this.src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png'" 
                         alt="โลโก้โรงเรียนบ้านน้ำพร" 
                         class="w-16 h-16 mx-auto mb-1.5 object-cover rounded-full">
                    <h2 class="text-xl font-bold uppercase tracking-wide">รายงานสรุปรับ-จ่าย และงบกำไรขาดทุน</h2>
                    <h3 class="text-lg font-semibold text-emerald-800">สหกรณ์โรงเรียนบ้านน้ำพร</h3>
                    <p class="text-xs text-slate-600" id="print-header-period">ประจำช่วงเวลา: ทั้งหมด</p>
                </div>

                <!-- 2. Print Summary KPI Dashboard Cards (รายรับรวม, รายจ่ายรวม, กำไรสุทธิ) -->
                <div class="grid grid-cols-3 gap-3 section-block p-2.5 rounded-xl bg-slate-50/50">
                    <div class="text-center p-2 bg-emerald-50 border border-emerald-300 rounded-lg">
                        <span class="text-[9pt] font-semibold text-emerald-800 block">รายรับรวม (Total Revenue)</span>
                        <span class="text-sm font-bold text-emerald-900" id="print-kpi-income">฿0.00</span>
                    </div>
                    <div class="text-center p-2 bg-rose-50 border border-rose-300 rounded-lg">
                        <span class="text-[9pt] font-semibold text-rose-800 block">รายจ่ายรวม (Total Expenses)</span>
                        <span class="text-sm font-bold text-rose-900" id="print-kpi-expense">฿0.00</span>
                    </div>
                    <div class="text-center p-2 bg-indigo-50 border border-indigo-300 rounded-lg" id="print-kpi-profit-box">
                        <span class="text-[9pt] font-semibold text-indigo-800 block" id="print-kpi-profit-label">กำไร (ขาดทุน) สุทธิ</span>
                        <span class="text-sm font-bold text-indigo-900" id="print-kpi-profit">฿0.00</span>
                    </div>
                </div>

                <!-- 3. Print Financial Summary Table (Clean Header) -->
                <div class="space-y-2 section-block">
                    <h4 class="font-bold text-sm text-slate-800 underline">สรุปงบกำไรขาดทุน (Income Statement)</h4>
                    <div class="overflow-x-auto">
                        <table class="w-full text-xs border border-slate-800 border-collapse print-table">
                            <thead id="print-pnl-head">
                                <!-- Loaded dynamically -->
                            </thead>
                            <tbody id="print-pnl-body">
                                <!-- Loaded dynamically -->
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- 4. Dynamic Chart Section (Grouped Bar Chart for All Months / Spaced Doughnut Chart for Single Month) -->
                <div class="space-y-2 section-block text-center p-2 rounded-xl bg-slate-50/50">
                    <h4 class="font-bold text-xs text-slate-800 underline mb-1" id="print-chart-title">แผนภูมิเปรียบเทียบ รายรับ - รายจ่าย - กำไรสุทธิ แต่ละเดือน (Grouped Bar Chart)</h4>
                    <div class="flex justify-center items-center">
                        <img id="print-chart-img" src="" alt="แผนภูมิเปรียบเทียบ" class="max-h-56 object-contain">
                    </div>
                </div>

                <!-- 5. Print Transaction Ledger (Flows continuously without page break) -->
                <div class="space-y-2 section-block print-ledger-section">
                    <h4 class="font-bold text-sm text-slate-800 underline">รายละเอียดประวัติรายการรับ-จ่าย (Transaction Ledger)</h4>
                    <table class="w-full text-xs border border-slate-800 border-collapse print-table">
                        <thead>
                            <tr class="bg-slate-100 text-slate-800 border-b border-slate-800">
                                <th class="p-1.5 text-center border-r border-slate-800 w-20 nowrap-cell">วันที่</th>
                                <th class="p-1.5 text-left border-r border-slate-800 w-16 nowrap-cell">ประเภท</th>
                                <th class="p-1.5 text-left border-r border-slate-800 w-32 nowrap-cell">หมวดหมู่</th>
                                <th class="p-1.5 text-left border-r border-slate-800">รายการ</th>
                                <th class="p-1.5 text-right w-24 nowrap-cell">จำนวนเงิน (บาท)</th>
                            </tr>
                        </thead>
                        <tbody id="print-ledger-body">
                            <!-- Loaded dynamically -->
                        </tbody>
                    </table>
                </div>

                <!-- 6. Sign-off Signatures AT THE VERY END -->
                <div class="signature-block grid grid-cols-3 gap-4 text-center text-xs text-slate-800 pt-12 mt-10">
                    <div class="space-y-3">
                        <p>ลงชื่อ..........................................................<br>( <span id="print-signer-1" class="font-semibold">..........................................................</span> )<br><span class="font-bold">ผู้จัดทำรายงาน / เจ้าหน้าที่สหกรณ์</span></p>
                    </div>
                    <div class="space-y-3">
                        <p>ลงชื่อ..........................................................<br>( <span id="print-signer-2" class="font-semibold">..........................................................</span> )<br><span class="font-bold">ผู้ตรวจสอบ / ครูผู้รับผิดชอบสหกรณ์</span></p>
                    </div>
                    <div class="space-y-3">
                        <p>ลงชื่อ..........................................................<br>( <span id="print-signer-3" class="font-semibold">..........................................................</span> )<br><span class="font-bold">ผู้อำนวยการโรงเรียนบ้านน้ำพร</span></p>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="fixed bottom-6 right-6 bg-slate-900 text-white px-5 py-3.5 rounded-2xl shadow-2xl z-50 flex items-center gap-3 transition-all duration-300 opacity-0 translate-y-4 pointer-events-none">
        <i id="toast-icon" class="fas fa-circle-check text-emerald-400 text-lg"></i>
        <span id="toast-message" class="text-sm font-medium">บันทึกข้อมูลเรียบร้อยแล้ว</span>
    </div>

    <!-- JavaScript Core Logic -->
    <script>
        // Pre-bundled POS Sales data template
        const posSalesTemplate = {pos_json_str};
        const mayJuneMasterTemplate = {may_june_json_str};

        // Wallets / Accounts State
        const defaultWallets = [
            {{ id: 'w_cash', name: 'เงินสดหน้าร้าน', type: 'cash', bankName: '', accountNo: '', initBalance: 0 }},
            {{ id: 'w_bank', name: 'บัญชีธนาคารสหกรณ์', type: 'bank', bankName: 'ธนาคารกรุงไทย', accountNo: '123-4-56789-0', initBalance: 0 }}
        ];
        let wallets = [];

        let transactions = [];
        let pendingRows = []; // State for Batch Entry Table
        let currentMonthFilter = 'all';
        let customStartDate = null;
        let customEndDate = null;

        // Sorting State for Ledger Table
        let currentSortColumn = 'date';
        let currentSortDirection = 'desc';

        let deleteTargetId = null;
        let monthlyChartInstance = null;
        let expenseChartInstance = null;

        const categoryDefs = {{
            income: {{
                income_shop: 'รายรับขายสินค้าหน้าร้าน',
                income_book: 'รายรับขายสินค้าตามสมุด',
                income_other: 'รายรับอื่นๆ / หุ้น'
            }},
            expense: {{
                exp_mall: 'ซื้อจากห้าง (Makro/Lotus/Big C)',
                exp_market: 'ซื้อจากตลาด/ร้านค้าส่ง',
                exp_wages: 'ค่าแรง',
                exp_utilities: 'สาธารณูปโภค',
                exp_other: 'ค่าใช้จ่ายอื่นๆ'
            }}
        }};

        const thaiMonthNames = {{
            '01': 'ม.ค.', '02': 'ก.พ.', '03': 'มี.ค.', '04': 'เม.ย.',
            '05': 'พ.ค.', '06': 'มิ.ย.', '07': 'ก.ค.', '08': 'ส.ค.',
            '09': 'ก.ย.', '10': 'ต.ค.', '11': 'พ.ย.', '12': 'ธ.ค.'
        }};

        const fullThaiMonthNames = {{
            '01': 'มกราคม', '02': 'กุมภาพันธ์', '03': 'มีนาคม', '04': 'เมษายน',
            '05': 'พฤษภาคม', '06': 'มิถุนายน', '07': 'กรกฎาคม', '08': 'สิงหาคม',
            '09': 'กันยายน', '10': 'ตุลาคม', '11': 'พฤศจิกายน', '12': 'ธันวาคม'
        }};

        function getMonthLabel(ym, full = false) {{
            if (!ym || ym.length < 7) return ym;
            const parts = ym.split('-');
            const year = parseInt(parts[0]) + 543;
            const map = full ? fullThaiMonthNames : thaiMonthNames;
            const month = map[parts[1]] || parts[1];
            return `${{month}} ${{year}}`;
        }}

        // App Initialization
        window.addEventListener('DOMContentLoaded', () => {{
            loadWallets();
            loadTransactions();
            loadSigners();
            initBatchRows(3);
            updateAllViews();
        }});

        // Automatic Before-Print Data Handler
        window.addEventListener('beforeprint', () => {{
            populatePrintReportData();
        }});

        function getTodayStr() {{
            const now = new Date();
            const year = now.getFullYear();
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            return `${{year}}-${{month}}-${{day}}`;
        }}

        // Import Master May and June Excel Data
        function importMayJuneExcelData() {{
            if (!mayJuneMasterTemplate || mayJuneMasterTemplate.length === 0) {{
                showToast('ไม่พบข้อมูล พ.ค.-มิ.ย. ในระบบ', 'error');
                return;
            }}

            const existingIds = new Set(transactions.map(t => t.id));
            const newEntries = mayJuneMasterTemplate.filter(t => !existingIds.has(t.id));

            if (newEntries.length === 0) {{
                showToast('ข้อมูล พ.ค.-มิ.ย. ทั้งหมด 94 รายการมีอยู่ในระบบเรียบร้อยแล้ว', 'info');
                return;
            }}

            transactions.unshift(...newEntries);
            saveTransactions();
            updateAllViews();
            showToast(`นำเข้าข้อมูล พ.ค. & มิ.ย. สำเร็จเรียบร้อย ${{newEntries.length}} รายการ!`, 'success');
        }}

        // Wallets / Accounts LocalStorage Management
        function loadWallets() {{
            const stored = localStorage.getItem('coop_wallets');
            if (stored) {{
                try {{
                    wallets = JSON.parse(stored);
                }} catch(e) {{
                    wallets = defaultWallets;
                }}
            }} else {{
                wallets = defaultWallets;
                saveWallets();
            }}
            populateWalletSelectors();
        }}

        function saveWallets() {{
            localStorage.setItem('coop_wallets', JSON.stringify(wallets));
        }}

        function populateWalletSelectors() {{
            const filterSel = document.getElementById('ledger-wallet-filter');
            filterSel.innerHTML = '<option value="all">แสดงทุกบัญชี/กระเป๋า</option>';
            wallets.forEach(w => {{
                const icon = w.type === 'cash' ? '💵' : (w.type === 'bank' ? '🏦' : '👛');
                filterSel.innerHTML += `<option value="${{w.id}}">${{icon}} ${{w.name}}</option>`;
            }});

            const posSel = document.getElementById('pos-target-wallet');
            if (posSel) {{
                posSel.innerHTML = '';
                wallets.forEach(w => {{
                    const icon = w.type === 'cash' ? '💵' : (w.type === 'bank' ? '🏦' : '👛');
                    posSel.innerHTML += `<option value="${{w.id}}">${{icon}} ${{w.name}}</option>`;
                }});
            }}

            const editSel = document.getElementById('edit-wallet');
            if (editSel) {{
                editSel.innerHTML = '';
                wallets.forEach(w => {{
                    const icon = w.type === 'cash' ? '💵' : (w.type === 'bank' ? '🏦' : '👛');
                    editSel.innerHTML += `<option value="${{w.id}}">${{icon}} ${{w.name}}</option>`;
                }});
            }}
        }}

        function loadTransactions() {{
            const stored = localStorage.getItem('coop_transactions');
            if (stored) {{
                try {{
                    transactions = JSON.parse(stored);
                    transactions.forEach(t => {{
                        if (!t.walletId) t.walletId = 'w_cash';
                    }});
                }} catch (e) {{
                    transactions = [...mayJuneMasterTemplate];
                }}
            }} else {{
                transactions = [...mayJuneMasterTemplate];
                saveTransactions();
            }}
        }}

        function saveTransactions() {{
            localStorage.setItem('coop_transactions', JSON.stringify(transactions));
        }}

        function resetToBlankDatabase() {{
            if (confirm('คุณต้องการล้างรายการทั้งหมดเพื่อเริ่มต้นใหม่จากฐานข้อมูลเปล่า ใช่หรือไม่?')) {{
                transactions = [];
                saveTransactions();
                updateAllViews();
                showToast('ล้างข้อมูลเรียบร้อยแล้ว เริ่มต้นใช้งานฐานข้อมูลเปล่า', 'success');
            }}
        }}

        // Signer Names Handlers
        function loadSigners() {{
            const stored = localStorage.getItem('coop_signers');
            if (stored) {{
                try {{
                    const s = JSON.parse(stored);
                    document.getElementById('signer-1-input').value = s.s1 || '';
                    document.getElementById('signer-2-input').value = s.s2 || '';
                    document.getElementById('signer-3-input').value = s.s3 || '';
                }} catch(e) {{}}
            }}
            updatePrintSignatures();
        }}

        function saveAndApplySigners() {{
            const s1 = document.getElementById('signer-1-input').value;
            const s2 = document.getElementById('signer-2-input').value;
            const s3 = document.getElementById('signer-3-input').value;

            localStorage.setItem('coop_signers', JSON.stringify({{ s1, s2, s3 }}));
            updatePrintSignatures();
        }}

        function updatePrintSignatures() {{
            const s1 = document.getElementById('signer-1-input').value.trim();
            const s2 = document.getElementById('signer-2-input').value.trim();
            const s3 = document.getElementById('signer-3-input').value.trim();

            document.getElementById('print-signer-1').textContent = s1 || '..........................................................';
            document.getElementById('print-signer-2').textContent = s2 || '..........................................................';
            document.getElementById('print-signer-3').textContent = s3 || '..........................................................';
        }}

        // ========================================================
        // DYNAMIC MONTH PRESET BUTTONS GENERATOR
        // ========================================================
        function renderMonthPresetButtons() {{
            const container = document.getElementById('month-preset-buttons-container');
            if (!container) return;

            // Collect all unique YYYY-MM months from transactions
            const monthSet = new Set();
            transactions.forEach(t => {{
                if (t.date && t.date.length >= 7) {{
                    monthSet.add(t.date.substring(0, 7));
                }}
            }});

            const months = Array.from(monthSet).sort();

            let html = '';

            // 1. "ทั้งหมด" button
            const isAll = currentMonthFilter === 'all';
            const allClass = isAll
                ? "px-3.5 py-1.5 text-xs sm:text-sm font-semibold rounded-xl transition-all shadow-sm bg-emerald-600 text-white"
                : "px-3.5 py-1.5 text-xs sm:text-sm font-medium rounded-xl transition-all bg-slate-100 text-slate-700 hover:bg-slate-200";
            html += `<button onclick="setMonthPreset('all')" id="btn-month-all" class="${{allClass}}">ทั้งหมด</button>`;

            // 2. "วันนี้" button
            const isToday = currentMonthFilter === 'today';
            const todayClass = isToday
                ? "px-3.5 py-1.5 text-xs sm:text-sm font-semibold rounded-xl transition-all shadow-sm bg-emerald-600 text-white"
                : "px-3.5 py-1.5 text-xs sm:text-sm font-medium rounded-xl transition-all bg-slate-100 text-slate-700 hover:bg-slate-200";
            html += `<button onclick="setMonthPreset('today')" id="btn-month-today" class="${{todayClass}}">วันนี้</button>`;

            // 3. Dynamic Month buttons (Automatically added for any existing month in database)
            months.forEach(m => {{
                const isSelected = currentMonthFilter === m;
                const btnClass = isSelected
                    ? "px-3.5 py-1.5 text-xs sm:text-sm font-semibold rounded-xl transition-all shadow-sm bg-emerald-600 text-white"
                    : "px-3.5 py-1.5 text-xs sm:text-sm font-medium rounded-xl transition-all bg-slate-100 text-slate-700 hover:bg-slate-200";
                html += `<button onclick="setMonthPreset('${{m}}')" id="btn-month-${{m}}" class="${{btnClass}}">${{getMonthLabel(m)}}</button>`;
            }});

            // 4. "กำหนดวัน" button
            const isCustom = currentMonthFilter === 'custom';
            const customClass = isCustom
                ? "px-3.5 py-1.5 text-xs sm:text-sm font-semibold rounded-xl transition-all shadow-sm bg-emerald-600 text-white flex items-center gap-1"
                : "px-3.5 py-1.5 text-xs sm:text-sm font-medium rounded-xl transition-all bg-slate-100 text-slate-700 hover:bg-slate-200 flex items-center gap-1";
            html += `<button onclick="toggleCustomDateModal()" id="btn-month-custom" class="${{customClass}}"><i class="far fa-calendar-alt"></i> กำหนดวัน</button>`;

            container.innerHTML = html;
        }}

        // ========================================================
        // CASH FLOW & WALLET MANAGEMENT MODAL
        // ========================================================
        function openWalletModal() {{
            renderWalletList();
            resetWalletForm();
            document.getElementById('wallet-modal').classList.remove('hidden');
        }}

        function closeWalletModal() {{
            document.getElementById('wallet-modal').classList.add('hidden');
        }}

        function toggleBankFields() {{
            const type = document.getElementById('wallet-type').value;
            const container = document.getElementById('bank-fields-container');
            if (type === 'bank') {{
                container.classList.remove('hidden');
            }} else {{
                container.classList.add('hidden');
            }}
        }}

        function resetWalletForm() {{
            document.getElementById('wallet-edit-id').value = '';
            document.getElementById('wallet-name').value = '';
            document.getElementById('wallet-type').value = 'cash';
            document.getElementById('wallet-init-balance').value = '0';
            document.getElementById('wallet-bank-name').value = '';
            document.getElementById('wallet-account-no').value = '';
            document.getElementById('wallet-form-title').innerHTML = '<i class="fas fa-plus-circle text-emerald-600"></i> เพิ่มบัญชี / กระเป๋าเงินใหม่';
            toggleBankFields();
        }}

        function editWallet(id) {{
            const w = wallets.find(x => x.id === id);
            if (!w) return;
            document.getElementById('wallet-edit-id').value = w.id;
            document.getElementById('wallet-name').value = w.name;
            document.getElementById('wallet-type').value = w.type;
            document.getElementById('wallet-init-balance').value = w.initBalance || 0;
            document.getElementById('wallet-bank-name').value = w.bankName || '';
            document.getElementById('wallet-account-no').value = w.accountNo || '';
            document.getElementById('wallet-form-title').innerHTML = '<i class="fas fa-pen-to-square text-amber-500"></i> แก้ไขบัญชี / กระเป๋าเงิน';
            toggleBankFields();
        }}

        function deleteWallet(id) {{
            if (wallets.length <= 1) {{
                showToast('ต้องมีบัญชี/กระเป๋าเงินอย่างน้อย 1 รายการในระบบ', 'error');
                return;
            }}
            if (confirm('คุณต้องการลบบัญชีนี้ใช่หรือไม่? รายการเดิมจะย้ายไปกระเป๋าเงินหลัก')) {{
                wallets = wallets.filter(x => x.id !== id);
                saveWallets();
                populateWalletSelectors();
                renderWalletList();
                updateAllViews();
                showToast('ลบบัญชีเรียบร้อยแล้ว', 'success');
            }}
        }}

        function handleWalletSubmit(e) {{
            e.preventDefault();
            const editId = document.getElementById('wallet-edit-id').value;
            const name = document.getElementById('wallet-name').value.trim();
            const type = document.getElementById('wallet-type').value;
            const initBal = parseFloat(document.getElementById('wallet-init-balance').value || 0);
            const bankName = document.getElementById('wallet-bank-name').value.trim();
            const accountNo = document.getElementById('wallet-account-no').value.trim();

            if (editId) {{
                const idx = wallets.findIndex(x => x.id === editId);
                if (idx !== -1) {{
                    wallets[idx] = {{ id: editId, name, type, bankName, accountNo, initBalance: initBal }};
                }}
            }} else {{
                const newId = 'w_' + Date.now();
                wallets.push({{ id: newId, name, type, bankName, accountNo, initBalance: initBal }});
            }}

            saveWallets();
            populateWalletSelectors();
            renderWalletList();
            resetWalletForm();
            updateAllViews();
            showToast('บันทึกข้อมูลบัญชีเรียบร้อยแล้ว', 'success');
        }}

        function renderWalletList() {{
            const container = document.getElementById('wallet-list-container');
            container.innerHTML = '';

            wallets.forEach(w => {{
                const icon = w.type === 'cash' ? 'fas fa-money-bill-wave text-emerald-600' : (w.type === 'bank' ? 'fas fa-building-columns text-blue-600' : 'fas fa-wallet text-amber-500');
                const badge = w.type === 'cash' ? 'เงินสด' : (w.type === 'bank' ? 'ธนาคาร' : 'อื่นๆ');
                
                const bankInfo = w.type === 'bank' && (w.bankName || w.accountNo) 
                    ? `<p class="text-[11px] text-slate-500 font-mono">${{w.bankName}} - เลขบัญชี: ${{w.accountNo}}</p>` 
                    : '';

                container.innerHTML += `
                    <div class="bg-slate-50 p-3 rounded-2xl border border-slate-200 flex items-center justify-between gap-3">
                        <div class="flex items-center gap-3">
                            <div class="w-9 h-9 rounded-xl bg-white text-slate-700 flex items-center justify-center shadow-sm">
                                <i class="${{icon}} text-base"></i>
                            </div>
                            <div>
                                <h5 class="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                                    <span>${{w.name}}</span>
                                    <span class="text-[10px] font-normal px-2 py-0.5 bg-slate-200 text-slate-700 rounded-md">${{badge}}</span>
                                </h5>
                                ${{bankInfo}}
                                <p class="text-[11px] text-slate-500">ยอดยกมาเริ่มต้น: <span class="font-bold text-slate-700">฿${{w.initBalance.toLocaleString('th-TH', {{minimumFractionDigits: 2}})}}</span></p>
                            </div>
                        </div>
                        <div class="flex items-center gap-1">
                            <button type="button" onclick="editWallet('${{w.id}}')" class="w-7 h-7 rounded-lg text-slate-400 hover:bg-amber-100 hover:text-amber-600 transition-all flex items-center justify-center">
                                <i class="fas fa-pen text-xs"></i>
                            </button>
                            <button type="button" onclick="deleteWallet('${{w.id}}')" class="w-7 h-7 rounded-lg text-slate-400 hover:bg-rose-100 hover:text-rose-600 transition-all flex items-center justify-center">
                                <i class="fas fa-trash-alt text-xs"></i>
                            </button>
                        </div>
                    </div>
                `;
            }});
        }}

        // Render Cash Flow Summary Cards
        function renderCashFlowCards(data) {{
            const grid = document.getElementById('cashflow-cards-grid');
            grid.innerHTML = '';

            let grandTotalBalance = 0;

            wallets.forEach(w => {{
                let inc = 0;
                let exp = 0;

                data.forEach(t => {{
                    if (t.walletId === w.id) {{
                        if (t.type === 'income') inc += t.amount;
                        else if (t.type === 'expense') exp += t.amount;
                    }}
                }});

                const currentBal = (w.initBalance || 0) + inc - exp;
                grandTotalBalance += currentBal;

                const icon = w.type === 'cash' ? 'fas fa-money-bill-wave text-emerald-500' : (w.type === 'bank' ? 'fas fa-building-columns text-blue-500' : 'fas fa-wallet text-amber-500');
                const bankLine = w.type === 'bank' && w.accountNo ? `<span class="text-[11px] font-mono text-slate-400 block">${{w.bankName || 'ธนาคาร'}} • ${{w.accountNo}}</span>` : '';

                grid.innerHTML += `
                    <div class="bg-slate-50/90 rounded-2xl p-4 border border-slate-200/80 space-y-2 hover:shadow-md transition-all">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2.5">
                                <i class="${{icon}} text-lg"></i>
                                <div>
                                    <h4 class="font-bold text-slate-800 text-sm leading-tight">${{w.name}}</h4>
                                    ${{bankLine}}
                                </div>
                            </div>
                            <span class="text-xs font-bold text-slate-700 bg-white px-2.5 py-1 rounded-xl shadow-xs border border-slate-200">
                                ฿${{currentBal.toLocaleString('th-TH', {{minimumFractionDigits: 2, maximumFractionDigits: 2}})}}
                            </span>
                        </div>
                        <div class="grid grid-cols-2 gap-2 text-xs pt-1 border-t border-slate-200/60">
                            <div>
                                <span class="text-slate-400 block text-[10px]">รายรับเข้า:</span>
                                <span class="font-bold text-emerald-600">+฿${{inc.toLocaleString('th-TH', {{minimumFractionDigits: 2}})}}</span>
                            </div>
                            <div>
                                <span class="text-slate-400 block text-[10px]">รายจ่ายออก:</span>
                                <span class="font-bold text-rose-600">-฿${{exp.toLocaleString('th-TH', {{minimumFractionDigits: 2}})}}</span>
                            </div>
                        </div>
                    </div>
                `;
            }});

            // Grand Total Card
            grid.innerHTML += `
                <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-4 text-white space-y-2 shadow-md">
                    <div class="flex items-center justify-between">
                        <span class="text-xs text-slate-300 font-semibold flex items-center gap-1.5">
                            <i class="fas fa-coins text-amber-400"></i> รวมกระแสเงินสดทุกบัญชี
                        </span>
                        <span class="text-xs bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-md font-bold">สุทธิ</span>
                    </div>
                    <h3 class="text-2xl font-bold tracking-tight text-amber-300">
                        ฿${{grandTotalBalance.toLocaleString('th-TH', {{minimumFractionDigits: 2, maximumFractionDigits: 2}})}}
                    </h3>
                    <p class="text-[11px] text-slate-400">ยอดเงินสดและเงินฝากธนาคารคงเหลือรวมทั้งสิ้น</p>
                </div>
            `;
        }}

        // ========================================================
        // DEDICATED POS SALES EXPORT.XLSX IMPORTER LOGIC
        // ========================================================
        function openPosImportModal() {{
            populateWalletSelectors();
            document.getElementById('pos-import-modal').classList.remove('hidden');
        }}

        function closePosImportModal() {{
            document.getElementById('pos-import-modal').classList.add('hidden');
        }}

        function triggerPosExcelSelect() {{
            document.getElementById('pos-excel-file-input').click();
        }}

        function importBundledPosData() {{
            if (!posSalesTemplate || posSalesTemplate.length === 0) {{
                showToast('ไม่พบข้อมูลแบบออฟไลน์', 'error');
                return;
            }}

            const targetWallet = document.getElementById('pos-target-wallet').value || 'w_cash';

            const newItems = posSalesTemplate.map(t => ({{
                ...t,
                walletId: targetWallet,
                id: Date.now() + Math.floor(Math.random() * 1000000)
            }}));

            transactions.unshift(...newItems);
            saveTransactions();
            updateAllViews();
            closePosImportModal();
            showToast(`นำเข้ารายรับหน้าร้าน POS สำเร็จเรียบร้อย ${{newItems.length}} วัน!`, 'success');
        }}

        function handlePosExcelSelect(event) {{
            const file = event.target.files[0];
            if (!file) return;

            const mode = document.querySelector('input[name="pos-mode"]:checked').value;
            const targetWallet = document.getElementById('pos-target-wallet').value || 'w_cash';
            const reader = new FileReader();

            reader.onload = function(e) {{
                try {{
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, {{ type: 'array' }});
                    const firstSheetName = workbook.SheetNames[0];
                    const worksheet = workbook.Sheets[firstSheetName];

                    const jsonData = XLSX.utils.sheet_to_json(worksheet);
                    parseAndImportPosData(jsonData, mode, targetWallet);
                    document.getElementById('pos-excel-file-input').value = '';
                }} catch(err) {{
                    console.error(err);
                    showToast('เกิดข้อผิดพลาดในการอ่านไฟล์ Excel POS', 'error');
                }}
            }};

            reader.readAsArrayBuffer(file);
        }}

        function parseAndImportPosData(rows, mode, targetWallet) {{
            if (!rows || rows.length === 0) {{
                showToast('ไม่พบข้อมูลในไฟล์ Excel POS', 'error');
                return;
            }}

            const newRecords = [];

            if (mode === 'summary') {{
                const dailyMap = {{}};

                rows.forEach(r => {{
                    const status = (r.Status || r.status || '').toString().trim();
                    const rawDate = r.Date || r.date;
                    const netTotal = parseFloat(r.NetTotal || r.subtotal || 0);

                    if ((status.toLowerCase() === 'active' || !status) && rawDate && !isNaN(netTotal) && netTotal > 0) {{
                        const isoDate = parsePosDate(rawDate);
                        if (!dailyMap[isoDate]) dailyMap[isoDate] = 0;
                        dailyMap[isoDate] += netTotal;
                    }}
                }});

                Object.keys(dailyMap).sort().forEach(d => {{
                    newRecords.push({{
                        id: Date.now() + Math.floor(Math.random() * 1000000),
                        date: d,
                        type: 'income',
                        category: 'income_shop',
                        categoryName: 'รายรับขายสินค้าหน้าร้าน',
                        item: 'ขายของได้ในโปรแกรม (POS หน้าร้าน)',
                        amount: Math.round(dailyMap[d] * 100) / 100,
                        doc: 'Sales_Export.xlsx',
                        walletId: targetWallet
                    }});
                }});

            }} else {{
                rows.forEach(r => {{
                    const status = (r.Status || r.status || '').toString().trim();
                    const rawDate = r.Date || r.date;
                    const receiptId = (r.ReceiptID || r.receiptid || 'POS').toString().trim();
                    const netTotal = parseFloat(r.NetTotal || r.subtotal || 0);

                    if ((status.toLowerCase() === 'active' || !status) && rawDate && !isNaN(netTotal) && netTotal > 0) {{
                        newRecords.push({{
                            id: Date.now() + Math.floor(Math.random() * 1000000),
                            date: parsePosDate(rawDate),
                            type: 'income',
                            category: 'income_shop',
                            categoryName: 'รายรับขายสินค้าหน้าร้าน',
                            item: `ขายสินค้าหน้าร้าน (บิล ${{receiptId}})`,
                            amount: netTotal,
                            doc: receiptId,
                            walletId: targetWallet
                        }});
                    }}
                }});
            }}

            if (newRecords.length > 0) {{
                transactions.unshift(...newRecords);
                saveTransactions();
                updateAllViews();
                closePosImportModal();
                showToast(`นำเข้ารายรับ POS สำเร็จทั้งหมด ${{newRecords.length}} รายการ!`, 'success');
            }} else {{
                showToast('ไม่พบรายการขาย POS ที่สมบูรณ์ในไฟล์', 'error');
            }}
        }}

        function parsePosDate(val) {{
            if (!val) return getTodayStr();
            const str = val.toString().trim();
            const datePart = str.split(' ')[0];

            const parts = datePart.split(/[-/]/);
            if (parts.length === 3) {{
                let d = parts[0].padStart(2, '0');
                let m = parts[1].padStart(2, '0');
                let y = parseInt(parts[2]);
                if (y > 2500) y = y - 543;
                return `${{y}}-${{m}}-${{d}}`;
            }}

            return getTodayStr();
        }}

        // ========================================================
        // INTERACTIVE TABLE COLUMN SORTING LOGIC
        // ========================================================
        function toggleSort(col) {{
            if (currentSortColumn === col) {{
                currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
            }} else {{
                currentSortColumn = col;
                currentSortDirection = (col === 'amount' || col === 'date') ? 'desc' : 'asc';
            }}
            updateSortIcons();
            renderLedgerTable();
        }}

        function updateSortIcons() {{
            const cols = ['date', 'type', 'category', 'item', 'doc', 'amount'];
            cols.forEach(c => {{
                const el = document.getElementById('sort-icon-' + c);
                if (el) {{
                    if (c === currentSortColumn) {{
                        el.textContent = currentSortDirection === 'asc' ? '▲' : '▼';
                        el.className = 'ml-1 text-emerald-600 font-bold';
                    }} else {{
                        el.textContent = '⇕';
                        el.className = 'ml-1 text-slate-300 font-normal';
                    }}
                }}
            }});
        }}

        // ========================================================
        // CSV IMPORT & EXPORT FEATURES (นำเข้า/ส่งออก CSV)
        // ========================================================
        function triggerCSVImport() {{
            document.getElementById('csv-file-input').click();
        }}

        function handleCSVFileSelect(event) {{
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {{
                const content = e.target.result;
                parseAndImportCSV(content);
                document.getElementById('csv-file-input').value = '';
            }};
            reader.readAsText(file, 'UTF-8');
        }}

        function parseAndImportCSV(csvText) {{
            let text = csvText.replace(/^\\uFEFF/, '');
            const lines = text.split(/\\r?\\n/);
            
            const newRecords = [];
            let skipHeader = true;

            lines.forEach(line => {{
                if (!line.trim()) return;

                const row = parseCSVLine(line);
                if (row.length < 4) return;

                const col0 = (row[0] || '').toLowerCase();
                if (skipHeader && (col0.includes('วันที่') || col0.includes('date'))) {{
                    skipHeader = false;
                    return;
                }}

                const dateStr = parseCSVDate(row[0]);
                const typeStr = (row[1] || '').trim();
                const type = (typeStr.includes('รับ') || typeStr.toLowerCase().includes('income')) ? 'income' : 'expense';

                const catInput = (row[2] || '').trim();
                const category = matchCategoryKey(catInput, type);
                const categoryName = categoryDefs[type][category] || catInput;

                const item = (row[3] || '').trim();
                const amountRaw = (row[4] || '0').replace(/[^0-9.-]/g, '');
                const amount = parseFloat(amountRaw);
                const doc = row[5] ? (row[5] || '').trim() : '';

                if (item && !isNaN(amount) && amount > 0) {{
                    newRecords.push({{
                        id: Date.now() + Math.floor(Math.random() * 1000000),
                        date: dateStr,
                        type: type,
                        category: category,
                        categoryName: categoryName,
                        item: item,
                        amount: amount,
                        doc: doc,
                        walletId: 'w_cash'
                    }});
                }}
            }});

            if (newRecords.length > 0) {{
                transactions.unshift(...newRecords);
                saveTransactions();
                updateAllViews();
                showToast(`นำเข้าสำเร็จทั้งหมด ${{newRecords.length}} รายการ!`, 'success');
            }} else {{
                showToast('ไม่พบรายการข้อมูลในไฟล์ CSV หรือรูปแบบไฟล์ไม่ถูกต้อง', 'error');
            }}
        }}

        function parseCSVLine(text) {{
            const result = [];
            let cur = '';
            let inQuotes = false;

            for (let i = 0; i < text.length; i++) {{
                const c = text[i];
                if (c === '"') {{
                    if (inQuotes && text[i+1] === '"') {{
                        cur += '"';
                        i++;
                    }} else {{
                        inQuotes = !inQuotes;
                    }}
                }} else if (c === ',' && !inQuotes) {{
                    result.push(cur.trim());
                    cur = '';
                }} else {{
                    cur += c;
                }}
            }}
            result.push(cur.trim());
            return result;
        }}

        function parseCSVDate(str) {{
            if (!str) return getTodayStr();
            const clean = str.replace(/"/g, '').trim();
            
            if (/^\\d{{4}}-\\d{{2}}-\\d{{2}}$/.test(clean)) return clean;

            const parts = clean.split(/[-/]/);
            if (parts.length === 3) {{
                let d = parts[0].padStart(2, '0');
                let m = parts[1].padStart(2, '0');
                let y = parseInt(parts[2]);
                if (y > 2500) y = y - 543;
                return `${{y}}-${{m}}-${{d}}`;
            }}

            return getTodayStr();
        }}

        function matchCategoryKey(catText, type) {{
            const defs = categoryDefs[type];
            for (let key in defs) {{
                if (defs[key] === catText || catText.includes(defs[key])) return key;
            }}
            return type === 'income' ? 'income_shop' : 'exp_mall';
        }}

        // Export to CSV
        function exportToCSV() {{
            const filtered = getFilteredData();
            let csvContent = "\\uFEFF";
            csvContent += "วันที่,ประเภท,หมวดหมู่,บัญชี/กระเป๋าเงิน,รายการ,จำนวนเงิน (บาท),เอกสารอ้างอิง\\n";

            filtered.forEach(t => {{
                const typeName = t.type === 'income' ? 'รายรับ' : 'รายจ่าย';
                const w = wallets.find(x => x.id === t.walletId);
                const wName = w ? w.name : 'เงินสดหน้าร้าน';

                const row = [
                    `"${{t.date}}"`,
                    `"${{typeName}}"`,
                    `"${{t.categoryName || t.category}}"`,
                    `"${{wName}}"`,
                    `"${{(t.item || '').replace(/"/g, '""')}}"`,
                    t.amount,
                    `"${{(t.doc || '').replace(/"/g, '""')}}"`
                ];
                csvContent += row.join(",") + "\\n";
            }});

            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", `รายงานรายรับรายจ่าย_สหกรณ์โรงเรียนบ้านน้ำพร_${{getTodayStr()}}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            showToast('ส่งออก CSV เรียบร้อยแล้ว', 'success');
        }}

        // ========================================================
        // BATCH ENTRY GRID LOGIC
        // ========================================================
        function initBatchRows(count = 3) {{
            pendingRows = [];
            for (let i = 0; i < count; i++) {{
                pendingRows.push(createEmptyPendingRow());
            }}
            renderBatchTable();
        }}

        function createEmptyPendingRow() {{
            const defaultW = wallets[0] ? wallets[0].id : 'w_cash';
            return {{
                tempId: Date.now() + Math.random(),
                date: getTodayStr(),
                type: 'expense',
                category: 'exp_mall',
                walletId: defaultW,
                item: '',
                amount: '',
                doc: ''
            }};
        }}

        function addBatchRow() {{
            pendingRows.push(createEmptyPendingRow());
            renderBatchTable();
        }}

        function addMultipleBatchRows(count = 5) {{
            for (let i = 0; i < count; i++) {{
                pendingRows.push(createEmptyPendingRow());
            }}
            renderBatchTable();
            showToast(`เพิ่มแถวใหม่ ${{count}} แถวเรียบร้อย`, 'success');
        }}

        function removeBatchRow(index) {{
            if (pendingRows.length <= 1) {{
                pendingRows = [createEmptyPendingRow()];
            }} else {{
                pendingRows.splice(index, 1);
            }}
            renderBatchTable();
        }}

        function clearBatchRows() {{
            initBatchRows(3);
            showToast('ล้างรายการในตารางเรียบร้อยแล้ว', 'success');
        }}

        function updatePendingRowField(index, field, value) {{
            if (!pendingRows[index]) return;
            pendingRows[index][field] = value;

            if (field === 'type') {{
                const newType = value;
                if (newType === 'income') {{
                    pendingRows[index].category = 'income_shop';
                }} else {{
                    pendingRows[index].category = 'exp_mall';
                }}
                renderBatchTable();
            }}
        }}

        function renderBatchTable() {{
            const tbody = document.getElementById('batch-table-body');
            tbody.innerHTML = '';

            pendingRows.forEach((row, idx) => {{
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-50 transition-colors border-b border-slate-100";

                const typeOptions = `
                    <select onchange="updatePendingRowField(${{idx}}, 'type', this.value)" class="w-full bg-white border border-slate-300 rounded-xl px-2 py-1.5 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-emerald-500">
                        <option value="expense" ${{row.type === 'expense' ? 'selected' : ''}}>🔴 รายจ่าย</option>
                        <option value="income" ${{row.type === 'income' ? 'selected' : ''}}>🟢 รายรับ</option>
                    </select>
                `;

                const cats = categoryDefs[row.type] || categoryDefs.expense;
                let catOptions = '';
                Object.entries(cats).forEach(([k, v]) => {{
                    catOptions += `<option value="${{k}}" ${{row.category === k ? 'selected' : ''}}>${{v}}</option>`;
                }});

                const categorySelect = `
                    <select onchange="updatePendingRowField(${{idx}}, 'category', this.value)" class="w-full bg-white border border-slate-300 rounded-xl px-2 py-1.5 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-emerald-500">
                        ${{catOptions}}
                    </select>
                `;

                let walletOptions = '';
                wallets.forEach(w => {{
                    const icon = w.type === 'cash' ? '💵' : (w.type === 'bank' ? '🏦' : '👛');
                    walletOptions += `<option value="${{w.id}}" ${{row.walletId === w.id ? 'selected' : ''}}>${{icon}} ${{w.name}}</option>`;
                }});

                const walletSelect = `
                    <select onchange="updatePendingRowField(${{idx}}, 'walletId', this.value)" class="w-full bg-white border border-slate-300 rounded-xl px-2 py-1.5 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-emerald-500">
                        ${{walletOptions}}
                    </select>
                `;

                tr.innerHTML = `
                    <td class="py-2.5 px-3 text-center text-slate-400 font-bold text-xs">${{idx + 1}}</td>
                    <td class="py-2.5 px-3">
                        <input type="date" value="${{row.date}}" onchange="updatePendingRowField(${{idx}}, 'date', this.value)" class="w-full bg-white border border-slate-300 rounded-xl px-2.5 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    </td>
                    <td class="py-2.5 px-3">${{typeOptions}}</td>
                    <td class="py-2.5 px-3">${{categorySelect}}</td>
                    <td class="py-2.5 px-3">${{walletSelect}}</td>
                    <td class="py-2.5 px-3">
                        <input type="text" value="${{row.item}}" oninput="updatePendingRowField(${{idx}}, 'item', this.value)" placeholder="กรอกชื่อรายการ..." class="w-full bg-white border border-slate-300 rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500 font-medium">
                    </td>
                    <td class="py-2.5 px-3">
                        <input type="number" step="0.01" min="0" value="${{row.amount}}" oninput="updatePendingRowField(${{idx}}, 'amount', this.value)" placeholder="0.00" class="w-full bg-white border border-slate-300 rounded-xl px-3 py-1.5 text-xs text-right font-bold focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    </td>
                    <td class="py-2.5 px-3">
                        <input type="text" value="${{row.doc}}" oninput="updatePendingRowField(${{idx}}, 'doc', this.value)" placeholder="บิล/หมายเหตุ..." class="w-full bg-white border border-slate-300 rounded-xl px-2.5 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    </td>
                    <td class="py-2.5 px-3 text-center">
                        <button type="button" onclick="removeBatchRow(${{idx}})" class="w-7 h-7 rounded-lg text-slate-400 hover:bg-rose-100 hover:text-rose-600 transition-all flex items-center justify-center mx-auto" title="ลบแถวนี้">
                            <i class="fas fa-xmark text-sm"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            }});

            const validCount = pendingRows.filter(r => r.item.trim() !== '' && !isNaN(parseFloat(r.amount)) && parseFloat(r.amount) > 0).length;
            document.getElementById('batch-row-count-label').textContent = `มี ${{pendingRows.length}} แถว (พร้อมบันทึก ${{validCount}} รายการ)`;
            document.getElementById('batch-save-btn-text').textContent = validCount > 0 ? `บันทึกทั้งหมด (${{validCount}} รายการ)` : 'บันทึกทั้งหมด';
        }}

        function saveAllBatchRows() {{
            const validItems = pendingRows.filter(r => r.item.trim() !== '' && !isNaN(parseFloat(r.amount)) && parseFloat(r.amount) > 0);

            if (validItems.length === 0) {{
                showToast('กรุณากรอกชื่อรายการและจำนวนเงินอย่างน้อย 1 รายการก่อนบันทึก', 'error');
                return;
            }}

            const newTransactions = validItems.map(r => ({{
                id: Date.now() + Math.floor(Math.random() * 100000),
                date: r.date || getTodayStr(),
                type: r.type,
                category: r.category,
                categoryName: categoryDefs[r.type][r.category] || r.category,
                walletId: r.walletId || (wallets[0] ? wallets[0].id : 'w_cash'),
                item: r.item.trim(),
                amount: parseFloat(r.amount),
                doc: (r.doc || '').trim()
            }}));

            transactions.unshift(...newTransactions);
            saveTransactions();

            initBatchRows(3);
            updateAllViews();
            showToast(`บันทึกรายการสำเร็จทั้งหมด ${{validItems.length}} รายการเรียบร้อยแล้ว!`, 'success');
        }}

        // Filtering Logic
        function setMonthPreset(mode) {{
            currentMonthFilter = mode;
            customStartDate = null;
            customEndDate = null;
            
            document.getElementById('custom-date-container').classList.add('hidden');

            renderMonthPresetButtons();
            updateAllViews();
        }}

        function toggleCustomDateModal() {{
            const container = document.getElementById('custom-date-container');
            container.classList.toggle('hidden');
        }}

        function applyCustomDateFilter() {{
            const start = document.getElementById('filter-start').value;
            const end = document.getElementById('filter-end').value;

            if (!start && !end) {{
                showToast('กรุณาเลือกวันที่เริ่มต้นหรือสิ้นสุด', 'error');
                return;
            }}

            currentMonthFilter = 'custom';
            customStartDate = start;
            customEndDate = end;

            renderMonthPresetButtons();
            updateAllViews();
        }}

        function getFilteredData() {{
            const todayStr = getTodayStr();

            return transactions.filter(t => {{
                if (currentMonthFilter === 'all') return true;
                if (currentMonthFilter === 'today') return t.date === todayStr;
                if (currentMonthFilter === 'custom') {{
                    if (customStartDate && t.date < customStartDate) return false;
                    if (customEndDate && t.date > customEndDate) return false;
                    return true;
                }}
                if (currentMonthFilter && t.date) {{
                    return t.date.startsWith(currentMonthFilter);
                }}
                return true;
            }});
        }}

        // Global Update Coordinator
        function updateAllViews() {{
            renderMonthPresetButtons();
            const filtered = getFilteredData();
            updateKPIs(filtered);
            renderCashFlowCards(filtered);
            updatePnLTable(filtered);
            renderLedgerTable();
            renderCharts();
            updateSortIcons();
        }}

        // 1. KPI Cards Update
        function updateKPIs(data) {{
            let totalIncome = 0;
            let totalExpense = 0;

            data.forEach(t => {{
                if (t.type === 'income') totalIncome += t.amount;
                else if (t.type === 'expense') totalExpense += t.amount;
            }});

            const netProfit = totalIncome - totalExpense;
            const marginPct = totalIncome > 0 ? (netProfit / totalIncome) * 100 : 0;

            document.getElementById('kpi-income').textContent = formatCurrency(totalIncome);
            document.getElementById('kpi-expense').textContent = formatCurrency(totalExpense);
            document.getElementById('kpi-profit').textContent = formatCurrency(netProfit);
            document.getElementById('kpi-margin-pct').textContent = `${{marginPct >= 0 ? '+' : ''}}${{marginPct.toFixed(1)}}%`;

            const profitCard = document.getElementById('card-profit-bg');
            if (netProfit >= 0) {{
                profitCard.className = "bg-gradient-to-br from-indigo-600 to-blue-800 rounded-3xl p-6 text-white shadow-lg shadow-indigo-500/10 relative overflow-hidden group transform hover:-translate-y-1 transition-all duration-300";
            }} else {{
                profitCard.className = "bg-gradient-to-br from-amber-600 to-rose-700 rounded-3xl p-6 text-white shadow-lg shadow-amber-500/10 relative overflow-hidden group transform hover:-translate-y-1 transition-all duration-300";
            }}
        }}

        // 2. Detailed Monthly Income Statement Matrix Generator
        function generateMonthlyPnLMatrix(data) {{
            const monthSet = new Set();
            data.forEach(t => {{
                if (t.date && t.date.length >= 7) {{
                    monthSet.add(t.date.substring(0, 7));
                }}
            }});

            const months = Array.from(monthSet).sort();
            if (months.length === 0) {{
                months.push(getTodayStr().substring(0, 7));
            }}

            const mData = {{}};
            months.forEach(m => {{
                mData[m] = {{
                    revShop: 0, revOther: 0,
                    cogsMall: 0, cogsMarket: 0,
                    opexWages: 0, opexUtil: 0, opexOther: 0
                }};
            }});

            data.forEach(t => {{
                const m = t.date ? t.date.substring(0, 7) : '';
                if (mData[m]) {{
                    const amt = t.amount || 0;
                    if (t.type === 'income') {{
                        if (t.category === 'income_shop') mData[m].revShop += amt;
                        else mData[m].revOther += amt;
                    }} else if (t.type === 'expense') {{
                        if (t.category === 'exp_mall') mData[m].cogsMall += amt;
                        else if (t.category === 'exp_market') mData[m].cogsMarket += amt;
                        else if (t.category === 'exp_wages') mData[m].opexWages += amt;
                        else if (t.category === 'exp_utilities') mData[m].opexUtil += amt;
                        else mData[m].opexOther += amt;
                    }}
                }}
            }});

            return {{ months, mData }};
        }}

        function updatePnLTable(data) {{
            const {{ months, mData }} = generateMonthlyPnLMatrix(data);

            let headHtml = `<tr class="border-b border-slate-200 text-slate-500 uppercase text-xs tracking-wider">
                <th class="py-3 px-4 font-bold text-slate-700">หมวดหมู่รายการ (Accounting Category)</th>`;
            
            months.forEach(m => {{
                headHtml += `<th class="py-3 px-4 font-bold text-slate-700 text-right whitespace-nowrap">${{getMonthLabel(m)}}</th>`;
            }});

            headHtml += `<th class="py-3 px-4 font-bold text-slate-800 text-right whitespace-nowrap">รวมทั้งสิ้น (บาท)</th>
                <th class="py-3 px-4 font-bold text-slate-700 text-right w-24 whitespace-nowrap">สัดส่วน (%)</th>
            </tr>`;

            document.getElementById('pnl-table-head').innerHTML = headHtml;

            let grandRev = 0, grandCOGS = 0, grandGross = 0, grandOpex = 0, grandNet = 0;
            const totals = {{
                revShop: 0, revOther: 0,
                cogsMall: 0, cogsMarket: 0,
                opexWages: 0, opexUtil: 0, opexOther: 0
            }};

            months.forEach(m => {{
                Object.keys(totals).forEach(k => {{
                    totals[k] += mData[m][k];
                }});
            }});

            grandRev = totals.revShop + totals.revOther;
            grandCOGS = totals.cogsMall + totals.cogsMarket;
            grandGross = grandRev - grandCOGS;
            grandOpex = totals.opexWages + totals.opexUtil + totals.opexOther;
            grandNet = grandGross - grandOpex;

            const getPct = val => grandRev > 0 ? ((val / grandRev) * 100).toFixed(2) + '%' : '0.00%';

            let bodyHtml = `
                <!-- 1. Revenue -->
                <tr class="bg-emerald-50/50 font-bold text-emerald-900">
                    <td class="py-3 px-4 flex items-center gap-2">
                        <i class="fas fa-circle-plus text-emerald-600 text-xs"></i>
                        <span>1. รายรับจากการขายสินค้า (Revenue from Sales)</span>
                    </td>`;
            months.forEach(m => {{
                const rM = mData[m].revShop + mData[m].revOther;
                bodyHtml += `<td class="py-3 px-4 text-right text-emerald-700 font-bold whitespace-nowrap">${{formatCurrency(rM)}}</td>`;
            }});
            bodyHtml += `<td class="py-3 px-4 text-right text-emerald-800 font-black whitespace-nowrap">${{formatCurrency(grandRev)}}</td>
                    <td class="py-3 px-4 text-right font-bold text-emerald-800">100.00%</td>
                </tr>
                <tr class="text-slate-600 text-sm">
                    <td class="py-2 pl-8 pr-4">• รายรับขายสินค้าหน้าร้าน / ในโปรแกรม (POS)</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-2 px-4 text-right whitespace-nowrap">${{formatCurrency(mData[m].revShop)}}</td>`;
            }});
            bodyHtml += `<td class="py-2 px-4 text-right font-semibold text-slate-800 whitespace-nowrap">${{formatCurrency(totals.revShop)}}</td>
                    <td class="py-2 px-4 text-right text-slate-500 text-xs">${{getPct(totals.revShop)}}</td>
                </tr>
                <tr class="text-slate-600 text-sm">
                    <td class="py-2 pl-8 pr-4">• รายรับขายสินค้าตามสมุด / อื่นๆ</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-2 px-4 text-right whitespace-nowrap">${{formatCurrency(mData[m].revOther)}}</td>`;
            }});
            bodyHtml += `<td class="py-2 px-4 text-right font-semibold text-slate-800 whitespace-nowrap">${{formatCurrency(totals.revOther)}}</td>
                    <td class="py-2 px-4 text-right text-slate-500 text-xs">${{getPct(totals.revOther)}}</td>
                </tr>

                <!-- 2. Cost of Goods Sold -->
                <tr class="bg-rose-50/50 font-bold text-rose-900">
                    <td class="py-3 px-4 flex items-center gap-2">
                        <i class="fas fa-circle-minus text-rose-600 text-xs"></i>
                        <span>2. หัก: ต้นทุนขายสินค้า (Cost of Goods Sold - COGS)</span>
                    </td>`;
            months.forEach(m => {{
                const cM = mData[m].cogsMall + mData[m].cogsMarket;
                bodyHtml += `<td class="py-3 px-4 text-right text-rose-700 font-bold whitespace-nowrap">${{formatCurrency(cM)}}</td>`;
            }});
            bodyHtml += `<td class="py-3 px-4 text-right text-rose-800 font-black whitespace-nowrap">${{formatCurrency(grandCOGS)}}</td>
                    <td class="py-3 px-4 text-right font-bold text-rose-800">${{getPct(grandCOGS)}}</td>
                </tr>
                <tr class="text-slate-600 text-sm">
                    <td class="py-2 pl-8 pr-4">• ซื้อสินค้าจากห้าง (Makro / Lotus / Big C)</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-2 px-4 text-right whitespace-nowrap">${{formatCurrency(mData[m].cogsMall)}}</td>`;
            }});
            bodyHtml += `<td class="py-2 px-4 text-right font-semibold text-slate-800 whitespace-nowrap">${{formatCurrency(totals.cogsMall)}}</td>
                    <td class="py-2 px-4 text-right text-slate-500 text-xs">${{getPct(totals.cogsMall)}}</td>
                </tr>
                <tr class="text-slate-600 text-sm">
                    <td class="py-2 pl-8 pr-4">• ซื้อสินค้าจากตลาด / ร้านค้าส่ง</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-2 px-4 text-right whitespace-nowrap">${{formatCurrency(mData[m].cogsMarket)}}</td>`;
            }});
            bodyHtml += `<td class="py-2 px-4 text-right font-semibold text-slate-800 whitespace-nowrap">${{formatCurrency(totals.cogsMarket)}}</td>
                    <td class="py-2 px-4 text-right text-slate-500 text-xs">${{getPct(totals.cogsMarket)}}</td>
                </tr>

                <!-- 3. Gross Profit -->
                <tr class="bg-slate-100/90 font-bold text-slate-800 border-t-2 border-slate-200">
                    <td class="py-3 px-4 flex items-center gap-2">
                        <i class="fas fa-equals text-slate-500 text-xs"></i>
                        <span>เท่ากับ: กำไรขั้นต้น (Gross Profit)</span>
                    </td>`;
            months.forEach(m => {{
                const gM = (mData[m].revShop + mData[m].revOther) - (mData[m].cogsMall + mData[m].cogsMarket);
                bodyHtml += `<td class="py-3 px-4 text-right text-slate-900 font-bold whitespace-nowrap">${{formatCurrency(gM)}}</td>`;
            }});
            bodyHtml += `<td class="py-3 px-4 text-right text-slate-900 font-black whitespace-nowrap">${{formatCurrency(grandGross)}}</td>
                    <td class="py-3 px-4 text-right font-bold text-slate-800">${{getPct(grandGross)}}</td>
                </tr>

                <!-- 4. Operating Expenses -->
                <tr class="bg-amber-50/50 font-bold text-amber-900">
                    <td class="py-3 px-4 flex items-center gap-2">
                        <i class="fas fa-circle-minus text-amber-600 text-xs"></i>
                        <span>3. หัก: ค่าใช้จ่ายในการดำเนินงาน (Operating Expenses)</span>
                    </td>`;
            months.forEach(m => {{
                const oM = mData[m].opexWages + mData[m].opexUtil + mData[m].opexOther;
                bodyHtml += `<td class="py-3 px-4 text-right text-amber-800 font-bold whitespace-nowrap">${{formatCurrency(oM)}}</td>`;
            }});
            bodyHtml += `<td class="py-3 px-4 text-right text-amber-900 font-black whitespace-nowrap">${{formatCurrency(grandOpex)}}</td>
                    <td class="py-3 px-4 text-right font-bold text-amber-900">${{getPct(grandOpex)}}</td>
                </tr>
                <tr class="text-slate-600 text-sm">
                    <td class="py-2 pl-8 pr-4">• ค่าแรง</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-2 px-4 text-right whitespace-nowrap">${{formatCurrency(mData[m].opexWages)}}</td>`;
            }});
            bodyHtml += `<td class="py-2 px-4 text-right font-semibold text-slate-800 whitespace-nowrap">${{formatCurrency(totals.opexWages)}}</td>
                    <td class="py-2 px-4 text-right text-slate-500 text-xs">${{getPct(totals.opexWages)}}</td>
                </tr>
                <tr class="text-slate-600 text-sm">
                    <td class="py-2 pl-8 pr-4">• สาธารณูปโภค (ค่าน้ำ/ไฟ/เน็ต)</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-2 px-4 text-right whitespace-nowrap">${{formatCurrency(mData[m].opexUtil)}}</td>`;
            }});
            bodyHtml += `<td class="py-2 px-4 text-right font-semibold text-slate-800 whitespace-nowrap">${{formatCurrency(totals.opexUtil)}}</td>
                    <td class="py-2 px-4 text-right text-slate-500 text-xs">${{getPct(totals.opexUtil)}}</td>
                </tr>
                <tr class="text-slate-600 text-sm">
                    <td class="py-2 pl-8 pr-4">• ค่าใช้จ่ายอื่นๆ (อุปกรณ์/วัสดุสำนักงาน)</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-2 px-4 text-right whitespace-nowrap">${{formatCurrency(mData[m].opexOther)}}</td>`;
            }});
            bodyHtml += `<td class="py-2 px-4 text-right font-semibold text-slate-800 whitespace-nowrap">${{formatCurrency(totals.opexOther)}}</td>
                    <td class="py-2 px-4 text-right text-slate-500 text-xs">${{getPct(totals.opexOther)}}</td>
                </tr>

                <!-- 5. Net Profit / Loss -->
                <tr class="bg-emerald-100/80 font-bold text-slate-900 border-t-2 border-b-2 border-slate-300 text-base">
                    <td class="py-4 px-4 flex items-center gap-2">
                        <i class="fas fa-award text-emerald-600"></i>
                        <span>เท่ากับ: กำไร (ขาดทุน) สุทธิ (Net Profit / Loss)</span>
                    </td>`;
            months.forEach(m => {{
                const rM = mData[m].revShop + mData[m].revOther;
                const cM = mData[m].cogsMall + mData[m].cogsMarket;
                const oM = mData[m].opexWages + mData[m].opexUtil + mData[m].opexOther;
                const netM = (rM - cM) - oM;
                bodyHtml += `<td class="py-4 px-4 text-right font-bold whitespace-nowrap">${{formatCurrency(netM)}}</td>`;
            }});
            bodyHtml += `<td class="py-4 px-4 text-right font-black text-emerald-900 whitespace-nowrap text-lg">${{formatCurrency(grandNet)}}</td>
                    <td class="py-4 px-4 text-right font-bold text-emerald-900">${{getPct(grandNet)}}</td>
                </tr>
            `;

            document.getElementById('pnl-table-body').innerHTML = bodyHtml;

            let periodText = "ทั้งหมด";
            if (currentMonthFilter === 'today') periodText = "วันนี้ (" + formatThaiDate(getTodayStr()) + ")";
            else if (currentMonthFilter === 'custom') {{
                periodText = (customStartDate ? formatThaiDate(customStartDate) : 'เริ่มต้น') + " ถึง " + (customEndDate ? formatThaiDate(customEndDate) : 'ปัจจุบัน');
            }} else if (currentMonthFilter !== 'all') {{
                periodText = getMonthLabel(currentMonthFilter, true);
            }}
            document.getElementById('pnl-period-badge').textContent = "ช่วงเวลา: " + periodText;
            document.getElementById('pnl-subtitle').textContent = "เปรียบเทียบรายเดือน ประจำ " + periodText;
        }}

        // 3. Ledger Table Rendering with Dynamic Sorting & Wallet Display
        function renderLedgerTable() {{
            const filteredData = getFilteredData();
            const typeFilter = document.getElementById('ledger-type-filter').value;
            const walletFilter = document.getElementById('ledger-wallet-filter').value;
            const query = document.getElementById('search-input').value.trim().toLowerCase();

            let displayData = filteredData.filter(t => {{
                if (typeFilter !== 'all' && t.type !== typeFilter) return false;
                if (walletFilter !== 'all' && t.walletId !== walletFilter) return false;
                if (query) {{
                    const matchItem = t.item.toLowerCase().includes(query);
                    const matchDoc = (t.doc || '').toLowerCase().includes(query);
                    const matchCat = (t.categoryName || '').toLowerCase().includes(query);
                    const w = wallets.find(x => x.id === t.walletId);
                    const matchWallet = w ? w.name.toLowerCase().includes(query) : false;
                    if (!matchItem && !matchDoc && !matchCat && !matchWallet) return false;
                }}
                return true;
            }});

            displayData.sort((a, b) => {{
                let valA = a[currentSortColumn];
                let valB = b[currentSortColumn];

                if (currentSortColumn === 'category') {{
                    valA = a.categoryName || a.category;
                    valB = b.categoryName || b.category;
                }}

                if (currentSortColumn === 'amount') {{
                    return currentSortDirection === 'asc' ? valA - valB : valB - valA;
                }}

                valA = (valA || '').toString();
                valB = (valB || '').toString();

                const cmp = valA.localeCompare(valB, 'th-TH', {{ sensitivity: 'base', numeric: true }});
                return currentSortDirection === 'asc' ? cmp : -cmp;
            }});

            document.getElementById('ledger-count').textContent = `แสดง ${{displayData.length}} รายการ (จากทั้งหมด ${{filteredData.length}} รายการ)`;

            const tbody = document.getElementById('ledger-table-body');
            tbody.innerHTML = '';

            if (displayData.length === 0) {{
                tbody.innerHTML = `
                    <tr>
                        <td colspan="8" class="py-12 text-center text-slate-400">
                            <i class="fas fa-folder-open text-4xl mb-3 block text-slate-300"></i>
                            ยังไม่มีรายการในระบบ (พร้อมบันทึกรายการใหม่ในตารางด้านบน)
                        </td>
                    </tr>
                `;
                return;
            }}

            displayData.forEach(t => {{
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-50 transition-colors";

                const isIncome = t.type === 'income';
                const typeBadge = isIncome
                    ? `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-emerald-100 text-emerald-800"><i class="fas fa-arrow-down text-[10px]"></i> รายรับ</span>`
                    : `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-rose-100 text-rose-800"><i class="fas fa-arrow-up text-[10px]"></i> รายจ่าย</span>`;

                const amountClass = isIncome ? 'text-emerald-600 font-bold' : 'text-rose-600 font-bold';
                const sign = isIncome ? '+' : '-';

                const w = wallets.find(x => x.id === t.walletId);
                const wBadge = w 
                    ? `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-xs font-medium bg-slate-100 text-slate-700"><i class="${{w.type==='cash'?'fas fa-money-bill-wave text-emerald-600':(w.type==='bank'?'fas fa-building-columns text-blue-600':'fas fa-wallet text-amber-500')}} text-[10px]"></i> ${{w.name}}</span>` 
                    : `<span class="text-slate-400 text-xs">เงินสดหน้าร้าน</span>`;

                tr.innerHTML = `
                    <td class="py-3 px-4 text-slate-600 whitespace-nowrap font-medium text-xs sm:text-sm">${{formatThaiDate(t.date)}}</td>
                    <td class="py-3 px-4 whitespace-nowrap">${{typeBadge}}</td>
                    <td class="py-3 px-4 text-slate-500 text-xs sm:text-sm whitespace-nowrap">${{t.categoryName || t.category}}</td>
                    <td class="py-3 px-4 whitespace-nowrap">${{wBadge}}</td>
                    <td class="py-3 px-4 text-slate-900 font-medium">${{t.item}}</td>
                    <td class="py-3 px-4 text-slate-400 text-xs">${{t.doc || '-'}}</td>
                    <td class="py-3 px-4 text-right ${{amountClass}} whitespace-nowrap text-sm sm:text-base">${{sign}} ${{formatCurrency(t.amount)}}</td>
                    <td class="py-3 px-4 text-center whitespace-nowrap">
                        <button onclick="openEditModal(${{t.id}})" class="w-8 h-8 rounded-lg text-slate-400 hover:bg-amber-100 hover:text-amber-600 transition-all mr-1" title="แก้ไข">
                            <i class="fas fa-pen text-xs"></i>
                        </button>
                        <button onclick="openDeleteModal(${{t.id}})" class="w-8 h-8 rounded-lg text-slate-400 hover:bg-rose-100 hover:text-rose-600 transition-all" title="ลบ">
                            <i class="fas fa-trash-alt text-xs"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // 4. Render Fully Dynamic Grouped Bar Chart with Exact Amounts Above Each Bar
        function renderCharts() {{
            // Dynamically collect unique YYYY-MM months from transactions
            const monthSet = new Set();
            transactions.forEach(t => {{
                if (t.date && t.date.length >= 7) {{
                    monthSet.add(t.date.substring(0, 7));
                }}
            }});

            let months = Array.from(monthSet).sort();
            if (months.length === 0) {{
                months = [getTodayStr().substring(0, 7)];
            }}

            const labels = months.map(ym => getMonthLabel(ym, true));

            const incData = new Array(months.length).fill(0);
            const expData = new Array(months.length).fill(0);
            const profitData = new Array(months.length).fill(0);

            transactions.forEach(t => {{
                const ym = t.date ? t.date.substring(0, 7) : '';
                const idx = months.indexOf(ym);
                if (idx !== -1) {{
                    if (t.type === 'income') incData[idx] += t.amount;
                    else if (t.type === 'expense') expData[idx] += t.amount;
                }}
            }});

            for (let i = 0; i < months.length; i++) {{
                profitData[i] = incData[i] - expData[i];
            }}

            // Custom Plugin to Render Currency Amounts Above Every Bar
            const barValueLabelsPlugin = {{
                id: 'barValueLabels',
                afterDatasetsDraw(chart) {{
                    const {{ ctx }} = chart;
                    chart.data.datasets.forEach((dataset, datasetIndex) => {{
                        const meta = chart.getDatasetMeta(datasetIndex);
                        meta.data.forEach((bar, index) => {{
                            const val = dataset.data[index];
                            if (val !== undefined && val !== null && val !== 0) {{
                                ctx.save();
                                ctx.font = 'bold 9px Prompt, sans-serif';
                                ctx.fillStyle = '#0f172a';
                                ctx.textAlign = 'center';
                                const formatted = (val >= 0 ? '฿' : '-฿') + Math.abs(val).toLocaleString('th-TH', {{ maximumFractionDigits: 0 }});
                                const yPos = val >= 0 ? bar.y - 4 : bar.y + 12;
                                ctx.textBaseline = val >= 0 ? 'bottom' : 'top';
                                ctx.fillText(formatted, bar.x, yPos);
                                ctx.restore();
                            }}
                        }});
                    }});
                }}
            }};

            const ctxBar = document.getElementById('monthlyBarChart').getContext('2d');
            if (monthlyChartInstance) monthlyChartInstance.destroy();

            monthlyChartInstance = new Chart(ctxBar, {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: [
                        {{
                            label: 'รายรับ (Income)',
                            data: incData,
                            backgroundColor: '#10b981',
                            borderRadius: 6
                        }},
                        {{
                            label: 'รายจ่าย (Expenses)',
                            data: expData,
                            backgroundColor: '#f43f5e',
                            borderRadius: 6
                        }},
                        {{
                            label: 'กำไร/ขาดทุนสุทธิ (Net Profit)',
                            data: profitData,
                            backgroundColor: '#6366f1',
                            borderRadius: 6
                        }}
                    ]
                }},
                plugins: [barValueLabelsPlugin],
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    layout: {{
                        padding: {{
                            top: 20
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            position: 'top',
                            labels: {{
                                font: {{ family: 'Prompt', size: 12, weight: '500' }},
                                padding: 15
                            }}
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    let label = context.dataset.label || '';
                                    if (label) label += ': ';
                                    if (context.parsed.y !== null) {{
                                        label += '฿' + context.parsed.y.toLocaleString('th-TH', {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
                                    }}
                                    return label;
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            ticks: {{
                                font: {{ family: 'Prompt', size: 11 }},
                                callback: val => '฿' + (val / 1000).toFixed(0) + 'k'
                            }},
                            grid: {{ color: '#f1f5f9' }}
                        }},
                        x: {{
                            ticks: {{ font: {{ family: 'Prompt', size: 11, weight: '600' }} }},
                            grid: {{ display: false }}
                        }}
                    }}
                }}
            }});

            const expCategories = {{
                exp_mall: 0,
                exp_market: 0,
                exp_wages: 0,
                exp_utilities: 0,
                exp_other: 0
            }};

            const filteredData = getFilteredData();
            filteredData.forEach(t => {{
                if (t.type === 'expense' && expCategories[t.category] !== undefined) {{
                    expCategories[t.category] += t.amount;
                }}
            }});

            const ctxPie = document.getElementById('expenseDoughnutChart').getContext('2d');
            if (expenseChartInstance) expenseChartInstance.destroy();

            expenseChartInstance = new Chart(ctxPie, {{
                type: 'doughnut',
                data: {{
                    labels: ['ซื้อจากห้าง', 'ซื้อจากตลาด/ร้านค้าส่ง', 'ค่าแรง', 'สาธารณูปโภค', 'อื่นๆ'],
                    datasets: [{{
                        data: [
                            expCategories.exp_mall,
                            expCategories.exp_market,
                            expCategories.exp_wages,
                            expCategories.exp_utilities,
                            expCategories.exp_other
                        ],
                        backgroundColor: ['#e11d48', '#f97316', '#eab308', '#06b6d4', '#64748b']
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ font: {{ family: 'Prompt', size: 11 }} }} }}
                    }}
                }}
            }});
        }}

        // Edit Modal Operations
        function openEditModal(id) {{
            const t = transactions.find(x => x.id === id);
            if (!t) return;

            populateWalletSelectors();
            document.getElementById('edit-id').value = t.id;
            document.getElementById('edit-date').value = t.date;
            document.getElementById('edit-type').value = t.type;
            document.getElementById('edit-wallet').value = t.walletId || (wallets[0] ? wallets[0].id : 'w_cash');
            updateEditCategoryOptions();
            document.getElementById('edit-category').value = t.category;
            document.getElementById('edit-item').value = t.item;
            document.getElementById('edit-amount').value = t.amount;
            document.getElementById('edit-doc').value = t.doc || '';

            document.getElementById('edit-modal').classList.remove('hidden');
        }}

        function updateEditCategoryOptions() {{
            const type = document.getElementById('edit-type').value;
            const select = document.getElementById('edit-category');
            select.innerHTML = '';
            
            Object.entries(categoryDefs[type]).forEach(([key, val]) => {{
                const opt = document.createElement('option');
                opt.value = key;
                opt.textContent = val;
                select.appendChild(opt);
            }});
        }}

        function closeEditModal() {{
            document.getElementById('edit-modal').classList.add('hidden');
        }}

        function handleEditSubmit(e) {{
            e.preventDefault();
            const id = parseInt(document.getElementById('edit-id').value);
            const index = transactions.findIndex(x => x.id === id);
            if (index === -1) return;

            const date = document.getElementById('edit-date').value;
            const type = document.getElementById('edit-type').value;
            const walletId = document.getElementById('edit-wallet').value;
            const category = document.getElementById('edit-category').value;
            const item = document.getElementById('edit-item').value.trim();
            const amount = parseFloat(document.getElementById('edit-amount').value);
            const doc = document.getElementById('edit-doc').value.trim();

            transactions[index] = {{
                id,
                date,
                type,
                walletId,
                category,
                categoryName: categoryDefs[type][category] || category,
                item,
                amount,
                doc
            }};

            saveTransactions();
            closeEditModal();
            updateAllViews();
            showToast('แก้ไขรายการเรียบร้อยแล้ว', 'success');
        }}

        // Delete Modal Operations
        function openDeleteModal(id) {{
            deleteTargetId = id;
            document.getElementById('delete-modal').classList.remove('hidden');
        }}

        function closeDeleteModal() {{
            deleteTargetId = null;
            document.getElementById('delete-modal').classList.add('hidden');
        }}

        document.getElementById('confirm-delete-btn').addEventListener('click', () => {{
            if (deleteTargetId !== null) {{
                transactions = transactions.filter(x => x.id !== deleteTargetId);
                saveTransactions();
                closeDeleteModal();
                updateAllViews();
                showToast('ลบรายการเรียบร้อยแล้ว', 'success');
            }}
        }});

        // Print & Report Generation (KPI Dashboard + Continuous Flow + Dynamic Spaced Doughnut Chart Switch)
        function populatePrintReportData() {{
            const filteredData = getFilteredData();
            
            let periodText = "ทั้งหมด";
            if (currentMonthFilter === 'today') periodText = "ประจำวันที่ " + formatThaiDate(getTodayStr());
            else if (currentMonthFilter === 'custom') {{
                periodText = "ระหว่างวันที่ " + (customStartDate ? formatThaiDate(customStartDate) : 'เริ่มต้น') + " ถึง " + (customEndDate ? formatThaiDate(customEndDate) : 'ปัจจุบัน');
            }} else if (currentMonthFilter !== 'all') {{
                periodText = "ประจำเดือน " + getMonthLabel(currentMonthFilter, true);
            }}

            document.getElementById('print-header-period').textContent = periodText;

            // 1. Calculate KPI Dashboard Summary for Print Area
            let totalInc = 0;
            let totalExp = 0;

            filteredData.forEach(t => {{
                if (t.type === 'income') totalInc += t.amount;
                else if (t.type === 'expense') totalExp += t.amount;
            }});

            const netProf = totalInc - totalExp;

            document.getElementById('print-kpi-income').textContent = formatCurrency(totalInc);
            document.getElementById('print-kpi-expense').textContent = formatCurrency(totalExp);
            document.getElementById('print-kpi-profit').textContent = formatCurrency(netProf);

            const profitBox = document.getElementById('print-kpi-profit-box');
            if (netProf >= 0) {{
                profitBox.className = "text-center p-2 bg-indigo-50 border border-indigo-300 rounded-lg";
            }} else {{
                profitBox.className = "text-center p-2 bg-amber-50 border border-amber-300 rounded-lg";
            }}

            // 2. Detailed Monthly Income Statement Matrix for Print
            const {{ months, mData }} = generateMonthlyPnLMatrix(filteredData);

            let headHtml = `<tr class="bg-slate-100 text-slate-800 border-b border-slate-800">
                <th class="p-1.5 text-left border-r border-slate-800">หมวดหมู่รายการ (Accounting Category)</th>`;
            
            months.forEach(m => {{
                headHtml += `<th class="p-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{getMonthLabel(m)}}</th>`;
            }});

            headHtml += `<th class="p-1.5 text-right border-r border-slate-800 whitespace-nowrap">รวมทั้งสิ้น (บาท)</th>
                <th class="p-1.5 text-right w-20 whitespace-nowrap">สัดส่วน (%)</th>
            </tr>`;

            document.getElementById('print-pnl-head').innerHTML = headHtml;

            let grandRev = 0, grandCOGS = 0, grandGross = 0, grandOpex = 0, grandNet = 0;
            const totals = {{
                revShop: 0, revOther: 0,
                cogsMall: 0, cogsMarket: 0,
                opexWages: 0, opexUtil: 0, opexOther: 0
            }};

            months.forEach(m => {{
                Object.keys(totals).forEach(k => {{
                    totals[k] += mData[m][k];
                }});
            }});

            grandRev = totals.revShop + totals.revOther;
            grandCOGS = totals.cogsMall + totals.cogsMarket;
            grandGross = grandRev - grandCOGS;
            grandOpex = totals.opexWages + totals.opexUtil + totals.opexOther;
            grandNet = grandGross - grandOpex;

            const getPct = val => grandRev > 0 ? ((val / grandRev) * 100).toFixed(2) + '%' : '0.00%';

            let bodyHtml = `
                <tr class="bg-emerald-50/70 font-bold border-b border-slate-300 text-emerald-900">
                    <td class="p-1.5 border-r border-slate-800">1. รายรับจากการขายสินค้า (Revenue from Sales)</td>`;
            months.forEach(m => {{
                const rM = mData[m].revShop + mData[m].revOther;
                bodyHtml += `<td class="p-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(rM)}}</td>`;
            }});
            bodyHtml += `<td class="p-1.5 text-right border-r border-slate-800 font-bold whitespace-nowrap">${{formatCurrency(grandRev)}}</td>
                    <td class="p-1.5 text-right font-bold">100.00%</td>
                </tr>
                <tr class="text-slate-800">
                    <td class="py-1 pl-4 pr-1 border-r border-slate-800">• รายรับขายสินค้าหน้าร้าน / ในโปรแกรม (POS)</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(mData[m].revShop)}}</td>`;
            }});
            bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(totals.revShop)}}</td>
                    <td class="py-1 px-1.5 text-right text-slate-600">${{getPct(totals.revShop)}}</td>
                </tr>
                <tr class="text-slate-800 border-b border-slate-300">
                    <td class="py-1 pl-4 pr-1 border-r border-slate-800">• รายรับขายสินค้าตามสมุด / อื่นๆ</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(mData[m].revOther)}}</td>`;
            }});
            bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(totals.revOther)}}</td>
                    <td class="py-1 px-1.5 text-right text-slate-600">${{getPct(totals.revOther)}}</td>
                </tr>

                <tr class="bg-rose-50/70 font-bold border-b border-slate-300 text-rose-900">
                    <td class="p-1.5 border-r border-slate-800">2. หัก: ต้นทุนขายสินค้า (Cost of Goods Sold - COGS)</td>`;
            months.forEach(m => {{
                const cM = mData[m].cogsMall + mData[m].cogsMarket;
                bodyHtml += `<td class="p-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(cM)}}</td>`;
            }});
            bodyHtml += `<td class="p-1.5 text-right border-r border-slate-800 font-bold whitespace-nowrap">${{formatCurrency(grandCOGS)}}</td>
                    <td class="p-1.5 text-right font-bold">${{getPct(grandCOGS)}}</td>
                </tr>
                <tr class="text-slate-800">
                    <td class="py-1 pl-4 pr-1 border-r border-slate-800">• ซื้อสินค้าจากห้าง (Makro / Lotus / Big C)</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(mData[m].cogsMall)}}</td>`;
            }});
            bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(totals.cogsMall)}}</td>
                    <td class="py-1 px-1.5 text-right text-slate-600">${{getPct(totals.cogsMall)}}</td>
                </tr>
                <tr class="text-slate-800 border-b border-slate-300">
                    <td class="py-1 pl-4 pr-1 border-r border-slate-800">• ซื้อสินค้าจากตลาด / ร้านค้าส่ง</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(mData[m].cogsMarket)}}</td>`;
            }});
            bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(totals.cogsMarket)}}</td>
                    <td class="py-1 px-1.5 text-right text-slate-600">${{getPct(totals.cogsMarket)}}</td>
                </tr>

                <tr class="bg-slate-100 font-bold border-t-2 border-b-2 border-slate-400 text-slate-900">
                    <td class="p-1.5 border-r border-slate-800">เท่ากับ: กำไรขั้นต้น (Gross Profit)</td>`;
            months.forEach(m => {{
                const gM = (mData[m].revShop + mData[m].revOther) - (mData[m].cogsMall + mData[m].cogsMarket);
                bodyHtml += `<td class="p-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(gM)}}</td>`;
            }});
            bodyHtml += `<td class="p-1.5 text-right border-r border-slate-800 font-bold text-slate-900 whitespace-nowrap">${{formatCurrency(grandGross)}}</td>
                    <td class="p-1.5 text-right font-bold text-slate-800">${{getPct(grandGross)}}</td>
                </tr>

                <tr class="bg-amber-50/70 font-bold border-b border-slate-300 text-amber-900">
                    <td class="p-1.5 border-r border-slate-800">3. หัก: ค่าใช้จ่ายในการดำเนินงาน (Operating Expenses)</td>`;
            months.forEach(m => {{
                const oM = mData[m].opexWages + mData[m].opexUtil + mData[m].opexOther;
                bodyHtml += `<td class="p-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(oM)}}</td>`;
            }});
            bodyHtml += `<td class="p-1.5 text-right border-r border-slate-800 font-bold whitespace-nowrap">${{formatCurrency(grandOpex)}}</td>
                    <td class="p-1.5 text-right font-bold">${{getPct(grandOpex)}}</td>
                </tr>
                <tr class="text-slate-800">
                    <td class="py-1 pl-4 pr-1 border-r border-slate-800">• ค่าแรง</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(mData[m].opexWages)}}</td>`;
            }});
            bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(totals.opexWages)}}</td>
                    <td class="py-1 px-1.5 text-right text-slate-600">${{getPct(totals.opexWages)}}</td>
                </tr>
                <tr class="text-slate-800">
                    <td class="py-1 pl-4 pr-1 border-r border-slate-800">• สาธารณูปโภค (ค่าน้ำ/ไฟ/เน็ต)</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(mData[m].opexUtil)}}</td>`;
            }});
            bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(totals.opexUtil)}}</td>
                    <td class="py-1 px-1.5 text-right text-slate-600">${{getPct(totals.opexUtil)}}</td>
                </tr>
                <tr class="text-slate-800 border-b border-slate-300">
                    <td class="py-1 pl-4 pr-1 border-r border-slate-800">• ค่าใช้จ่ายอื่นๆ (อุปกรณ์/วัสดุสำนักงาน)</td>`;
            months.forEach(m => {{
                bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(mData[m].opexOther)}}</td>`;
            }});
            bodyHtml += `<td class="py-1 px-1.5 text-right border-r border-slate-800 whitespace-nowrap">${{formatCurrency(totals.opexOther)}}</td>
                    <td class="py-1 px-1.5 text-right text-slate-600">${{getPct(totals.opexOther)}}</td>
                </tr>

                <tr class="bg-emerald-100/90 font-black border-t-2 border-b-2 border-slate-400 text-xs sm:text-sm">
                    <td class="p-2 border-r border-slate-800">เท่ากับ: กำไร (ขาดทุน) สุทธิ (Net Profit / Loss)</td>`;
            months.forEach(m => {{
                const rM = mData[m].revShop + mData[m].revOther;
                const cM = mData[m].cogsMall + mData[m].cogsMarket;
                const oM = mData[m].opexWages + mData[m].opexUtil + mData[m].opexOther;
                const netM = (rM - cM) - oM;
                bodyHtml += `<td class="p-2 text-right border-r border-slate-800 font-bold whitespace-nowrap">${{formatCurrency(netM)}}</td>`;
            }});
            bodyHtml += `<td class="p-2 text-right border-r border-slate-800 font-black text-emerald-900 whitespace-nowrap">${{formatCurrency(grandNet)}}</td>
                    <td class="p-2 text-right font-black text-emerald-900">${{getPct(grandNet)}}</td>
                </tr>
            `;
            document.getElementById('print-pnl-body').innerHTML = bodyHtml;

            // 3. Render Dynamic Chart Image (Spaced Doughnut Chart for Single Month vs Grouped Bar Chart for All Months)
            const printChartTitle = document.getElementById('print-chart-title');
            const printChartImg = document.getElementById('print-chart-img');

            if (currentMonthFilter !== 'all') {{
                printChartTitle.textContent = 'แผนภูมิสรุปสัดส่วน รายรับ - รายจ่าย - กำไรสุทธิ ประจำช่วงเวลา (Doughnut Chart)';
                
                const canvas = document.createElement('canvas');
                canvas.width = 520;
                canvas.height = 260;
                const ctx = canvas.getContext('2d');

                const doughnutLabels = [
                    `รายรับ (฿${{totalInc.toLocaleString('th-TH', {{maximumFractionDigits: 0}})}})`,
                    `รายจ่าย (฿${{totalExp.toLocaleString('th-TH', {{maximumFractionDigits: 0}})}})`,
                    `${{netProf >= 0 ? 'กำไรสุทธิ' : 'ขาดทุนสุทธิ'}} (฿${{Math.abs(netProf).toLocaleString('th-TH', {{maximumFractionDigits: 0}})}})`
                ];

                const singleDoughnutChart = new Chart(ctx, {{
                    type: 'doughnut',
                    data: {{
                        labels: doughnutLabels,
                        datasets: [{{
                            data: [totalInc, totalExp, Math.abs(netProf)],
                            backgroundColor: ['#10b981', '#f43f5e', netProf >= 0 ? '#6366f1' : '#d97706'],
                            borderWidth: 3,
                            borderColor: '#ffffff',
                            spacing: 6,
                            offset: 6
                        }}]
                    }},
                    options: {{
                        responsive: false,
                        animation: false,
                        cutout: '55%',
                        plugins: {{
                            legend: {{
                                position: 'right',
                                labels: {{
                                    font: {{ family: 'Prompt', size: 12, weight: '600' }},
                                    padding: 18,
                                    usePointStyle: true,
                                    pointStyle: 'circle'
                                }}
                            }}
                        }}
                    }}
                }});

                printChartImg.src = singleDoughnutChart.toBase64Image();
                singleDoughnutChart.destroy();
            }} else {{
                printChartTitle.textContent = 'แผนภูมิเปรียบเทียบ รายรับ - รายจ่าย - กำไรสุทธิ แต่ละเดือน (Grouped Bar Chart)';
                if (monthlyChartInstance) {{
                    printChartImg.src = monthlyChartInstance.toBase64Image();
                }}
            }}

            // 4. Clean Transaction Ledger for Print (Unnumbered Title - Flows continuously)
            const sorted = [...filteredData].sort((a,b) => new Date(a.date) - new Date(b.date));
            let ledgerHtml = '';
            if (sorted.length === 0) {{
                ledgerHtml = `<tr><td colspan="5" class="p-4 text-center text-slate-500">ไม่มีรายการในช่วงเวลานี้</td></tr>`;
            }} else {{
                sorted.forEach(t => {{
                    const typeText = t.type === 'income' ? 'รายรับ' : 'รายจ่าย';
                    const sign = t.type === 'income' ? '+' : '-';
                    
                    let cleanCat = t.categoryName || t.category;
                    if (cleanCat.includes('ซื้อจากห้าง')) cleanCat = 'ซื้อจากห้าง';
                    else if (cleanCat.includes('ซื้อจากตลาด')) cleanCat = 'ซื้อจากตลาด/ร้านค้าส่ง';
                    else if (cleanCat.includes('ขายสินค้าหน้าร้าน')) cleanCat = 'ขายสินค้าหน้าร้าน';
                    else if (cleanCat.includes('ขายสินค้าตามสมุด')) cleanCat = 'ขายสินค้าตามสมุด';

                    ledgerHtml += `
                        <tr class="border-b border-slate-400">
                            <td class="p-1.5 text-center border-r border-slate-800 nowrap-cell whitespace-nowrap">${{formatThaiDate(t.date)}}</td>
                            <td class="p-1.5 border-r border-slate-800 nowrap-cell whitespace-nowrap">${{typeText}}</td>
                            <td class="p-1.5 border-r border-slate-800 nowrap-cell whitespace-nowrap">${{cleanCat}}</td>
                            <td class="p-1.5 border-r border-slate-800">${{t.item}}</td>
                            <td class="p-1.5 text-right font-semibold nowrap-cell whitespace-nowrap">${{sign}} ${{formatCurrency(t.amount)}}</td>
                        </tr>
                    `;
                }});
            }}
            document.getElementById('print-ledger-body').innerHTML = ledgerHtml;
        }}

        function openPrintModal() {{
            populatePrintReportData();
            document.getElementById('print-modal').classList.remove('hidden');
        }}

        function closePrintModal() {{
            document.getElementById('print-modal').classList.add('hidden');
        }}

        function triggerPrint() {{
            populatePrintReportData();
            window.print();
        }}

        // Helper Formatters
        function formatCurrency(val) {{
            return '฿' + val.toLocaleString('th-TH', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
        }}

        function formatThaiDate(dateStr) {{
            if (!dateStr) return '';
            const parts = dateStr.split('-');
            if (parts.length !== 3) return dateStr;
            
            const year = parseInt(parts[0]) + 543;
            const monthNames = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
            const month = monthNames[parseInt(parts[1]) - 1];
            const day = parseInt(parts[2]);

            return `${{day}} ${{month}} ${{year}}`;
        }}

        // Toast Handler
        function showToast(msg, type = 'success') {{
            const toast = document.getElementById('toast');
            const icon = document.getElementById('toast-icon');
            const message = document.getElementById('toast-message');

            message.textContent = msg;
            if (type === 'success') {{
                icon.className = "fas fa-circle-check text-emerald-400 text-lg";
            }} else if (type === 'info') {{
                icon.className = "fas fa-circle-info text-blue-400 text-lg";
            }} else {{
                icon.className = "fas fa-circle-exclamation text-rose-400 text-lg";
            }}

            toast.classList.remove('opacity-0', 'translate-y-4', 'pointer-events-none');
            
            setTimeout(() => {{
                toast.classList.add('opacity-0', 'translate-y-4', 'pointer-events-none');
            }}, 3000);
        }}
    </script>
</body>
</html>
'''

with open('รายรับรายจ่าย.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Generated รายรับรายจ่าย.html with Dynamic Month Preset Buttons successfully!')
