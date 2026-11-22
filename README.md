# SimpleAgriChain Web

Sistem ketertelusuran rantai pasok pangan organik sederhana berbasis blockchain internal (permissioned logic tanpa mining/nonce) dengan kriptografi SHA-256 kanonikal dan pemantauan suhu rantai dingin (*cold chain food safety*).

---

## 🌾 Fitur Utama

1. **Dual Form Transaksi Hulu-Hilir:**
   - **Petani:** Inisiasi panen, pencatatan varietas organik, nomor sertifikat SNI/organik, pupuk, dan lokasi lahan.
   - **Distributor:** Pembaruan logistik, tanggal kirim, rute transportasi, kondisi barang, dan suhu pengiriman (°C).
2. **Peringatan Suhu Otomatis (Food Safety Guard):**
   - Ambang batas kritis suhu pangan segar: **25.0°C**.
   - Jika suhu transit melebihi 25.0°C, sistem pelacakan otomatis menampilkan peringatan bahaya mutu/keamanan pangan.
3. **Blockchain Explorer Real-time:**
   - Visualisasi setiap blok dengan rantai hash `previous_hash` dan `current_hash`.
   - Indikator integritas instan: status rantai **VALID** (Hijau) atau **INVALID** (Merah).
4. **Panel Simulasi Serangan (Tamper Resistance Demo):**
   - Menguji keandalan sistem terhadap manipulasi data historis di buku besar (*ledger*).
   - Menunjukkan bagaimana modifikasi 1 nilai saja langsung merusak konsistensi SHA-256 dan terdeteksi oleh auditor/konsumen.
5. **Google Colab Notebook:**
   - Demonstrasi mandiri 3 skenario (*Normal Flow*, *Temperature Alert*, dan *Tamper Attack*) di `notebook/SimpleAgriChain_Colab.ipynb`.

---

## 🔐 Akun & Batas Peran

Aplikasi memakai sesi login (Flask session). Ada dua peran:

| Akun | Password | Peran | Boleh apa |
|---|---|---|---|
| `admin` | `admin123` | ADMIN | Semua tab: Dashboard, Input, Lacak, Buku Besar, Uji Ubah — termasuk catat transaksi, uji tamper, reset buku |
| `user` | `user123` | USER (konsumen) | Halaman awal **Lacak**: masukkan Batch ID dari kemasan / buka tautan QR → lihat asal panen, perjalanan, dan tanda risiko. Tab Buku Besar tetap bisa dibaca. Tab Input, Uji Ubah, dan Dashboard tidak dirender; POST tulis ditolak 403 |

Tombol **Keluar** ada di kanan header. Ganti secret sesi lewat env `AGRICHAIN_SECRET` untuk pemakaian di luar lokal.

---

## 🚀 Cara Menjalankan Aplikasi

### Opsi 1: One-Click Launcher (Windows)
Cukup klik ganda (double-click) file launcher:
- **Jalankan:** `run-agrichain.bat`
  - Memulai server Flask secara otomatis.
  - Melakukan polling kesiapan port 5000 dengan `curl`.
  - Membuka peramban default ke `http://127.0.0.1:5000` → diarahkan ke halaman **Masuk**.
- **Hentikan:** `stop-agrichain.bat`
  - Mematikan proses background yang mendengarkan port 5000.

### Opsi 2: Manual Terminal
Pastikan virtual environment telah aktif:
```bash
# Masuk ke folder proyek
cd "C:\Ouput Shiro\SimpleAgriChain"

# Jalankan server
.venv\Scripts\python.exe app.py
```
Akses di browser: `http://127.0.0.1:5000`

---

## 📡 Dokumentasi Endpoint REST API

Semua request dan response menggunakan format `application/json`.

| Method | Endpoint | Deskripsi |
|---|---|---|
| `GET` | `/login` | Halaman masuk (form username/password) |
| `POST` | `/login` | Proses login, set sesi (401 kalau salah) |
| `GET` | `/register` | Halaman daftar akun konsumen |
| `POST` | `/register` | Proses daftar (400 + pesan kalau isian tidak valid) |
| `GET` | `/logout` | Hapus sesi, kembali ke halaman masuk |
| `GET` | `/` | Melayani antarmuka SPA Web (wajib login; 302 ke `/login`) |
| `GET` | `/api/chain` | Mengambil seluruh blok dan status integritas rantai |
| `POST` | `/api/block/petani` | Mencatat transaksi panen baru dari petani |
| `POST` | `/api/block/distributor` | Mencatat pergerakan logistik transit dari distributor |
| `GET` | `/api/trace/<batch_id>` | Menelusuri seluruh riwayat batch dan deteksi suhu |
| `POST` | `/api/tamper` | Simulasi manipulasi data pada blok target |
| `POST` | `/api/reset` | Mereset buku besar kembali ke Genesis Block |

---

## 🧭 Peta File — mau ngutak-atik apa, buka file mana

| Mau ubah | File | Catatan |
|---|---|---|
| Tampilan halaman (tab, tombol, warna) | `templates/index.html` | HTML + CSS (Tailwind) + JavaScript halaman utama |
| Halaman login | `templates/login.html` | kartu masuk + tombol isi akun demo |
| Endpoint API, validasi, aturan peran | `app.py` | satu file Flask: rute, guard login, `USERS` |
| Cara blok & hash dibuat | `blockchain.py` | `compute_hash`, `add_block`, `is_chain_valid`, `trace_batch` |
| Data buku besar (jangan diedit manual) | `ledger_data.json` | diubah lewat aplikasi; reset pakai tombol di tab Uji Ubah |
| Uji otomatis API | `tests/e2e_api.py` | jalankan `python tests/e2e_api.py` (40 cek) — tes menyalakan server sendiri di port 5099 dengan ledger sementara, jadi **data asli tidak terhapus** |
| Dokumentasi | `docs/` | plan, arsitektur, ui-spec, panduan klik (md/docx/pdf) |

