# PLAN & SPESIFIKASI FITUR: SimpleAgriChain Web

**Dokumen:** Product & Technical Plan (Fase 1 + Addendum Revisi 1)  
**Penyusun:** @planner (AG-01)  
**Root Proyek:** `C:\Ouput Shiro\SimpleAgriChain\`  
**Target Platform:** Python Flask (Web App) + Google Colaboratory Notebook (`.ipynb`)  
**Status:** Terverifikasi & Selaras Revisi 1  

---

## 1. Ringkasan Fitur & User Flow

SimpleAgriChain Web adalah sistem ketertelusuran rantai pasok pangan organik sederhana berbasis blockchain publik internal (permissioned logic tanpa mining/nonce). Menggunakan algoritma SHA-256 untuk memastikan catatan asal komoditas (Petani) dan kondisi transit (Distributor) tidak dapat diubah tanpa terdeteksi oleh Konsumen/Auditor.

### Prinsip Netralitas & Batas Sistem (Revisi 1):
Sistem ini bersifat **tamper-evident** (mendeteksi perubahan setelah data tercatat), **bukan penjamin kebenaran saat data pertama kali diketik**. Data awal diinput secara manual oleh operator (masalah Oracle), sehingga:
- Petani maupun Distributor sama-sama dapat menjadi sumber risiko mutu pangan.
- Petani dapat memasukkan gabah/beras dengan kadar air tinggi (> 14%) yang memicu risiko jamur.
- Distributor dapat mengetik angka suhu dingin (misal 15°C) padahal kondisi truk sebenarnya hangat (35°C), dan buku besar akan tetap sah (**VALID**) karena data tidak dimanipulasi pasca-pencatatan.
- Seluruh bahasa sistem dan antarmuka **netral**: menyebut "sumber risiko", tanpa menyalahkan atau menuduh salah satu aktor ("lalai", "pelanggaran", atau "kesalahan").

### 4 Tab Antarmuka Utama:
1. **Tab 1: Input Transaksi** — Dual form berdampingan: Inisiasi Panen Petani & Update Logistik Distributor.
2. **Tab 2: Pelacakan Konsumen** — Pencarian `Batch_ID` publik dengan visualisasi timeline hulu-ke-hilir dan auto-alert suhu transit (> 25°C).
3. **Tab 3: Blockchain Explorer** — Tampilan visual seluruh blok rantai, keterkaitan `previous_hash` & `current_hash`, serta badge validitas rantai (**VALID** / **INVALID**).
4. **Tab 4: Panel Simulasi Serangan** — Demo manipulasi data blok historis untuk menguji ketahanan dan deteksi kecurangan secara visual real-time.

### Ringkasan User Flow:
- **Flow A (Petani / Hulu):** Masuk Tab Input -> Isi form inisiasi (Batch ID, komoditas, lahan, panen, pupuk, sertifikat) -> Klik "Simpan ke Blockchain" -> Blok baru terbentuk -> Muncul hash blok -> Data tersinkron ke Explorer.
- **Flow B (Distributor / Logistik):** Masuk Tab Input -> Isi form pengiriman (Batch ID, tanggal, rute, suhu °C, kondisi) -> Klik "Perbarui Status Logistik" -> Blok lanjutan tercatat terikat blok petani.
- **Flow C (Konsumen & Auditor / Hilir):** Masuk Tab Pelacakan -> Masukkan `Batch_ID` (misal: `ORG-BRS-001`) -> Klik "Lacak" -> Tampil timeline asal panen, validasi sertifikat organik, status suhu pengiriman (warning merah jika > 25°C).
- **Flow D (Audit & Simulasi Serangan):** Masuk Tab Simulasi -> Pilih nomor blok target -> Ubah nilai parameter (misal suhu 35°C diubah jadi 15°C) -> Klik "Manipulasi Data" -> Sistem verifikasi ulang `is_chain_valid()` -> Status rantai berubah jadi **INVALID (Merah)** + Banner peringatan manipulasi aktif.

---

## 2. Acceptance Criteria (Dapat Diuji)

### A. Acceptance Criteria Baseline
- **AC-01 (Genesis Block):** Sistem otomatis membentuk Genesis Block (Index 0, `batch_id: "GENESIS"`, `previous_hash: "0"`) saat runtime pertama kali dijalankan tanpa error.
- **AC-02 (Input Petani Baseline):** Endpoint `POST /api/block/petani` berhasil menyimpan data panen baru, menghasilkan `current_hash` SHA-256 valid yang mengikat `previous_hash` blok sebelumnya, status rantai tetap VALID.
- **AC-03 (Input Distributor Baseline):** Endpoint `POST /api/block/distributor` berhasil menambahkan blok logistik dengan `batch_id` yang sesuai, mencatat data rute dan suhu.
- **AC-04 (Traceability Baseline):** Endpoint `GET /api/trace/<batch_id>` mengembalikan seluruh riwayat blok terkait secara kronologis dalam waktu < 1 detik.
- **AC-05 (Blockchain Explorer):** Endpoint `GET /api/chain` mengembalikan array semua blok dan boolean `is_valid`. Explorer menampilkan rantai blok terhubung.
- **AC-06 (Deteksi Manipulasi / Tamper Test):** Endpoint `POST /api/tamper` memodifikasi payload data blok target tanpa memperbarui hash blok setelahnya. Pemanggilan `is_chain_valid()` langsung mengembalikan `is_valid: false` beserta daftar indeks blok yang rusak. UI menampilkan status INVALID dan alert merah.
- **AC-07 (Ketahanan Data / Persistence):** Rantai blok disimpan dalam `ledger_data.json`. Data tidak hilang ketika aplikasi Flask di-restart.
- **AC-08 (Colab Notebook Skenario):** File `notebook/SimpleAgriChain_Colab.ipynb` dapat dijalankan run-all tanpa error, memuat `Block` & `SimpleAgriChain` yang identik dengan backend, dan memperlihatkan output skenario demonstrasi pada cell output.
- **AC-09 (Windows One-Click Launcher):** Script `run-agrichain.bat` berhasil mengeksekusi Flask menggunakan python virtual environment lokal (`.venv\Scripts\python.exe`) dan membuka browser ke halaman utama tanpa error terminal manual.

### B. Acceptance Criteria Revisi 1 (Netralitas & Kadar Air)
- **AC-R1 (Field Kadar Air Hulu):** `POST /api/block/petani` tanpa `kadar_air` menolak dengan HTTP 400. `kadar_air` valid (contoh 12.5 atau 18.5) disimpan ke dalam objek `data` blok dengan HTTP 201. Struktur 7 field utama blok tidak berubah.
- **AC-R2 (Evaluasi Risiko Hulu Netral):** `GET /api/trace/<batch>` untuk batch dengan kadar air 18.5% dan suhu 24.0°C mengembalikan: `has_moisture_alert: true`, `has_temperature_alert: false`, `has_quality_risk: true`, dan `risk_sources: ["PETANI"]`. Membuktikan risiko mutu dapat berasal dari tahap panen.
- **AC-R3 (Dua Sumber Risiko Bersamaan):** Batch dengan kadar air 18.5% dan suhu 35.0°C mengembalikan `risk_sources: ["PETANI", "DISTRIBUTOR"]`, dengan peringatan aktif untuk kedua tahap.
- **AC-R4 (Batas Sistem / Bohong Sejak Awal):** Jika Distributor menginput suhu 15.0°C sejak awal lewat form, `GET /api/chain` mengembalikan `is_valid: true` dan `tampered_indices: []`. Antarmuka web tetap menampilkan status VALID tanpa banner merah, disertai penjelasan terbuka bahwa ini adalah batas kemampuan ledger (tamper-evident pasca-catat, bukan verifikator kebenaran input awal).
- **AC-R5 (Bahasa Netral & Tanpa Tuduhan):** Tidak ada istilah menyudutkan ("lalai", "pelanggaran", "kesalahan petani", "kesalahan distributor") di API maupun antarmuka web.
- **AC-R6 (Label Sumber Data Manual):** Setiap entri timeline dan kartu explorer menampilkan label eksplisit: `"Sumber data: diisi manual oleh Petani/Distributor"`.
- **AC-R7 (Regresi & Kompatibilitas):** Seluruh pengujian integritas sebelumnya (genesis, tamper test, XSS escaping, payload dictionary validation, pencegahan duplikat inisiasi, pencegahan orphan distributor) tetap berfungsi 100%.

---

## 3. Negative & Edge Cases

1. **Edge Cases Kadar Air (`kadar_air`):**
   - **Kosong / Null / Missing:** Menghasilkan HTTP 400 Bad Request: `"Field wajib 'kadar_air' tidak boleh kosong"`.
   - **Non-Numerik (String/Simbol):** Menghasilkan HTTP 400 Bad Request: `"Nilai kadar air harus berupa angka numerik"`.
   - **Nilai Negatif (< 0.0%):** Menghasilkan HTTP 400 Bad Request: `"Nilai kadar air harus berada dalam rentang 0.0 s.d. 100.0 %"`.
   - **Nilai > 100.0%:** Menghasilkan HTTP 400 Bad Request: `"Nilai kadar air harus berada dalam rentang 0.0 s.d. 100.0 %"`.
   - **Tepat 14.0% (Ambang Batas):** Diterima sah (HTTP 201), status `moisture_alert: false` (hanya nilai > 14.0% yang memicu alert risiko).
2. **Payload JSON Non-Dictionary:** Seluruh endpoint POST menolak payload berupa JSON array (`[1, 2, 3]`), raw string, atau int dengan HTTP 400 `"Payload JSON harus berupa objek dictionary"`.
3. **Inisiasi Duplikat Petani:** `POST /api/block/petani` menolak `batch_id` yang sudah pernah diinisiasi Petani dengan HTTP 400.
4. **Distributor Orphan:** `POST /api/block/distributor` menolak `batch_id` yang belum pernah didaftarkan Petani dengan HTTP 400.
5. **Stored XSS Attack:** Seluruh string masukan pengguna (`komoditas`, `lokasi_lahan`, `pupuk`, `rute`, dll.) disanitasi menggunakan `escapeHtml()` sebelum dirender ke DOM; payload seperti `"><img src=x onerror=alert(1)>` dirender literal sebagai teks, bukan elemen HTML.
6. **Input Kosong / Incomplete Payload:** Form petani atau distributor dikirim dengan field string kosong atau null -> Client-side memblokir submit; Backend mengembalikan HTTP 400 Bad Request dengan pesan error spesifik.
7. **Suhu Non-Numerik atau Negatif Ekstrem:** Input suhu diisi karakter non-angka atau nilai anomali -> Backend memvalidasi tipe data angka (float/int).
8. **Pencarian Batch ID Tidak Ditemukan:** Konsumen mencari `batch_id` yang belum pernah didaftarkan -> API mengembalikan status sukses dengan data kosong / 404 informatif, UI menampilkan pesan ramah: *"Batch ID tidak ditemukan dalam buku besar"*.
9. **Manipulasi Blok yang Tidak Ada:** Request tamper pada `block_index` negatif atau di luar panjang rantai saat ini -> API mengembalikan HTTP 400/404 tanpa merusak integritas sistem.
10. **Klik Dobel (Double Submission):** User menekan tombol submit berkali-kali secara cepat -> Tombol di-disable saat fetch berlangsung dan indikator loading ditampilkan untuk mencegah duplikasi blok identik.
11. **File Ledger Hilang / Rusak (Corrupted JSON):** Jika `ledger_data.json` terhapus atau berisi format non-JSON -> Engine otomatis melakukan re-inisialisasi Genesis Block baru secara aman tanpa crash.
12. **Jaringan / Server Terputus:** Saat server Flask mati atau tidak merespons -> Fetch API di frontend menangkap error (`catch`) dan menampilkan toast "Koneksi ke node blockchain terputus".

