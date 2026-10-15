# 🛡️ TrustLine / NPRU Sentinel — E2E Test Suite

ชุดทดสอบ End-to-End อัตโนมัติด้วย **Selenium + pytest** สำหรับระบบรับแจ้งเบาะแสและจัดการเรื่องร้องเรียนลับ  
มหาวิทยาลัยราชภัฏนครปฐม (Nakhon Pathom Rajabhat University)

---

## 👥 สมาชิกกลุ่มและความรับผิดชอบ

| ชื่อ | โฟลเดอร์ | Test Cases | โมดูล |
|------|----------|-----------|-------|
| **วัชรากร** | `tests/watcharakorn/` | TC-001 – TC-030 | FR-SUB, FR-AI |
| **วุฒิชัย** | `tests/wuttichai/` | TC-031 – TC-053 | FR-TRK, FR-CAS |
| **สหรัฐ** | `tests/saharat/` | TC-054 – TC-063 | FR-ANA, FR-SEC |
| **อธิป** | `tests/athip/` | TC-064 – TC-068 | FR-SYS |

---

## 📁 โครงสร้างโปรเจกต์

```
group/
├── pytest.ini                           # ค่าคอนฟิก pytest และ markers
├── requirements.txt                     # Python dependencies
├── README.md                            # ไฟล์นี้
│
├── docs/
│   ├── Annonymous-Test-Cases.docx       # เอกสาร Test Case Specification (68 TCs)
│   └── Annonymous-Test-Plan-and-Report.docx # แผนการทดสอบและรายงานผล
│
└── tests/
    ├── conftest.py                      # Fixtures ร่วม (driver, config, base_url)
    │
    ├── pages/                           # Page Object Model
    │   ├── base_page.py                 # Base class สำหรับทุก Page
    │   ├── report_page.py               # หน้าส่งรายงาน
    │   ├── tracking_page.py             # หน้าติดตามสถานะ
    │   ├── admin_page.py                # หน้า Admin Dashboard
    │   └── login_page.py                # หน้า Login
    │
    ├── watcharakorn/                    # วัชรากร — TC-001 to TC-030
    │   ├── test_TC001_016_submission.py # FR-SUB: การส่งรายงานเบาะแสลับ
    │   ├── test_TC017_urgency_lock.py   # FR-SUB: ล็อกระดับความเร่งด่วน
    │   └── test_TC018_030_ai_analysis.py# FR-AI: วิเคราะห์ด้วย Gemini AI
    │
    ├── wuttichai/                       # วุฒิชัย — TC-031 to TC-053
    │   ├── test_TC031_038_tracking_chat.py    # FR-TRK: ติดตามสถานะ + แชทลับ
    │   └── test_TC039_053_case_management.py  # FR-CAS: จัดการสำนวนคดี
    │
    ├── saharat/                         # สหรัฐ — TC-054 to TC-063
    │   ├── test_TC054_057_analytics.py  # FR-ANA: Dashboard สถิติ
    │   └── test_TC058_063_security.py   # FR-SEC: Authentication & Security
    │
    └── athip/                           # อธิป — TC-064 to TC-068
        └── test_TC064_068_system.py     # FR-SYS: โครงสร้างพื้นฐาน & Real-time
```

---

## ⚙️ การติดตั้ง

### ความต้องการเบื้องต้น

- Python 3.9+
- Google Chrome (แนะนำเวอร์ชันล่าสุด) หรือ Firefox / Edge
- ระบบ TrustLine รันอยู่ที่ `http://localhost:3000` (หรือ URL ที่กำหนด)

### ขั้นตอนติดตั้ง

```bash
# 1. Clone หรือเปิดโฟลเดอร์โปรเจกต์
cd "test case/group"

# 2. สร้าง virtual environment (แนะนำ)
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

# 3. ติดตั้ง dependencies
pip install -r requirements.txt
```

> ChromeDriver จะถูกดาวน์โหลดอัตโนมัติผ่าน `webdriver-manager` ไม่ต้องติดตั้งเพิ่ม

---

## 🚀 การรันทดสอบ

### รันทั้งหมด

```bash
python -m pytest tests/
```

### รันเฉพาะสมาชิก

```bash
# วัชรากร (TC-001 to TC-030)
python -m pytest tests/watcharakorn/

# วุฒิชัย (TC-031 to TC-053)
python -m pytest tests/wuttichai/

# สหรัฐ (TC-054 to TC-063)
python -m pytest tests/saharat/

# อธิป (TC-064 to TC-068)
python -m pytest tests/athip/
```

### รันด้วย Marker (โมดูล / TC เดี่ยว)

```bash
# รันตามโมดูล
python -m pytest -m fr_sub       # FR-SUB: การส่งรายงาน
python -m pytest -m fr_ai        # FR-AI: AI Analysis
python -m pytest -m fr_trk       # FR-TRK: Tracking & Chat
python -m pytest -m fr_cas       # FR-CAS: Case Management
python -m pytest -m fr_ana       # FR-ANA: Analytics
python -m pytest -m fr_sec       # FR-SEC: Security
python -m pytest -m fr_sys       # FR-SYS: System

# รัน TC เดี่ยว
python -m pytest -m tc012
python -m pytest -m "tc001 or tc002 or tc003"
```

### ตัวเลือกที่มีประโยชน์