## 💻 Ngoding pakai VS Code

1. Double-click **`buka-vscode.bat`** → folder proyek langsung terbuka di VS Code
2. Double-click **`run-agrichain-dev.bat`** → server hidup dengan **auto-reload**
   - file `.py` diubah → server restart sendiri
   - file `.html` diubah → cukup refresh browser
3. Edit file, simpan (`Ctrl+S`), refresh browser (`F5`) di `http://127.0.0.1:5000`
4. Kalau mau pakai tombol Run di VS Code: pilih konfigurasi **"SimpleAgriChain (auto-reload)"** lalu tekan `F5`
5. Selesai ngoding: double-click **`stop-agrichain.bat`**; untuk demo pakai **`run-agrichain.bat`** (mode normal, tanpa debug)

Python sudah tersedia di dalam proyek: `.venv\Scripts\python.exe` — tidak perlu install apa pun lagi.

## 🧾 Daftar Akun Konsumen (register)

Siapa pun bisa membuat akun sendiri dari halaman **`/register`** (di halaman Masuk ada tautan *"Belum punya akun? Daftar sebagai konsumen"*).

| Isian | Aturan |
|---|---|
| Username | 3–20 karakter, huruf kecil/angka/garis bawah, harus unik |
| Nama tampilan | wajib, maksimal 40 karakter |
| Password | minimal 8 karakter, harus diketik dua kali dan sama |

- Akun baru **selalu berperan `user` (konsumen)** — tidak bisa mencatat transaksi. Akun admin hanya dibuat lewat file `users.json` (akun awal `admin/admin123`).
- Password disimpan sebagai hash (`werkzeug`), bukan teks biasa.
- Akun tersimpan di **`users.json`** sehingga tetap ada setelah server dimatikan/dinyalakan lagi.
- Setelah daftar, diarahkan ke halaman Masuk dengan pesan "Akun berhasil dibuat".

## 🌐 Akses dari HP / laptop lain (satu jaringan)

Aplikasi sudah mendengarkan di semua antarmuka (`0.0.0.0`), jadi bisa dibuka dari perangkat lain selama satu jaringan (Wi-Fi rumah, Wi-Fi kampus, atau hotspot HP).

1. **Sekali saja:** double-click **`izinkan-jaringan.bat`** → muncul jendela izin Administrator → klik **Yes**. Aturan firewall dibuat untuk **semua tipe jaringan**, karena Wi-Fi kampus/hotspot sering dikategorikan *Public* oleh Windows.
2. Sambungkan HP/laptop ke jaringan yang **sama** dengan komputer ini.
3. Double-click **`run-agrichain.bat`**. Di jendela hitam akan tertulis:

```
  AgriChain siap diakses:
  - Komputer ini : http://127.0.0.1:5000
  - Perangkat lain: http://192.168.3.137:5000
```

4. Di HP, buka alamat **"Perangkat lain"** itu di browser → muncul halaman Masuk, dan alamatnya juga ditampilkan di kartu hijau halaman login.
5. Login `admin/admin123` atau `user/user123` seperti biasa — data yang sama, buku besar yang sama.

Catatan:
- Ganti jaringan (misal pindah ke hotspot HP) → **matikan lalu jalankan lagi** `run-agrichain.bat` supaya alamat IP yang tertulis ikut berubah.
- Kalau HP tidak bisa membuka: pastikan satu jaringan, `izinkan-jaringan.bat` sudah dijalankan, dan Windows Firewall tidak memblokir.
- Cek cepat dari komputer: `curl http://<alamat-lan>:5000/healthz` → `{"ok": true, ...}`.

## 📄 Dokumen untuk Presentasi

| Dokumen | Isi |
|---|---|
| `docs/Presentasi-AgriChain.pdf` / `.docx` (25 halaman) | Alasan memilih tema, masalah yang dijawab, dasar rantai blok tanpa istilah teknis, struktur kode beserta potongan kodenya, cara menyambung banyak perangkat, perbandingan Solidity+Docker vs Python, dan alur pemakaian web |
| `docs/Panduan-Klik-SimpleAgriChain.pdf` / `.docx` | Panduan klik langkah demi langkah untuk demo |
| `docs/architecture.md` | Kontrak API, skema data, keputusan teknis |
| `docs/ui-spec.md` | Spesifikasi tampilan |
| `docs/verifikasi-final.md` | Catatan verifikasi dan bukti angka |

## 📂 Struktur File

```
C:\Ouput Shiro\SimpleAgriChain\
├── .venv/                           # Python Virtual Environment
├── docs/                            # Dokumentasi SDLC (brief, plan, architecture, ui-spec)
├── notebook/
│   └── SimpleAgriChain_Colab.ipynb  # Notebook Colab 3 skenario
├── templates/
│   └── index.html                   # Antarmuka SPA 4 Tab
├── tests/
│   └── e2e_api.py                   # Uji API end-to-end (35 cek, stdlib)
├── app.py                           # Server Flask & Controller REST API
├── blockchain.py                    # Core Blockchain Engine & SHA-256 Hashing
├── ledger_data.json                 # Penyimpanan buku besar lokal
├── requirements.txt                 # Dependensi Python (Flask)
├── run-agrichain.bat                # Launcher mode normal (untuk demo)
├── run-agrichain-dev.bat            # Launcher mode ngoding (auto-reload)
├── stop-agrichain.bat               # Stopper
├── buka-vscode.bat                  # Buka folder proyek di VS Code
├── .vscode/launch.json              # Konfigurasi Run/Debug VS Code (F5)
└── README.md                        # Panduan Teknis
```