---

## 4. Task Breakdown & Dependensi

Urutan eksekusi antar-role:

```
[Fase 1: Planner] -> [Fase 2: Architect + UI/UX] -> [Fase 3: Backend + Colab] -> [Fase 4: Frontend] -> [Fase 5: QA/Bug Report]
```

### A. Backend Developer Tasks (@backend)
1. **Core Engine (`blockchain.py`):**
   - Implementasi `class Block` dengan hashing SHA-256 (`compute_hash` dengan JSON canonical `sort_keys=True`).
   - Implementasi `class SimpleAgriChain` (genesis block, `add_block`, `is_chain_valid`, `trace_batch`, read/write `ledger_data.json`).
   - Revisi 1: Update `trace_batch(batch_id)` menghitung `kadar_air_max`, `moisture_threshold: 14.0`, `has_moisture_alert`, `has_quality_risk`, dan `risk_sources: ["PETANI"]` dan/atau `["DISTRIBUTOR"]`.
   - Revisi 1: Penanda `moisture_alert: true` pada entri timeline aktor PETANI dengan kadar air > 14.0%.
2. **Colab Notebook (`notebook/SimpleAgriChain_Colab.ipynb`):**
   - Buat notebook terstruktur: Teori singkat -> Implementasi Class -> Simulasi Skenario 1 (Normal) -> Skenario 2 (Pelacakan Risiko Panen Basah & Suhu Kritis) -> Skenario 3 (Bohong Sejak Awal / Batas Sistem) -> Skenario 4 (Tamper Attack).