```bash
# Headless mode (ไม่เปิดหน้าต่าง browser)
$env:HEADLESS="true"; python -m pytest tests/

# เปลี่ยน Browser
$env:BROWSER="firefox"; python -m pytest tests/
$env:BROWSER="edge";    python -m pytest tests/

# เปลี่ยน URL เป้าหมาย
$env:BASE_URL="http://localhost:3000"; python -m pytest tests/

# ออก HTML Report
python -m pytest tests/ --html=tests/reports/report.html --self-contained-html

# รันแบบ Parallel (เร็วขึ้น)
python -m pytest tests/ -n auto

# หยุดทันทีเมื่อ test แรก fail
python -m pytest tests/ -x

# แสดงผล print() ระหว่างรัน
python -m pytest tests/ -s
```

---

## 🔧 Environment Variables

| Variable | Default | คำอธิบาย |
|----------|---------|-----------|
| `BASE_URL` | `https://anonymous-report.ai.studio` | URL ของระบบที่ทดสอบ |
| `BROWSER` | `chrome` | Browser: `chrome`, `firefox`, `edge` |
| `HEADLESS` | `false` | รัน headless: `true` / `false` |
| `TIMEOUT` | `15` | Implicit wait timeout (วินาที) |
| `ADMIN_USERNAME` | `admin` | ชื่อผู้ใช้ admin |
| `ADMIN_PASSWORD` | `admin` | รหัสผ่าน admin |
| `OFFICER_USERNAME` | `officer1` | ชื่อผู้ใช้ investigator |
| `OFFICER_PASSWORD` | `officer1` | รหัสผ่าน investigator |
| `TEST_REPORT_ID` | `RPT-TEST-001` | Report ID จริงสำหรับ TC-031–033 |
| `TEST_PIN` | `1234` | PIN จริงสำหรับ TC-031–033 |

---

## 📋 ความครอบคลุม Test Cases

**รวม 68 TC / 118 Tests — ครอบคลุม 52 Functional Requirements**

| โมดูล | FR | TC | Tests | ผู้รับผิดชอบ |
|-------|----|----|-------|-------------|
| FR-SUB: การส่งรายงาน | FR-SUB-001–011 | TC-001–017 | 30 | วัชรากร |
| FR-AI: วิเคราะห์ด้วย AI | FR-AI-001–007 | TC-018–030 | 22 | วัชรากร |
| FR-TRK: ติดตามสถานะ + แชท | FR-TRK-001–006 | TC-031–038 | 11 | วุฒิชัย |
| FR-CAS: จัดการสำนวนคดี | FR-CAS-001–013 | TC-039–053 | 17 | วุฒิชัย |
| FR-ANA: Dashboard สถิติ | FR-ANA-001–004 | TC-054–057 | 8 | สหรัฐ |
| FR-SEC: ความปลอดภัย | FR-SEC-001–004 | TC-058–063 | 17 | สหรัฐ |
| FR-SYS: โครงสร้างพื้นฐาน | FR-SYS-001–004 | TC-064–068 | 13 | อธิป |
| **รวม** | **52 FR** | **68 TC** | **118** | |

- ✅ **Positive:** 55 TC — ทดสอบพฤติกรรมปกติ
- ❌ **Negative:** 13 TC — ทดสอบการป้องกัน/ปฏิเสธ

---

## 📐 สถาปัตยกรรม — Page Object Model

```
conftest.py
│  fixtures: driver, wait, base_url, config
│
└── pages/
    ├── BasePage          ← find(), click(), is_element_present(), open()
    ├── ReportPage        ← open_report_page(), set_description(), upload_file()
    ├── TrackingPage      ← open_tracking_tab(), track_report(), get_error_message()
    ├── AdminPage         ← open_dashboard(), click_case_row(), get_case_row_count()
    └── LoginPage         ← open_login(), login(), is_logged_in()
```

---

## 🗂️ เอกสารอ้างอิง

| เอกสาร | คำอธิบาย |
|--------|-----------|
| [`docs/Annonymous-Test-Cases.docx`](docs/Annonymous-Test-Cases.docx) | Test Case Specification (68 TC พร้อม Expected Results) |
| [`docs/Annonymous-Test-Plan-and-Report.docx`](docs/Annonymous-Test-Plan-and-Report.docx) | แผนการทดสอบ, เกณฑ์ผ่าน/ไม่ผ่าน, รายงานผล |
| [`pytest.ini`](pytest.ini) | ค่าคอนฟิก pytest, markers ทั้งหมด |
| [`requirements.txt`](requirements.txt) | Python packages ที่ต้องใช้ |

---

## ❓ คำถามที่พบบ่อย

**Q: ChromeDriver version ไม่ตรงกับ Chrome?**  
A: `webdriver-manager` จัดการให้อัตโนมัติ แต่ถ้ายังมีปัญหาให้รัน:
```bash
pip install --upgrade webdriver-manager
```

**Q: TC-031–033 skip เสมอ?**  
A: ต้องมี Report ID + PIN จริง ตั้งค่าผ่าน Environment Variable:
```bash
$env:TEST_REPORT_ID="RPT-XXXX-YYYY"; $env:TEST_PIN="1234"
```

**Q: รันในเครื่อง CI/CD (ไม่มีหน้าจอ)?**  
A: ใช้ headless mode:
```bash
$env:HEADLESS="true"; python -m pytest tests/
```

**Q: เพิ่ม Test Case ใหม่?**  
A: วางไฟล์ `test_*.py` ใน folder ของสมาชิก แล้วเพิ่ม marker ใหม่ใน `pytest.ini`

---

<div align="center">

**TrustLine / NPRU Sentinel** — Automated E2E Test Suite  
มหาวิทยาลัยราชภัฏนครปฐม · ตุลาคม 2569

</div>
