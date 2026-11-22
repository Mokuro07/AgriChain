# BRIEF PROYEK — SimpleAgriChain Web

Sumber: PRD `SimpleAgriChain Web` (Final Draft v1.0) + docx "Peta Konsep dan Skeleton Sistem Blockchain Pertanian (Versi Ringkas 3 Aktor)".
Kedua file asli ada di `C:\Users\sevar\AppData\Local\hermes\attachments\`.

## Root kerja (WAJIB, absolut)
`C:\Ouput Shiro\SimpleAgriChain\`
Semua dokumen dan kode ditulis di bawah root ini. Nggak ada yang nulis di tempat lain.

Struktur yang diharapkan (boleh disesuaikan architect kalau ada alasan jelas, tulis di docs/architecture.md):

```
C:\Ouput Shiro\SimpleAgriChain\
├── docs\brief.md            <- ini
├── docs\plan.md             <- AG-01
├── docs\architecture.md     <- AG-02
├── docs\ui-spec.md          <- AG-03
├── docs\bug-report.md       <- AG-06
├── blockchain.py            <- Class Block + Class SimpleAgriChain (inti, bebas framework)
├── app.py                   <- Flask: routing halaman + REST API
├── ledger_data.json         <- persistence rantai blok
├── requirements.txt
├── templates\index.html     <- UI utama, 4 tab
└── run-agrichain.bat        <- launcher double-click buat user (Windows)
```

## Konteks produk
Sistem blockchain keamanan pangan & anti-pemalsuan sertifikasi organik, prototipe tugas semester 5.
3 aktor, TANPA mining/nonce (no Proof of Work):
1. Petani/Produsen — write: inisiasi batch (Batch_ID, komoditas, lokasi lahan, tanggal panen, pupuk, no sertifikat organik)
2. Distributor/Logistik — write: update pengiriman (Batch_ID, tanggal kirim, rute, suhu °C, status kondisi)
3. Konsumen/Auditor — read-only: trace by Batch_ID

## Fitur wajib (dari PRD Bab 3)
- FR-01 Core Blockchain Engine: genesis block (Blok 0, batch_id "GENESIS", previous_hash "0") saat server start; chain SHA-256 ngikat previous_hash + current_hash; TANPA nonce.
- FR-02 Form/formulir input Petani -> POST /api/block/petani, tampilkan hash blok yang terbentuk.
- FR-03 Form input Distributor -> POST /api/block/distributor.
- FR-04 Halaman trace publik -> GET /api/trace/<batch_id>: visualisasi timeline hulu->hilir, status keaslian sertifikat, peringatan otomatis kalau suhu > 25 °C.
- FR-05 Blockchain Explorer -> GET /api/chain: seluruh blok + status is_chain_valid, badge VALID (hijau) / INVALID (merah) + tombol "Simulasi Manipulasi Data".
- FR-06 (Nice to have) Generator QR Code batch yang mengarah ke /trace?batch_id=...

## Kontrak inti (dari PRD Bab 4.2/4.3) — jangan diubah tanpa alasan kuat
Struktur JSON blok, 7 atribut: `index`, `timestamp`, `batch_id`, `actor`, `data`, `previous_hash`, `current_hash`.
Kelas: `Block(index, batch_id, actor, data, previous_hash, timestamp=None)`, `compute_hash()`, dan
`SimpleAgriChain`: `create_genesis_block()`, `add_block(batch_id, actor, data)`, `is_chain_valid()` (kembalikan valid + daftar index blok rusak), `trace_batch(batch_id)`.

Endpoint REST (PRD Bab 4.4): `GET /api/chain`, `POST /api/block/petani`, `POST /api/block/distributor`, `GET /api/trace/<batch_id>`, `POST /api/tamper` (`block_index`, `modified_data`).

## Acceptance criteria (PRD Bab 6) — 3 skenario demo
1. Happy path: input ORG-BRS-001 (Beras Merah Organik) lewat form Petani, lalu form Distributor -> explorer nambah blok real-time, badge VALID hijau.
2. Instant recall: trace ORG-BRS-001 tampil < 1 detik, kronologi lengkap, sorotan merah: kontaminasi dari suhu 35 °C di tahap Distributor (bukan salah Petani).
3. Tamper detection: ubah suhu 35 -> 15 (atau ganti no sertifikat) lewat panel simulasi -> is_chain_valid() gagal, badge INVALID merah, banner "PERINGATAN: Data Blok Telah Dimanipulasi / Rantai Tidak Valid!".

## Keputusan user (jangan ditanya ulang)
- Scope DIPERLUAS dari PRD: PRD Bab 7 Fase 1 minta prototipe algoritma Google Colab. Ikut dikerjakan
  sebagai `notebook\SimpleAgriChain_Colab.ipynb` (bisa dijalankan di Colab, nunjukin 3 skenario di konsol).
  `blockchain.py` harus jadi satu-satunya sumber inti, notebook meng-import/menyalin isinya — jangan dua implementasi berbeda.
- Opsi A (Flask) yang dipakai, bukan Opsi B single-file client-side.
- Tech stack UI: Tailwind CSS via CDN + Vanilla JS Fetch API. Nggak ada build step, nggak ada node.
- 4 tab sesuai PRD Bab 5: Input Transaksi, Pelacakan Konsumen, Live Blockchain Explorer, Panel Simulasi Serangan.
- Persistence: file lokal `ledger_data.json` (bukan SQLite) — cukup buat demo, gampang direset presenter.
- Distribusi ke user: HARUS ada `run-agrichain.bat` yang bisa di-double-click di Windows, plus `stop-agrichain.bat`.
  User nggak nyaman main terminal. Runtime Python: TIDAK ada system python3/pip; pakai uv (`uv run --with flask python app.py`)
  atau venv lokal. Architect tentukan cara paling sederhana yang beneran jalan di mesin ini, dan tulis di docs/architecture.md.

## Runtime (SUDAH DIVERIFIKASI jalan di mesin ini — pakai ini, jangan cari cara lain)
```
C:\Ouput Shiro\SimpleAgriChain\.venv\Scripts\python.exe   <- sudah dibuat, sudah ada Flask 3.1.3 (Python 3.14.9)
```
`.venv` sudah dibuat pakai uv dan `flask` sudah terinstall. `run-agrichain.bat` cukup panggil
`.venv\Scripts\python.exe app.py` lalu buka `http://127.0.0.1:5000`. `requirements.txt` tetap ditulis (isi: `flask`).
Jangan pakai `php artisan serve`-style workaround, jangan pakai node/build step.

## Batas
- Nggak ada auth/login (PA di luar scope).
- Nggak ada deploy cloud, cukup jalan lokal `http://127.0.0.1:<port>`.
- Bahasa UI + dokumen: Indonesia.
