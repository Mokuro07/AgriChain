# VERIFIKASI FINAL — SimpleAgriChain Web

**Tanggal verifikasi:** 15 November 2026, 01:00–01:10 WIB
**Verifikator:** @default (AG-00 Orchestrator)
**Lingkungan:** Windows 11, `.venv` Python + Flask 3.1.3, port 5000, Chromium (headless CDP + viewport 390×844)
**Status:** LULUS — aplikasi jalan, semua alur UI berfungsi, nol error JavaScript

---

## 1. Bukti Runtime

| Aspek | Perintah / Aksi | Hasil Nyata |
|---|---|---|
| Server hidup | `.venv\Scripts\python.exe app.py` | `Running on http://127.0.0.1:5000`, `GET / -> 200` |
| Launcher double-click | `run-agrichain.bat` | Polling port sukses → `Server siap!` → browser default terbuka (`GET / 200` di log) |
| Stopper | `stop-agrichain.bat` | `Server berhasil dihentikan.` → port 5000 kosong |
| Persistensi | `ledger_data.json` | Reset bersih: 1 blok Genesis, hash `43e8bdcc…`, `is_valid: true` |

## 2. Uji API End-to-End — 35/35 PASS

Skrip: `tests/e2e_api.py` (stdlib `urllib`, tanpa dependensi tambahan)

```
cd "C:\Ouput Shiro\SimpleAgriChain"
.venv\Scripts\python.exe tests\e2e_api.py
→ ==== HASIL: 35/35 PASS ====
```

Cakupan: CRUD blok petani/distributor, duplikat batch, orphan batch, traceability, alert kadar air (>14%) & suhu (>25°C), validasi tanggal/angka/rentang/tipe, payload kosong, payload non-dict, tamper + deteksi `tampered_indices`, reset, 404 aman.

## 3. Uji UI Nyata (browser, bukan asumsi)