3. **Web Server & REST API (`app.py`):**
   - Setup Flask app melayani static/template.
   - Endpoint `GET /` (render UI).
   - Endpoint `GET /api/chain`.
   - Endpoint `POST /api/block/petani` (Revisi 1: validasi `kadar_air` numerik rentang 0-100%, tolak duplikat batch).
   - Endpoint `POST /api/block/distributor` (tolak batch orphan).
   - Endpoint `GET /api/trace/<batch_id>`.
   - Endpoint `POST /api/tamper`.
   - Endpoint utilitas `POST /api/reset`.
   - Penguatan keamanan: validasi payload JSON dictionary wajib untuk semua endpoint POST.
4. **Packaging & Launcher:**
   - Sediakan `requirements.txt` (isi: `flask`).
   - Sediakan `run-agrichain.bat` (eksekusi via `.venv\Scripts\python.exe app.py`, polling curl, tanpa timeout.exe).
   - Sediakan `stop-agrichain.bat` (kill task python listener port 5000).

### B. Frontend Developer Tasks (@frontend)
1. **Layout & Multi-Tab Container (`templates/index.html`):**
   - Implementasi navbar 4 tab: Input, Trace, Explorer, Simulasi.
   - Setup styling via Tailwind CSS CDN.
2. **Tab 1 — Input Transaksi:**
   - Form Petani (Batch ID, komoditas, lokasi, tgl panen, pupuk, no sertifikat, input `kadar_air`) + tombol preset contoh panen normal dan panen basah (18%).
   - Form Distributor (Batch ID dropdown/input, tgl kirim, rute, suhu, status) + tombol preset contoh suhu normal dan distributor bohong sejak awal (suhu 15°C).
