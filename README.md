# Order NP - ระบบสั่งของสหกรณ์โรงเรียนบ้านน้ำพร (PWA on Vercel & GitHub)

ระบบแอปพลิเคชันบริหารจัดการและสั่งสินค้าสหกรณ์โรงเรียนบ้านน้ำพร เชื่อมโยงราคาส่งและข้อมูลสินค้าจาก **Makro Pro** พร้อมระบบบันทึกประวัติการทำงาน (Action History & Audit Logs) และซิงค์ข้อมูลบนคลาวด์ผ่าน **GitHub REST API** และ **Vercel Serverless Functions**

![ไอคอนแอปพลิเคชัน Order NP](icon-192.png)

---

## ✨ คุณสมบัติเด่น (Features)

1. **รองรับ PWA 100%**: ติดตั้งใช้งานบน iPhone (iOS) และ Android ได้เหมือนแอปจริง เปิดเต็มหน้าจอ ไม่มีแถบ URL
2. **ค้นหาและดึงข้อมูลจาก Makro Pro อัตโนมัติ**: ค้นหาด้วยชื่อสินค้า, รหัสสินค้า, หรือคัดลอกลิงก์ Makro Pro มาวาง ข้อมูลจะถูกกรอกลงฟอร์มทันทีใน 1 วินาที
3. **บันทึกประวัติการกระทำทั้งหมด (Action Logging & Audit Trail)**:
   - บันทึกทุกการกระทำ: เพิ่มสินค้าใหม่, แก้ไขราคา, ลบสินค้า, บันทึกการสั่งซื้อ
   - ซิงค์ขึ้น GitHub อัตโนมัติ ทำให้ข้อมูลตรงกันทุกเครื่อง (คอมพิวเตอร์, iPhone, iPad)
   - มีหน้าต่างเปิดดู Timeline ประวัติย้อนหลังได้ตลอดเวลา
4. **โฮสต์และทำงานบน Vercel**:
   - เชื่อมต่อกับ GitHub อัปเดตและ Deploy อัตโนมัติ
   - Vercel Serverless Functions (`/api/makro-search`, `/api/record-action`, `/api/get-data`) ทำงานรวดเร็ว ปลอดภัย ไม่ติดปัญหา CORS
5. **ใช้งานแบบ Offline-First**: แม้ไม่มีสัญญาณอินเทอร์เน็ต ก็สามารถเปิดดูสินค้า จัดตะกร้า และสั่งของได้ เมื่อต่อเน็ตระบบจะซิงค์ให้อัตโนมัติ

---

## 🚀 วิธีการนำขึ้น Vercel (Deploy to Vercel)

### ขั้นตอนที่ 1: นำโค้ดขึ้น GitHub
1. สร้าง Repository ใหม่บน [GitHub.com](https://github.com/new) ชื่อ `order-np`
2. รันคำสั่งส่งโค้ดขึ้น GitHub:
   ```bash
   git remote add origin https://github.com/boasnirut/order-np.git
   git branch -M main
   git push -u origin main
   ```

### ขั้นตอนที่ 2: เชื่อมต่อและ Deploy บน Vercel
1. เข้าเว็บไซต์ [vercel.com](https://vercel.com) แล้วเข้าสู่ระบบด้วย GitHub
2. กดปุ่ม **"Add New..."** $\rightarrow$ เลือก **"Project"**
3. เลือก Repository `order-np` แล้วกด **"Import"**
4. (แนะนำ) ในส่วน **Environment Variables** เพิ่มตัวแปรดังนี้:
   - `GITHUB_TOKEN`: GitHub Personal Access Token (ที่มีสิทธิ์ repo)
   - `GITHUB_OWNER`: `boasnirut`
   - `GITHUB_REPO`: `order-np`
5. กดปุ่ม **"Deploy"** รอประมาณ 1 นาที จะได้ลิงก์ เช่น `https://order-np.vercel.app`

---

## 📱 วิธีติดตั้งบนโทรศัพท์มือถือ (iPhone & Android)

- **iPhone (Safari)**: เปิดลิงก์ Vercel $\rightarrow$ แตะปุ่มแชร์ ⎋ $\rightarrow$ เลือก **"เพิ่มไปยังหน้าจอโฮม" (Add to Home Screen)**
- **Android (Chrome)**: เปิดลิงก์ Vercel $\rightarrow$ แตะเมนูจุด 3 จุด $\rightarrow$ เลือก **"ติดตั้งแอปพลิเคชัน" (Install App)**

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

- `index.html` - หน้าหลักของแอปพลิเคชัน (PWA)
- `activity_logs.json` - ฐานข้อมูลประวัติการทำงานทั้งหมด (Action History)
- `makro_products.json` - ฐานข้อมูลรายการสินค้าของสหกรณ์โรงเรียน
- `manifest.json` & `sw.js` - การตั้งค่า Progressive Web App และ Cache (v7)
- `vercel.json` - การตั้งค่าการรันบน Vercel
- `api/` - Vercel Serverless Functions:
  - `makro-search.js` - ค้นหาและดึงข้อมูลจาก Makro Pro
  - `record-action.js` - บันทึกประวัติและ Commit ข้อมูลขึ้น GitHub
  - `get-data.js` - ดึงประวัติและข้อมูลสินค้าล่าสุด