| Alur | Bukti DOM |
|---|---|
| Load awal | 4 tab terdaftar, `metric-total-blocks = 1`, badge `● CATATAN UTUH, TIDAK BERUBAH`, feed 1 kartu |
| Submit form Petani | Toast `Catatan panen berhasil disimpan ke buku besar!`, blok 1 → 2 |
| Submit form Distributor (35°C) | Toast `Catatan pengiriman berhasil disimpan…`, blok 2 → 3, feed 3 kartu, badge tetap hijau |
| Trace batch | Timeline 2 item, banner `ADA TANDA RISIKO MUTU… suhu transit mencapai 35°C, melebihi batas toleransi 25°C` |
| Trace batch tak ada | State `Batch ID 'ORG-NOPE-000' tidak ditemukan dalam buku besar` |
| Tamper (Catatan #1) | Banner `TERDETEKSI: CATATAN INI SUDAH DIUBAH SETELAH MASUK BUKU … Nomor yang bermasalah: #1`, badge jadi `▲ ADA CATATAN BERUBAH` |
| Tombol preset demo | `prefillPetani` (12.5%), `prefillPetaniBasah` (18%), `prefillDistributor` (35.0), `prefillDistributorBohong` (15.0), `prepareTamperScenario` (index 2) — semua terisi benar |
| Error JavaScript | `window.__errs = []` di seluruh alur |
| Layout HP 390×844 | `scrollWidth == clientWidth == 390` (tanpa overflow horizontal), nav tab `overflow-x: auto` bisa digeser sampai Tab 4 |

## 4. Catatan Kontrak

`POST /api/tamper` memakai body `{"block_index": int, "modified_data": {…}}` — sudah sesuai `docs/architecture.md` dan sudah sesuai yang dikirim `templates/index.html`. Body bentuk lama (`field`/`new_value`) ditolak 400, bukan bug.

## 5. Sisa Pekerjaan (opsional, tidak menghalangi demo)

1. Laporan praktikum `.docx` — belum dibuat untuk revisi ini (dokumen SDLC sudah lengkap di `docs/`).
2. `demo/` masih folder kosong — boleh dihapus.
3. Deploy publik (Render/Railway) — belum, masih lokal `127.0.0.1:5000`.


---

## 6. Revisi UI (15 Nov 2026, setelah verifikasi awal)

Pengguna menilai UI terlalu ramai. Penyederhanaan diterapkan dan diuji ulang:

- Tab 1: pemilih peran, satu formulir tampil (12 → 7 field terlihat), 210 → 96 kata
- Tab 2: kotak pencarian di atas, panel penjelasan dilipat (`<details>`), 252 → 58 kata
- Tab 3: 3 kartu metrik → satu strip ringkas
- Navigasi dipendekkan: `1 · Input`, `2 · Lacak`, `3 · Buku Besar`, `4 · Uji Ubah` (935 → 548 px di 390 px)
- Regresi API: `tests/e2e_api.py` → **35/35 PASS** setelah perubahan UI
- Uji browser ulang: submit petani (blok 1→2), submit distributor (2→3), trace alert 35°C, tamper → badge `▲ ADA CATATAN BERUBAH`, `window.__errs = []`
- Tinggi Tab 1: 1121 px (dua form) → 881 px (satu form). Mobile 390 px: tanpa overflow horizontal
- Tangkapan layar: `docs/screenshots/05-ui-baru-tab1-petani.png`, `06-…-distributor.png`, `07-…-tab2-lacak.png`, `08-ui-baru-mobile.png`


---

## 7. Revisi Perataan (Presisi) — 15 Nov 2026

- Satu kolom terpusat `max-w-3xl` untuk header, nav, dan `<main>`; semua sumbu tengah terukur 713 px pada viewport 1425 px (selisih ≤ 1 px).
- Badge status jadi satu grup dengan judul: satu baris di desktop (jarak 12 px dari judul), turun ke baris kedua ter-center di mobile 390 px (`cx = 195`).
- Teks badge diringkas: `● CATATAN UTUH` / `▲ ADA CATATAN BERUBAH`.
- Metrik Tab 3 diringkas: `UTUH` / `BERUBAH`.
- Regresi: `tests/e2e_api.py` **35/35 PASS**, `window.__errs = []`, mobile `scrollWidth == clientWidth == 390`.
- Tangkapan layar: `09-rapih-desktop-tab1.png`, `10-rapih-desktop-badge-berubah.png`, `11-rapih-mobile.png`, `12-rapih-desktop-tab3.png`, `13-rapih-desktop-tab2.png`.


---

## 8. Realisasi Desain ke Web — 15 Nov 2026

Desain FigCraft (`agrichain-v2`) diterapkan ke `templates/index.html`:

- Header 114 px (desain 112), brand di `x=137`, badge 26 px sejajar judul, nav ter-center
- Label nav tanpa angka; tab 32 px di desktop, 44 px di mobile (touch target dipertahankan)
- Judul halaman dihapus di Tab 1, 3, 4 (sesuai desain); Tab 2 tetap
- Jarak: 28 px header→konten, 16 px antar kartu, 32 px padding bawah
- Uji ulang: API 35/35 PASS, submit petani/distributor, trace alert, tamper badge BERUBAH, `window.__errs` kosong, mobile `scrollWidth == clientWidth == 390`
- Screenshot: `14-web-desktop-tab2.png`, `15-web-desktop-tab1.png`, `16-web-desktop-tab3.png`, `17-web-desktop-tab4-tamper.png`, `18-web-mobile.png`


---

## 9. Login & Pemisahan Peran — 15 Nov 2026

- `templates/login.html` baru; `/login` (GET/POST) dan `/logout` ditambahkan di `app.py`.
- Gerbang akses: tanpa sesi halaman → 302, tanpa sesi API → 401; `user` melakukan POST tulis → 403.
- UI dirender per peran: tab Input & Uji Ubah hanya untuk admin (beserta section-nya), badge peran + tombol Keluar di header.
- `tests/e2e_api.py` diperluas: login admin, gerbang anonim, dan uji batas peran `user` → **40/40 PASS**.
- Screenshot: `22-web-user-dashboard.png`, `23-web-login.png`, `24-web-admin-dashboard.png`, `25-web-login-mobile.png`.


---

## 10. Tampilan Konsumen untuk Peran `user` — 15 Nov 2026

- Halaman awal `user` = Lacak; navbar 2 tab (Lacak, Buku Besar); Dashboard, Input, Uji Ubah tidak dirender.
- Kartu baru **"Asal & penanganan"** (8 baris data) khusus konsumen pada hasil pelacakan.
- Label pencarian diganti copy konsumen + hint Batch ID ada di kemasan/QR.
- Alur QR: `/?batch=X` → `302 /login?next=...` → login → redirect balik ke `/?batch=X` → hasil otomatis tampil.
- `/logout` dibuat publik agar tidak terjadi loop login.
- Regresi `tests/e2e_api.py` → **40/40 PASS**; nol error JS; mobile 390 px tanpa overflow.
- Screenshot: `26-web-konsumen-lacak.png`, `27-web-konsumen-hasil.png`, `28-web-konsumen-mobile.png`.


---

## 11. Audit UI/UX Pro Max & Perbaikan — 15 Nov 2026

- Audit DOM nyata (bukan asumsi): 6 layar diperiksa, **4 pelanggaran kontras** + **10 emoji sebagai ikon** ditemukan.
- Perbaikan: emerald-600→700 (3.77→**5.48:1**), sky-600→700 (4.10→**5.93:1**), slate-400→600 (2.56→**7.58:1**), placeholder→slate-500 (2.56→**4.76:1**); semua emoji → SVG inline; `aria-busy` pada 4 handler; `:focus-visible` global; `prefers-reduced-motion`.
- Audit ulang: **0 pelanggaran kontras, 0 emoji** di login + 5 tab; `aria-busy` terbukti `true` saat proses (fetch diperlambat 900 ms) dan `false` setelah selesai.
- Design system dipersist: `design-system/simpleagrichain/MASTER.md`.
- Regresi: `tests/e2e_api.py` **40/40 PASS**, nol error JS, mobile 390 px tanpa overflow.
- Screenshot: `29-web-tab1-svg-icons.png`, `30-web-tab3-kontras.png`, `31-web-tab4-svg.png`, `32-web-dashboard-final.png`, `33-web-login-final.png`, `34-web-login-mobile-final.png`.


---

## 12. Data Setelah Logout & Akses Konsumen — 16 Nov 2026

- Terbukti data **tidak hilang**: admin 3 blok → logout → login admin → tetap 3 blok; restart server → tetap; `user` membaca 3 blok.
- Penyebab kesan "reset": (a) tab Lacak konsumen tidak punya daftar batch, (b) `tests/e2e_api.py` mereset server port 5000 setiap dijalankan.
- Perbaikan: kartu **"Batch yang sudah tercatat"** (dinamis dari buku besar, bisa diklik), `switchTab(2)` ikut memuat data, dan tes kini memakai **server sendiri di port 5099** + `AGRICHAIN_LEDGER` sementara.
- Bukti: admin 5 blok/2 batch → logout → login admin → tetap → login user → daftar 2 batch → klik → hasil lacak 8 baris → Buku Besar konsumen 5 catatan UTUH. `tests/e2e_api.py` **40/40 PASS** dan `ledger_data.json` tetap 5 blok.
- Screenshot: `39-konsumen-daftar-batch.png`, `40-konsumen-hasil.png`.


---

## 13. Sistem Register Akun — 16 Nov 2026

- Akun pindah dari dict di kode ke **`users.json`** (hash `werkzeug`, atomic write, path bisa dialihkan via `AGRICHAIN_USERS`).
- Endpoint baru `GET/POST /register`; akun baru **selalu** role `user`.
- Validasi: username 3–20 (`[a-z0-9_]`), unik, nama wajib, password ≥ 8, konfirmasi sama.
- Halaman Masuk mendapat tautan "Daftar sebagai konsumen" + pesan sukses setelah daftar.
- Bukti browser: `/register` 200 → daftar valid → `/login?registered=1` + pesan sukses → login akun baru → 2 tab, badge USER, `POST` → **403**.
- `tests/e2e_api.py` diperluas dengan 8 cek register → **48/48 PASS**; server uji kini memakai port acak + `users.json` sementara sehingga akun & data asli aman.
- Screenshot: `42-halaman-daftar.png`, `43-daftar-berhasil.png`, `44-login-akun-baru.png`.


---

## 14. Realisasi Mockup v3 ke Web — 22 Nov 2026

- Masuk dan Daftar: kartu alamat LAN, blok akun demo, judul + paragraf penjelasan dihapus (mengikuti mockup).
- Header: chip alamat LAN dihapus untuk semua peran.
- Navbar: 5 tab dirender untuk semua peran; untuk konsumen tiga tab admin memakai `aria-disabled="true"` + gaya `text-slate-300` + `title="Khusus admin"`.
- Bukti browser: admin `nonaktif=0`; user `nonaktif=3`, klik Input tidak membuka panel, tab Lacak tetap memuat 2 batch.
- Tanpa overflow horizontal di 1440 dan 390. `tests/e2e_api.py` **48/48 PASS** (satu cek register disesuaikan karena judul halaman dihapus).
- Screenshot: `45-web-admin-navbar.png`, `46-web-user-navbar.png`.