3. **Tab 2 — Pelacakan Konsumen:**
   - Search bar Batch ID + button submit.
   - Visualisasi timeline vertikal hulu ke hilir.
   - Evaluasi dua sumber risiko (`risk_sources` PETANI dan/atau DISTRIBUTOR) dengan bahasa netral tanpa menuduh.
   - Label eksplisit pada tiap langkah: `"Sumber data: diisi manual oleh Petani/Distributor"`.
   - Panel edukasi batas sistem: analogi buku besar direkatkan lem super (yang dijamin vs yang tidak dijamin).
4. **Tab 3 — Blockchain Explorer:**
   - Header status rantai: Badge **VALID (Hijau)** / **INVALID (Merah)**.
   - Kartu blok berurutan dengan label sumber data manual dan glosarium istilah awam (sidik jari digital, buku besar, tidak bisa diubah).
5. **Tab 4 — Panel Simulasi Serangan:**
   - Form pilih indeks blok dan edit field data pasca-catat.
   - Tombol "Jalankan Manipulasi" -> trigger API `/api/tamper`.
   - Tombol "Reset Ledger ke Awal" -> trigger API `/api/reset`.
   - Banner merah besar saat manipulasi pasca-catat terdeteksi.
6. **Interaksi Client & Keamanan:**
   - Sanitasi Stored XSS (`escapeHtml`) pada seluruh payload yang dirender ke innerHTML.
   - Indikator loading dan proteksi double-submit pada setiap tombol aksi.

---

## 5. Target Files (Daftar File yang Boleh Dibuat/Diedit)

Pengembangan WAJIB terbatas hanya pada file-file berikut di dalam root `C:\Ouput Shiro\SimpleAgriChain\`:

1. `docs\plan.md` (Dokumen ini — @planner)
2. `docs\architecture.md` (Spesifikasi arsitektur & API contract — @architect)
3. `docs\ui-spec.md` (Desain komponen, layout & token UI — @uiux)
4. `docs\bug-report.md` (Laporan pengujian & QA — AG-06 / QA)
5. `blockchain.py` (Modul inti blockchain, Block & SimpleAgriChain)
6. `app.py` (Aplikasi Flask & route REST API)
7. `ledger_data.json` (File persistence penyimpanan data blok)
8. `requirements.txt` (Daftar dependensi Python)
9. `templates\index.html` (Antarmuka web SPA 4 tab)
10. `notebook\SimpleAgriChain_Colab.ipynb` (Colab notebook simulasi 3 skenario)
11. `run-agrichain.bat` (Launcher Windows)
12. `stop-agrichain.bat` (Stopper Windows)
13. `README.md` (Petunjuk penggunaan singkat proyek)

---

## 6. Asumsi & Pertanyaan Terbuka

### Asumsi:
1. **[ASUMSI] Ambang Batas Suhu Pangan:** Batas kritis suhu penyimpanan sayur/organik ditetapkan sebesar **25.0°C**. Nilai > 25.0°C otomatis ditandai sebagai potensi kontaminasi/kerusakan logistik pada view pelacakan.
2. **[ASUMSI] Fitur Reset Data (`/api/reset`):** Demi kelancaran demo berulang di hadapan penguji/dosen, disediakan tombol reset pada panel simulasi untuk mengembalikan buku besar ke kondisi awal (hanya Genesis Block).
3. **[ASUMSI] QR Code Generator (FR-06):** Berstatus *Nice to Have*. Jika waktu implementasi memungkinkan, di-generate di client-side menggunakan library JavaScript ringan via CDN (misal: `qrcode.min.js`) tanpa menambah dependensi pip backend.

### Pertanyaan Terbuka:
- Apakah perlu disediakan pre-populated sample batch (tombol "Isi Data Contoh") di form agar demonstrator tidak perlu mengetik panjang saat presentasi? (Rekomendasi Planner: Sangat disarankan untuk ditambahkan oleh Frontend).
