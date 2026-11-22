# LAPORAN PENGUJIAN & BUG REPORT: SimpleAgriChain Web

**Dokumen:** QA Bug Report & Security Audit (Putaran 2 — Status Akhir)  
**Auditor:** @qa (AG-06 / Kuro_QA-Hunter)  
**Root Proyek:** `C:\Ouput Shiro\SimpleAgriChain\`  
**Target Dokumen:** @default (Orchestrator), @backend, @frontend, @user  
**Status Audit:** ZERO CRITICAL BUG (Semua temuan Putaran 1 telah terverifikasi bersih)  

---

## ZERO CRITICAL BUG

Seluruh perbaikan dari temuan Putaran 1 telah diuji ulang secara langsung pada runtime aktif, API, DOM browser nyata, dan skrip automation. Tidak ditemukan bug berstatus Critical maupun Medium yang tersisa.

---

## 1. Verifikasi Status Temuan Putaran 1

| No | ID Temuan | Severity Asal | Lokasi | Hasil Verifikasi Putaran 2 | Status Akhir |
|---|---|---|---|---|---|
| 1 | Stored XSS di Tab 2 & Tab 3 | Critical | `templates/index.html` | Helper `escapeHtml()` aktif di seluruh interpolasi string. Injeksi `<img src=x onerror=alert(...)>` via API teruji muncul literal (`&lt;img...`) dan query DOM `document.querySelectorAll("img[src=x]").length` terbukti **0** di browser. | **RESOLVED** |
| 2 | HTTP 500 Non-Dict JSON Array | Critical | `app.py` | Fungsi `get_dict_payload()` memvalidasi tipe objek. Request `[1, 2, 3]` ke `/api/block/petani`, `/api/block/distributor`, dan `/api/tamper` mengembalikan HTTP 400 Bad Request secara konsisten. | **RESOLVED** |
| 3 | Inisiasi Batch ID Duplikat | Medium | `app.py` | Validasi keunikan batch aktif. Inisiasi ulang batch_id yang sama oleh Petani ditolak dengan HTTP 400: `"Batch ID '...' sudah pernah diinisiasi oleh Petani"`. | **RESOLVED** |
| 4 | Distributor Orphan Batch | Medium | `app.py` | Validasi keterikatan hulu aktif. Pencatatan logistik untuk batch_id tanpa blok Petani ditolak dengan HTTP 400: `"Batch ID '...' belum diinisiasi oleh Petani"`. | **RESOLVED** |
| 5 | Filter Stop Script Netstat | Low | `stop-agrichain.bat` | Filter netstat diperketat ke `findstr /r /c:":5000 .*LISTENING"` dan pengecekan `if not "%%a"=="0"`. Mematikan port 5000 secara bersih tanpa error PID 0. | **RESOLVED** |

---

## 2. Checklist Lengkap Pengujian Sistem (Bukti Nyata)

| No | Aspek / Fitur | Skenario Uji | Parameter / Payload | Respon Aktual | Status |
|---|---|---|---|---|---|
| 1 | Lifecycle Web Server | Start via virtualenv | `.venv\Scripts\python.exe app.py` | Port 5000 listen, HTTP 200 OK | PASS |
| 2 | Genesis Block | Load awal rantai | `GET /api/chain` | HTTP 200, index 0, hash SHA-256 valid | PASS |
| 3 | Form & API Petani | Pencatatan komoditas | `POST /api/block/petani` | HTTP 201 Created, hash terikat Genesis | PASS |
| 4 | Form & API Distributor | Suhu normal (24.5°C) | `POST /api/block/distributor` | HTTP 201 Created, hash terikat blok sebelumnya | PASS |
| 5 | Traceability Pelacakan | Runut komoditas | `GET /api/trace/ORG-BRS-001` | HTTP 200 OK, timeline kronologis | PASS |
| 6 | Cold Chain Safety Alert | Suhu transit kritis (35.0°C) | `POST /api/block/distributor` | Alert bahaya suhu aktif di trace & banner UI | PASS |
| 7 | Simulasi Serangan Tamper | Manipulasi data historis | `POST /api/tamper` (Index 1) | HTTP 200 OK, `is_valid: false`, `tampered_indices: [1]` | PASS |
| 8 | Reset Buku Besar | Pembersihan ledger | `POST /api/reset` | HTTP 200 OK, ledger bersih kembali ke Genesis | PASS |
| 9 | Persistence File I/O | Integritas ledger file | Simpan/baca `ledger_data.json` | JSON valid, atomic replace sukses | PASS |
| 10 | Robustness: Payload Kosong | Field validation | `{}` ke endpoint POST | HTTP 400 Bad Request spesifik | PASS |
| 11 | Robustness: Non-Dict JSON | Tipe input salah | `[1, 2, 3]` ke endpoint POST | HTTP 400 Bad Request ("Payload JSON harus...") | PASS |
| 12 | Business Logic: Duplikat Batch | Proteksi double inisiasi | `batch_id` kembar pada Petani | HTTP 400 Bad Request ("sudah pernah diinisiasi") | PASS |
| 13 | Business Logic: Orphan Batch | Rantai tanpa hulu | Distributor kirim batch fiktif | HTTP 400 Bad Request ("belum diinisiasi") | PASS |
| 14 | Validasi Suhu: Non-Numerik | Type check suhu | `"suhu": "panas"` / `true` | HTTP 400 Bad Request ("harus angka numerik") | PASS |
| 15 | Validasi Suhu: Out-of-Range | Range -20.0 s.d 60.0°C | `"suhu": -25.0` / `65.0` | HTTP 400 Bad Request ("harus dalam rentang...") | PASS |
| 16 | Validasi Suhu: Suhu Dingin | Suhu beku wajar | `"suhu": -15.5` / `0.0` | HTTP 201 Created tersimpan normal | PASS |
| 17 | Boundary: Index Tamper | Jangkauan array | `block_index: -1` / `999` | HTTP 400 Bad Request ("di luar jangkauan") | PASS |
| 18 | Sanitasi: Null Byte URL | Karakter anomali | `/api/trace/ORG-BRS-001%00` | HTTP 404 Not Found aman tanpa crash | PASS |
| 19 | Security: Stored XSS | Script tag & event handler | `<img src=x onerror=...>` di form | Teks di-escape (`&lt;...`), 0 tag img bahaya di DOM | PASS |
| 20 | Colab Notebook | Pengujian 3 skenario | `SimpleAgriChain_Colab.ipynb` | 4 cell dieksekusi run-all tanpa error | PASS |
| 21 | Automation Launcher | One-click run | `run-agrichain.bat` | Polling port 5000 sukses, browser terbuka | PASS |
| 22 | Automation Stopper | One-click stop | `stop-agrichain.bat` | Proses port 5000 mati bersih tanpa error PID 0 | PASS |
