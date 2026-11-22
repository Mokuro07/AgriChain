# ARSITEKTUR SISTEM & KONTRAK API: SimpleAgriChain Web

**Dokumen:** System Architecture & API Contract (Fase 2 — Selaras Revisi 1)  
**Penyusun:** @architect (AG-02)  
**Root Proyek:** `C:\Ouput Shiro\SimpleAgriChain\`  
**Target:** Backend (@backend), Frontend (@frontend), UI/UX (@uiux), QA (@bug-report)  
**Status:** Ditetapkan & Mengikat Seluruh Tim  

---

## 1. Ikhtisar Arsitektur Sistem

SimpleAgriChain Web menggunakan arsitektur **Client-Server Ringan** dengan persistensi file JSON lokal tanpa database SQL eksternal.

```
[Browser Client (Vanilla JS + Tailwind)]
        │
        ▼ HTTP REST JSON (Port 5000)
┌───────────────────────────────────────────────────────────┐
│ Flask Web Application (app.py)                            │
│  ├── Static / Template Routes (GET /)                     │
│  └── API Controller Routes (/api/*)                       │
│           │                                               │
│           ▼ Python Function Calls                         │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Core Engine (blockchain.py)                         │  │
│  │  ├── Block (SHA-256 Hashing, Canonical JSON)        │  │
│  │  └── SimpleAgriChain                                │  │
│  │       ├── Genesis Initialization                    │  │
│  │       ├── add_block()                               │  │
│  │       ├── is_chain_valid() (Tamper Detector)        │  │
│  │       └── trace_batch() (Traceability Engine)       │  │
│  └─────────────────────────────────────────────────────┘  │
│           │                                               │
│           ▼ File I/O (Atomic Write/Read)                  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ ledger_data.json (Blockchain Persistence Ledger)    │  │
│  └─────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

### Karakteristik Desain & Batas Sistem (The Oracle Problem):
1. **Tamper-Evident, Bukan Penjamin Kebenaran Fisik Awal:**
   - Blockchain menjamin bahwa data **tidak dapat diubah, dihapus, atau diselipkan secara diam-diam setelah tercatat**.
   - Blockchain **tidak dapat mengetahui apakah angka yang diketik manusia saat pertama kali menginput data itu benar atau bohong**.
   - *Analogi Bahasa Awam:* Sistem ini bekerja seperti **buku catatan fisik yang setiap halamannya direkatkan menggunakan lem super transparan**. Siapapun tidak bisa merobek halaman atau menimpa tulisan tanpa meninggalkan bekas kerusakan yang kentara. Namun, jika seseorang menulis data bohong di halaman sebelum lem mengering, buku catatan akan tetap menyimpan kebohongan itu sebagai catatan yang sah (*Bohong Sejak Awal*).
2. **Evaluasi Titik Risiko Mutu Bersifat Netral:**
   - Tidak ada asumsi bahwa "Petani selalu benar" atau "Distributor selalu bersalah".
   - **Risiko Hulu (Petani):** Gabah/beras yang dipanen terlalu basah (**kadar air > 14.0%**) berisiko berjamur dan membusuk dari awal, meskipun suhu truk pengiriman terjaga dingin.
   - **Risiko Transit (Distributor):** Pengiriman dengan **suhu > 25.0°C** berisiko merusak kesegaran dan memicu pertumbuhan bakteri/jamur pada komoditas organik.
   - Sistem mencatat sumber risiko secara objektif lewat atribut `risk_sources` (`["PETANI"]`, `["DISTRIBUTOR"]`, atau keduanya), tanpa kata-kata menuduh seperti *lalai*, *pelanggar*, atau *kesalahan*.
3. **Zero PoW / No Mining:** Sistem tidak memerlukan nonce atau proof-of-work. Penambahan blok terjadi secara deterministik dan instan (< 100 ms).
4. **Kriptografi SHA-256 Deterministik:** Integritas blok diverifikasi melalui hash dari gabungan string representasi data blok sebelumnya dan blok saat ini dengan format kanonikal (`sort_keys=True`, tanpa spasi ekstra).
5. **Single Source of Truth:** `blockchain.py` menjadi modul inti tunggal yang dipakai oleh `app.py` dan disalin/diimpor pada notebook Colab (`notebook/SimpleAgriChain_Colab.ipynb`).

---

## 2. Struktur Penyimpanan Data (Ledger Storage)

Persistensi rantai disimpan dalam satu file JSON lokal: `ledger_data.json`.

### 2.1 Lokasi & Format File
- **Path:** `C:\Ouput Shiro\SimpleAgriChain\ledger_data.json`
- **Format:** JSON Array berisi daftar objek `Block`.

```json
[
  {
    "index": 0,
    "timestamp": "2026-11-08T10:00:00.000000Z",
    "batch_id": "GENESIS",
    "actor": "SYSTEM",
    "data": {
      "message": "Genesis Block SimpleAgriChain",
      "version": "1.0.0"
    },
    "previous_hash": "0",
    "current_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  }
]
```

### 2.2 Struktur Atribut Blok (7 Field Wajib)

| Field | Tipe Data | Wajib | Keterangan |
|---|---|---|---|
| `index` | Integer | Ya | Nomor urut blok dalam rantai, dimulai dari 0 (Genesis). Auto-increment. |
| `timestamp` | String (ISO 8601) | Ya | Waktu pencatatan blok (UTC), misal: `2026-11-08T10:30:00.000000Z`. |
| `batch_id` | String | Ya | ID unik kelompok komoditas. Format standar: `ORG-XXX-NNN` (atau `GENESIS`). |
| `actor` | String (Enum) | Ya | Nilai: `SYSTEM`, `PETANI`, `DISTRIBUTOR`. |
| `data` | Object (JSON) | Ya | Payload spesifik aktor (skema diuraikan di bawah). |
| `previous_hash`| String (Hex 64) | Ya | Hash SHA-256 blok sebelumnya. Blok 0 bernilai `"0"`. |
| `current_hash` | String (Hex 64) | Ya | Hash SHA-256 dari seluruh konten blok ini (kecuali atribut `current_hash` itu sendiri). |

### 2.3 Skema Payload Data per Aktor

#### A. Aktor: `PETANI` (Inisiasi Panen Hulu)
```json
{
  "komoditas": "Beras Merah Organik",
  "lokasi_lahan": "Desa Sukatani, Karawang",
  "tanggal_panen": "2026-11-05",
  "pupuk": "Kompos Kotoran Sapi Fermentasi (Organik)",
  "no_sertifikat": "SNI-ORGANIK-2026-0881",
  "kadar_air": 12.5
}
```
*Validasi:*
- `komoditas`: string (1-100 karakter), tidak boleh kosong.
- `lokasi_lahan`: string (1-150 karakter), tidak boleh kosong.
- `tanggal_panen`: string format tanggal valid `YYYY-MM-DD`.
- `pupuk`: string (1-100 karakter), tidak boleh kosong.
- `no_sertifikat`: string (1-50 karakter), tidak boleh kosong.
- `kadar_air`: float / integer wajib numerik dalam rentang `0.0` s.d. `100.0` (%).
  - Ambang batas aman mutu beras/gabah: **$\le$ 14.0%**.
  - Nilai **> 14.0%** memicu penanda risiko mutu hulu (`has_moisture_alert: true`, `risk_sources: ["PETANI"]`).
  - Nilai **tepat 14.0%** berada di batas toleransi aman (`has_moisture_alert: false`).
- **Pencegahan Inisiasi Duplikat:** Satu `batch_id` hanya boleh diinisiasi satu kali oleh Petani.

#### B. Aktor: `DISTRIBUTOR` (Pembaruan Logistik Transit)
```json
{
  "tanggal_kirim": "2026-11-06",
  "rute": "Karawang -> Gudang Distributor Jakarta Timur",
  "suhu": 23.5,
  "status_kondisi": "Dalam Pengiriman - Kemasan Tersegel Aman"
}
```
*Validasi:*
- `tanggal_kirim`: string format tanggal valid `YYYY-MM-DD`.
- `rute`: string (1-150 karakter), tidak boleh kosong.
- `suhu`: float / integer wajib numerik (rentang: `-20.0` s.d. `60.0` °C).
  - Ambang batas aman suhu logistik komoditas: **$\le$ 25.0°C**.
  - Nilai **> 25.0°C** memicu penanda risiko mutu transit (`has_temperature_alert: true`, `risk_sources: ["DISTRIBUTOR"]`).
- `status_kondisi`: string (1-100 karakter), tidak boleh kosong.
- **Pencegahan Batch Orphan:** Distributor tidak diizinkan mencatat blok jika `batch_id` belum pernah diinisiasi oleh Petani.

#### C. Aktor: `SYSTEM` (Genesis Block)
```json
{
  "message": "Genesis Block SimpleAgriChain",
  "version": "1.0.0"
}
```

---

## 3. Algoritma Kriptografi & Core Engine (`blockchain.py`)

### 3.1 Perhitungan Hash SHA-256
Untuk menjamin determinisme, pembuatan hash blok dilakukan dengan format kanonikal:
```python
def compute_hash(self) -> str:
    block_dict = {
        "index": self.index,
        "timestamp": self.timestamp,
        "batch_id": self.batch_id,
        "actor": self.actor,
        "data": self.data,
        "previous_hash": self.previous_hash
    }
    block_string = json.dumps(block_dict, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(block_string.encode('utf-8')).hexdigest()
```

### 3.2 Aturan Validasi Rantai (`is_chain_valid`)
Fungsi `is_chain_valid()` mengembalikan tuple: `(is_valid: bool, tampered_indices: list[int])`.
Rantai dinyatakan **VALID** jika dan hanya jika:
1. `chain[0].previous_hash == "0"` dan `chain[0].current_hash == chain[0].compute_hash()`.
2. Untuk setiap blok `i` dari `1` s.d. `len(chain)-1`:
   - `chain[i].previous_hash == chain[i-1].current_hash`.
   - `chain[i].current_hash == chain[i].compute_hash()`.
Jika ada blok yang tidak cocok, masukkan indeks blok tersebut ke dalam `tampered_indices` dan set `is_valid = False`.

### 3.3 Penanganan File Ledger
- Saat inisialisasi:
  - Jika file `ledger_data.json` ada dan valid JSON: baca dan bangun rantai memori.
  - Jika file hilang atau rusak (corrupted JSON): inisialisasi rantai baru dengan satu Genesis Block, lalu simpan ke file.
- Setiap penambahan blok (`add_block`), perubahan tamper (`tamper_block`), atau reset (`reset_chain`): tulis ulang file `ledger_data.json` secara atomic.

---

## 4. Spesifikasi Kontrak REST API

Semua request dan response menggunakan Content-Type: `application/json`.
Base URL lokal: `http://127.0.0.1:5000`

### 4.1 Ringkasan Endpoint

| No | Method | Endpoint | Deskripsi | Aktor Utama |
|---|---|---|---|---|
| 1 | `GET` | `/` | Melayani UI Web SPA (HTML single-page) | Semua User |
| 2 | `GET` | `/api/chain` | Mengambil seluruh blok & status validitas rantai | Explorer / UI |
| 3 | `POST` | `/api/block/petani` | Menambahkan data panen baru dari petani | Petani |
| 4 | `POST` | `/api/block/distributor` | Menambahkan data transit pengiriman | Distributor |
| 5 | `GET` | `/api/trace/<batch_id>` | Mengambil riwayat runut & indikator suhu | Konsumen / Auditor |
| 6 | `POST` | `/api/tamper` | Memanipulasi isi blok untuk simulasi serangan | Presenter / Auditor |
| 7 | `POST` | `/api/reset` | Mereset ledger ke kondisi awal (hanya Genesis) | Presenter / QA |

---

### 4.2 Rincian Endpoint

#### 1. `GET /api/chain`
Mengambil data seluruh rantai blok untuk kebutuhan Explorer dan verifikasi integritas rantai.

- **Request:**
  - Header: `Accept: application/json`
  - Body: *None*
- **Response Success (HTTP 200):**
```json
{
  "success": true,
  "is_valid": true,
  "tampered_indices": [],
  "total_blocks": 2,
  "chain": [
    {
      "index": 0,
      "timestamp": "2026-11-08T10:00:00.000000Z",
      "batch_id": "GENESIS",
      "actor": "SYSTEM",
      "data": {
        "message": "Genesis Block SimpleAgriChain",
        "version": "1.0.0"
      },
      "previous_hash": "0",
      "current_hash": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b"
    },
    {
      "index": 1,
      "timestamp": "2026-11-08T10:15:30.123456Z",
      "batch_id": "ORG-BRS-001",
      "actor": "PETANI",
      "data": {
        "komoditas": "Beras Merah Organik",
        "lokasi_lahan": "Desa Sukatani, Karawang",
        "tanggal_panen": "2026-11-05",
        "pupuk": "Kompos Kotoran Sapi Fermentasi (Organik)",
        "no_sertifikat": "SNI-ORGANIK-2026-0881"
      },
      "previous_hash": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
      "current_hash": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
    }
  ]
}
```

---

#### 2. `POST /api/block/petani`
Menambahkan blok transaksi inisiasi batch komoditas organik oleh Petani.

- **Request:**
  - Header: `Content-Type: application/json`
  - Body:
```json
{
  "batch_id": "ORG-BRS-001",
  "komoditas": "Beras Merah Organik",
  "lokasi_lahan": "Desa Sukatani, Karawang",
  "tanggal_panen": "2026-11-05",
  "pupuk": "Kompos Kotoran Sapi Fermentasi (Organik)",
  "no_sertifikat": "SNI-ORGANIK-2026-0881"
}
```
- **Response Success (HTTP 201 Created):**
```json
{
  "success": true,
  "message": "Blok Petani berhasil dicatat dalam blockchain",
  "block": {
    "index": 1,
    "timestamp": "2026-11-08T10:15:30.123456Z",
    "batch_id": "ORG-BRS-001",
    "actor": "PETANI",
    "data": {
      "komoditas": "Beras Merah Organik",
      "lokasi_lahan": "Desa Sukatani, Karawang",
      "tanggal_panen": "2026-11-05",
      "pupuk": "Kompos Kotoran Sapi Fermentasi (Organik)",
      "no_sertifikat": "SNI-ORGANIK-2026-0881"
    },
    "previous_hash": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
    "current_hash": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
  }
}
```
- **Response Error (HTTP 400 Bad Request):**
```json
{
  "success": false,
  "error": "Field wajib 'batch_id' tidak boleh kosong"
}
```

---

#### 3. `POST /api/block/distributor`
Menambahkan blok logistik distribusi lanjutan untuk batch komoditas yang sedang beredar.

- **Request:**
  - Header: `Content-Type: application/json`
  - Body:
```json
{
  "batch_id": "ORG-BRS-001",
  "tanggal_kirim": "2026-11-06",
  "rute": "Karawang -> Gudang Distributor Jakarta Timur",
  "suhu": 35.0,
  "status_kondisi": "Dalam Pengiriman - Transit Hangat"
}
```
- **Response Success (HTTP 201 Created):**
```json
{
  "success": true,
  "message": "Blok Distributor berhasil dicatat dalam blockchain",
  "block": {
    "index": 2,
    "timestamp": "2026-11-08T10:20:15.987654Z",
    "batch_id": "ORG-BRS-001",
    "actor": "DISTRIBUTOR",
    "data": {
      "tanggal_kirim": "2026-11-06",
      "rute": "Karawang -> Gudang Distributor Jakarta Timur",
      "suhu": 35.0,
      "status_kondisi": "Dalam Pengiriman - Transit Hangat"
    },
    "previous_hash": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
    "current_hash": "8f480329ac614dee7923186156c4069e20384b8f64f0d6db37ebbe590e35f502"
  }
}
```
- **Response Error (HTTP 400 Bad Request):**
```json
{
  "success": false,
  "error": "Nilai suhu harus berupa angka numerik"
}
```

---

#### 4. `GET /api/trace/<batch_id>`
Mengambil timeline hulu-hilir komoditas berdasarkan Batch ID publik beserta evaluasi keamanan suhu.

- **Request:**
  - URL Parameter: `batch_id` (contoh: `ORG-BRS-001`)
  - Header: `Accept: application/json`
- **Response Success (HTTP 200 OK — Ditemukan):**
```json
{
  "success": true,
  "batch_id": "ORG-BRS-001",
  "total_records": 2,
  "has_temperature_alert": true,
  "max_temperature": 35.0,
  "temperature_threshold": 25.0,
  "certificate_valid": true,
  "no_sertifikat": "SNI-ORGANIK-2026-0881",
  "timeline": [
    {
      "step": 1,
      "index": 1,
      "actor": "PETANI",
      "timestamp": "2026-11-08T10:15:30.123456Z",
      "data": {
        "komoditas": "Beras Merah Organik",
        "lokasi_lahan": "Desa Sukatani, Karawang",
        "tanggal_panen": "2026-11-05",
        "pupuk": "Kompos Kotoran Sapi Fermentasi (Organik)",
        "no_sertifikat": "SNI-ORGANIK-2026-0881"
      },
      "current_hash": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
    },
    {
      "step": 2,
      "index": 2,
      "actor": "DISTRIBUTOR",
      "timestamp": "2026-11-08T10:20:15.987654Z",
      "data": {
        "tanggal_kirim": "2026-11-06",
        "rute": "Karawang -> Gudang Distributor Jakarta Timur",
        "suhu": 35.0,
        "status_kondisi": "Dalam Pengiriman - Transit Hangat"
      },
      "temperature_alert": true,
      "current_hash": "8f480329ac614dee7923186156c4069e20384b8f64f0d6db37ebbe590e35f502"
    }
  ]
}
```
- **Response Not Found (HTTP 404 Not Found):**
```json
{
  "success": false,
  "error": "Batch ID 'ORG-XYZ-999' tidak ditemukan dalam buku besar",
  "batch_id": "ORG-XYZ-999",
  "timeline": []
}
```

---

#### 5. `POST /api/tamper`
Memanipulasi nilai data pada blok tertentu tanpa memperbarui hash blok setelahnya. Digunakan untuk demonstrasi perusakan integritas rantai.

- **Request:**
  - Header: `Content-Type: application/json`
  - Body:
```json
{
  "block_index": 2,
  "modified_data": {
    "tanggal_kirim": "2026-11-06",
    "rute": "Karawang -> Gudang Distributor Jakarta Timur",
    "suhu": 15.0,
    "status_kondisi": "Suhu Dingin Terjaga Baik (Palsu)"
  }
}
```
- **Response Success (HTTP 200 OK — Manipulasi Berhasil Dilakukan):**
```json
{
  "success": true,
  "message": "Data blok index 2 berhasil dimanipulasi",
  "block_index": 2,
  "chain_validity": {
    "is_valid": false,
    "tampered_indices": [2],
    "message": "PERINGATAN: Integritas rantai rusak! Hash tidak cocok."
  }
}
```
- **Response Error (HTTP 400 Bad Request — Index di Luar Jangkauan):**
```json
{
  "success": false,
  "error": "Indeks blok tidak valid atau di luar jangkauan (0 <= index < panjang rantai)"
}
```

---

#### 6. `POST /api/reset`
Mereset buku besar rantai ke kondisi awal hanya menyisakan Genesis Block. Memudahkan presenter mengulang skenario demo.

- **Request:**
  - Header: `Content-Type: application/json`
  - Body: `{}` (Opsional / Kosong)
- **Response Success (HTTP 200 OK):**
```json
{
  "success": true,
  "message": "Buku besar berhasil direset ke Genesis Block",
  "total_blocks": 1,
  "is_valid": true
}
```

---

## 5. Struktur Folder Proyek & Pemetaan Peran File

Semua berkas berada di dalam direktori absolut:  
`C:\Ouput Shiro\SimpleAgriChain\`

```
C:\Ouput Shiro\SimpleAgriChain\
├── .venv\                           # Virtual environment Python lokal (sudah ada Flask)
├── docs\
│   ├── brief.md                     # Brief asli proyek & keputusan user
│   ├── plan.md                      # Spesifikasi fitur & task breakdown (@planner)
│   ├── architecture.md              # Spesifikasi teknis & API contract (@architect)
│   ├── ui-spec.md                   # Desain antarmuka & design tokens (@uiux)
│   └── bug-report.md                # Laporan verifikasi pengujian (@bug-report)
├── notebook\
│   └── SimpleAgriChain_Colab.ipynb  # Notebook Google Colab 3 skenario runnable (@backend)
├── templates\
│   └── index.html                   # Antarmuka SPA 4 tab (Tailwind + Vanilla JS) (@frontend)
├── app.py                           # Web server Flask & REST API endpoints (@backend)
├── blockchain.py                    # Class Block & SimpleAgriChain (Pure Python) (@backend)
├── ledger_data.json                 # File persistensi data rantai blok (Auto-generated)
├── requirements.txt                 # Manifest dependensi pip (flask)
├── run-agrichain.bat                # Launcher one-click Windows (@backend)
├── stop-agrichain.bat               # Killer process port 5000 Windows (@backend)
└── README.md                        # Panduan instalasi dan penggunaan (@backend / tim)
```

---

## 6. Daftar Library, Package, & Dependensi

Untuk memastikan Backend dan Frontend tidak salah sambung atau menginstal dependensi yang bertolak belakang:

### 6.1 Backend (Python Environment)
- **Python Version:** 3.14.9 (atau 3.10+ kompatibel)
- **Interpreter Path:** `C:\Ouput Shiro\SimpleAgriChain\.venv\Scripts\python.exe`
- **Isi `requirements.txt`:**
  ```text
  flask>=3.1.0
  ```
- **Standard Library Digunakan:**
  - `hashlib` (SHA-256 computation)
  - `json` (Serialization kanonikal & file I/O)
  - `datetime` (ISO 8601 UTC timestamp format: `datetime.now(timezone.utc).isoformat()`)
  - `os`, `sys`, `pathlib` (Penanganan file path absolut & atomic writing)

### 6.2 Frontend (Client-Side)
- **Tanpa Node.js / Tanpa Build Step (No npm / Vite).**
- **Styling:** Tailwind CSS Play CDN:
  ```html
  <script src="https://cdn.tailwindcss.com"></script>
  ```
- **Font & Icon:**
  - Font: Inter / System UI sans-serif bawaan Tailwind.
  - Icon: SVG Heroicons inline (bebas dependensi eksternal).
- **QR Code Generator (FR-06 Nice to Have):**
  - QRCode.js CDN:
  ```html
  <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
  ```
- **Network Call:** Standard browser `fetch()` API asynchronous.

---

## 7. Spesifikasi Launcher & Automation Scripts (Windows)

Presenter dan pengguna tidak terbiasa menggunakan command line terminal. Oleh karena itu, disediakan 2 script batch double-clickable:

### 7.1 `run-agrichain.bat`
- **Fungsi:** Menjalankan Flask di background/minimized, menunggu 2 detik hingga port 5000 listen, kemudian membuka browser default ke `http://127.0.0.1:5000`.
- **Implementasi:**
```bat
@echo off
title SimpleAgriChain Launcher
cd /d "%~dp0"
echo Memulai SimpleAgriChain Web Server...
start "" /b ".venv\Scripts\python.exe" app.py
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000
echo Server aktif di http://127.0.0.1:5000
exit
```

### 7.2 `stop-agrichain.bat`
- **Fungsi:** Menghentikan proses Python server yang mendengarkan port 5000 secara bersih.
- **Implementasi:**
```bat
@echo off
title SimpleAgriChain Stopper
echo Menghentikan SimpleAgriChain Web Server...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000') do taskkill /f /pid %%a >nul 2>&1
echo Server berhasil dihentikan.
pause
```

---

## 8. Panduan Integrasi Antar-Peran

1. **Untuk @uiux:**
   - Gunakan skema data di Bagian 2 untuk merancang input form Tab 1 (Petani & Distributor) dan timeline Tab 2.
   - Sediakan alert badge merah terang untuk suhu > 25°C dan rantai invalid.
   - Siapkan tombol cepat "Isi Contoh Data" (*sample pre-fill*) pada Tab Input agar presenter mudah mendemonstrasikan sistem.

2. **Untuk @backend:**
   - Implementasikan `blockchain.py` dengan method signature:
     - `Block(index, batch_id, actor, data, previous_hash, timestamp=None)`
     - `compute_hash()`
     - `SimpleAgriChain(storage_path="ledger_data.json")`
     - `create_genesis_block()`, `add_block(batch_id, actor, data)`, `is_chain_valid()`, `trace_batch(batch_id)`, `tamper_block(block_index, modified_data)`, `reset_chain()`
   - Pastikan response format `app.py` 100% identik dengan Bagian 4 agar @frontend tidak mengalami inkonsistensi payload.
   - Buat file `notebook/SimpleAgriChain_Colab.ipynb` dengan 3 skenario sesuai acceptance criteria.

3. **Untuk @frontend:**
   - Bangun SPA pada `templates/index.html` dengan 4 tab yang memanggil endpoint pada Bagian 4.
   - Berikan feedback visual: button loading state, disable double-submit, dan toast notification.
   - Saat tab Explorer dibuka, lakukan pooling/fetch `GET /api/chain` untuk menampilkan status rantai secara real-time.

---

*Dokumen ini sah dan mengikat seluruh tim pengembang SimpleAgriChain.*

---

## 9. Autentikasi & Otorisasi (15 November 2026)

**Peran:** `admin` (baca + tulis) dan `user` (baca saja). Disimpan di sesi Flask (`session["user"]`, `session["role"]`).

| Aturan | Perilaku |
|---|---|
| Tanpa sesi, akses halaman | `302` redirect ke `/login` |
| Tanpa sesi, akses `/api/*` | `401` JSON `{"success": false, "error": "Belum login. Silakan login dulu."}` |
| Login salah | `401` + halaman login dengan pesan "Username atau password salah." |
| `POST` `/api/block/petani`, `/api/block/distributor`, `/api/tamper`, `/api/reset` oleh `user` | `403` JSON `{"success": false, "error": "Aksi ini hanya untuk admin."}` |
| `GET` `/api/chain`, `/api/trace/<id>` oleh `user` | `200` (tetap boleh) |

Akun disimpan di `USERS` (`app.py`) dengan `werkzeug.security.generate_password_hash`; password tidak pernah disimpan sebagai teks biasa. Secret sesi dari env `AGRICHAIN_SECRET` (default khusus pengembangan).

**Dampak ke UI:** template `index.html` dirender dengan `role`, `name`, `username`. Tab Input dan Uji Ubah beserta section-nya hanya dirender untuk `admin`; tombol "+ Catat transaksi" dan tautan "Lihat di Tab Uji Coba" juga. Badge peran (`ADMIN`/`USER`) dan tombol Keluar ada di kanan header.


---

## 10. Tautan Verifikasi Publik (QR) — 15 November 2026

QR pada kartu hasil pelacakan berisi `/?batch=<BATCH_ID>`. Alur untuk pengunjung yang belum punya sesi:

1. Buka `/?batch=ORG-KONSUMEN-001` → guard mengembalikan `302` ke `/login?next=/?batch%3DORG-KONSUMEN-001`.
2. Form login membawa `<input type="hidden" name="next">`; setelah kredensial benar, server redirect ke `next` **hanya jika** nilainya diawali `/` dan bukan `//` (mencegah open redirect).
3. Halaman `/` membaca parameter `batch`, langsung membuka tab Lacak dan menjalankan pelacakan otomatis.

`/logout` ditambahkan ke `PUBLIC_ENDPOINTS`: membuka `/logout` tanpa sesi tidak lagi memicu loop `login → logout → login`.


---

## 11. Pendaftaran Akun (register) — 16 November 2026

**Penyimpanan akun:** `users.json` di root proyek (bukan lagi dict di kode). Struktur: `{"username": {"name", "role", "pw"}}`, `pw` = hash `werkzeug`. Dibuat otomatis saat server start bila belum ada, berisi `admin` (role admin) dan `user` (role user). Path bisa dialihkan lewat env `AGRICHAIN_USERS` (dipakai skrip uji supaya tidak menyentuh akun asli).

**Endpoint:**

| Method | Path | Aturan |
|---|---|---|
| `GET` | `/register` | Halaman formulir; kalau sudah login → redirect ke `/` |
| `POST` | `/register` | Validasi di bawah; sukses → `302 /login?registered=1` |

**Validasi (semua mengembalikan `400` + pesan di halaman):**

| Kondisi | Pesan |
|---|---|
| Username tidak cocok `^[a-z0-9_]{3,20}$` | "Username 3–20 karakter: huruf kecil, angka, atau garis bawah." |
| Username sudah ada | "Username itu sudah dipakai. Pilih yang lain." |
| Nama kosong | "Nama tampilan wajib diisi." |
| Password < 8 karakter | "Password minimal 8 karakter." |
| Konfirmasi berbeda | "Konfirmasi password belum sama." |

**Batas keamanan:** pendaftaran mandiri **selalu** menghasilkan `role="user"` — peran admin tidak bisa dibuat lewat form. Penulisan `users.json` memakai atomic replace (`.json.tmp` → rename) supaya file tidak korup bila proses berhenti di tengah.

**Konsekuensi ke skrip uji:** server uji memakai `AGRICHAIN_USERS` sementara dan port acak, sehingga akun asli dan data asli tidak tersentuh.
