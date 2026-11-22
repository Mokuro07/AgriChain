# PANDUAN KLIK — Cara Kerja SimpleAgriChain dari Awal sampai Selesai

Dokumen ini menuliskan **tombol mana yang ditekan** dan **apa yang terjadi di balik layar** pada setiap langkah.
Semua angka di bagian "bukti" diambil dari eksekusi nyata di browser (15 Nov 2026), bukan perkiraan.

---

## 0. Menyalakan aplikasi

1. Buka folder `C:\Ouput Shiro\SimpleAgriChain\`
2. **Double-click `run-agrichain.bat`**
   - Muncul jendela hitam, tulisan `[SimpleAgriChain] Menunggu server aktif di port 5000...`
   - Setelah ±3 detik: `[SimpleAgriChain] Server siap! Membuka browser default...`
   - Browser terbuka sendiri di **halaman Masuk** (`http://127.0.0.1:5000/login`)
3. Untuk mematikan: double-click `stop-agrichain.bat`

**Akun:**

| Username | Password | Peran |
|---|---|---|
| `admin` | `admin123` | operator — boleh mencatat, menguji ubah data, reset |
| `user` | `user123` | konsumen — hanya memeriksa |

---

## BAGIAN A — Sisi Admin (operator yang mencatat)

### Langkah 1 — Masuk sebagai admin

- **Klik:** kotak "Akun demo" baris `admin / admin123` → tombol **Isi →**, lalu **Masuk**
- **Yang terlihat:** halaman **Dashboard**, navbar 5 tab: `Dashboard · Input · Lacak · Buku Besar · Uji Ubah`; pojok kanan ada badge **ADMIN** dan tombol **Keluar**
- **Di balik layar:** `POST /login` → server mencocokkan password hash → sesi Flask dibuat (`session["role"]="admin"`) → redirect ke `/`
- **Bukti:** `GET /login` → 200; setelah submit, `location.pathname = /`, tab = 5 buah

### Langkah 2 — Lihat kondisi awal Dashboard

- **Klik:** tab **Dashboard**
- **Yang terlihat:** Catatan di buku = **1**, Batch terdaftar = **0**, Keutuhan = **UTUH**, Peringatan mutu = **aman**, Aktivitas = "Belum ada transaksi"
- **Di balik layar:** `GET /api/chain` → 1 blok (Genesis, index 0) → JS menghitung angka dari data itu (tanpa endpoint tambahan)

### Langkah 3 — Mulai mencatat panen

- **Klik:** tab **Input** → pastikan tombol peran **Petani — catat panen** aktif (hanya satu formulir yang tampil)
- **Klik:** **Isi Contoh Beras Organik**
- **Yang terlihat:** form terisi otomatis: `Batch ID = ORG-BRS-001`, `Komoditas = Beras Merah Organik`, `Kadar Air = 12.5`
- **Di balik layar:** hanya mengisi field di browser (belum ada data yang dikirim)

### Langkah 4 — Simpan catatan panen

- **Klik:** **Simpan Catatan Panen**
- **Yang terlihat:** tombol jadi spinner sebentar → toast hijau **"Catatan panen berhasil disimpan ke buku besar!"** → jumlah catatan di navbar/`Dashboard` naik jadi **2**
- **Di balik layar:**
  1. `POST /api/block/petani` dengan JSON form
  2. Server memvalidasi (field wajib, tanggal, kadar air 0–100, batch belum pernah ada)
  3. `blockchain.py` membuat blok baru: `index=1`, `actor=PETANI`, `previous_hash` = hash blok #0
  4. Hash dihitung: `sha256(json.dumps({index,timestamp,batch_id,actor,data,previous_hash}, sort_keys=True))`
  5. `ledger_data.json` ditulis ulang (atomic)
  6. Browser memuat ulang rantai → kartu blok baru muncul
- **Bukti:** toast tampil, `total_blocks` 1 → **2**, blok #1 actor `PETANI`

### Langkah 5 — Catat pengiriman (peran Distributor)

- **Klik:** tombol peran **Distributor — catat kirim** → **Isi Contoh Pengiriman Hangat**
- **Yang terlihat:** `Target Batch ID = ORG-BRS-001`, `Suhu Transit = 35.0`
- **Klik:** **Perbarui Status Logistik ke Rantai**
- **Yang terlihat:** toast **"Catatan pengiriman berhasil disimpan ke buku besar!"** → total **3**
- **Di balik layar:** `POST /api/block/distributor` → validasi (batch harus sudah ada di hulu) → blok #2 dibuat, `previous_hash` = hash blok #1
- **Catatan penting:** suhu 35 °C **sengaja** di atas batas 25 °C supaya muncul peringatan di langkah berikutnya

### Langkah 6 — Dashboard ikut berubah

- **Klik:** tab **Dashboard**
- **Yang terlihat:** Catatan = **3**, Batch = **1**, Peringatan mutu = **1 batch** (berisi `ORG-BRS-001 · suhu 35°C > 25°C`, bisa diklik), Aktivitas terakhir = 2 baris
- **Di balik layar:** `renderDashboard()` dipanggil setiap kali data rantai selesai dimuat

---

## BAGIAN B — Sisi Konsumen (memeriksa)

### Langkah 7 — Cari batch

- **Klik:** tab **Lacak** → isi `ORG-BRS-001` → **Lacak Komoditas**
- **Yang terlihat:** kartu **Beras Merah Organik**, banner oranye **"ADA TANDA RISIKO MUTU PADA BATCH INI:"** berisi *suhu transit mencapai 35 °C melebihi batas 25 °C*, lalu timeline 2 langkah (PETANI → DISTRIBUTOR) dan QR
- **Di balik layar:** `GET /api/trace/ORG-BRS-001` → server mengumpulkan semua blok batch itu, menghitung `max_temperature`, `kadar_air_max`, dan `risk_sources` → browser menggambar banner + timeline

### Langkah 8 — Periksa keutuhan di Buku Besar

- **Klik:** tab **Buku Besar**
- **Yang terlihat:** strip `Jumlah catatan 3 · Keutuhan ● UTUH` lalu 3 kartu: **Catatan #0** (AWAL BUKU / SYSTEM), **#1** (PETANI), **#2** (DISTRIBUTOR). Tiap kartu menampilkan isi JSON, **Sidik jari catatan sebelumnya** dan **Sidik jari digital catatan ini**
- **Di balik layar:** `GET /api/chain` → tiap blok ditampilkan; server juga mengembalikan `is_valid` hasil pengecekan ulang semua hash

---

## BAGIAN C — Uji apakah catatan bisa diubah diam-diam

### Langkah 9 — Coba ubah catatan lama

- **Klik:** tab **Uji Ubah** → **Muat Contoh Ubah Suhu**
- **Yang terlihat:** `Pilih Nomor Catatan = 2` dan kotak JSON terisi data pengiriman
- **Klik:** **Coba Ubah Catatan Ini**
- **Yang terlihat:** kotak merah **"TERDETEKSI: CATATAN INI SUDAH DIUBAH SETELAH MASUK BUKU"** + *Status Catatan: BERUBAH / TIDAK COCOK | Nomor yang bermasalah: #2*; badge pojok kanan berubah jadi **▲ ADA CATATAN BERUBAH**
- **Di balik layar:** `POST /api/tamper` → isi blok #2 ditimpa **tanpa** memperbarui hash-nya → `is_chain_valid()` menghitung ulang hash blok #2, hasilnya tidak cocok → `is_valid=false`, `tampered_indices=[2]`

### Langkah 10 — Buktikan di Buku Besar

- **Klik:** tab **Buku Besar**
- **Yang terlihat:** strip berubah jadi **BERUBAH**, kartu **Catatan #2** diberi bingkai merah + label **DIUBAH / RUSAK**, kotak sidik jarinya ikut merah

### Langkah 11 — Kembalikan ke kondisi bersih

- **Klik:** tab **Uji Ubah** → **Kosongkan Buku, Mulai dari Awal** → konfirmasi **OK**
- **Yang terlihat:** badge kembali **● CATATAN UTUH**, Dashboard: Catatan = **1**, Batch = **0**
- **Di balik layar:** `POST /api/reset` → rantai dibuat ulang hanya dengan Genesis Block, `ledger_data.json` ditimpa

---

## BAGIAN D — Konsumen memakai aplikasi

### Langkah 12 — Keluar dan masuk sebagai konsumen

- **Klik:** **Keluar** (kanan atas) → di halaman Masuk klik baris `user / user123` → **Isi →** → **Masuk**
- **Yang terlihat:** langsung ke tab **Lacak**, navbar hanya 2 tab: `Lacak · Buku Besar`; badge **USER**. Tab Input, Dashboard, dan Uji Ubah tidak ada
- **Di balik layar:** template dirender ulang sesuai `role`; server juga menolak (403) kalau konsumen mencoba mengirim data

### Langkah 13 — Lacak lewat QR (alur dunia nyata)

- Buka `http://127.0.0.1:5000/?batch=ORG-BRS-001` (ini isi QR di kemasan)
- **Yang terlihat:** diarahkan ke halaman Masuk dulu, lalu setelah login **otomatis kembali** ke batch itu dan hasilnya langsung tampil
- **Di balik layar:** guard menyimpan tujuan (`/login?next=/?batch=...`), setelah login diarahkan balik, JS membaca parameter `batch` dan menjalankan pelacakan otomatis

### Langkah 14 — Hasil yang dilihat konsumen

- **Yang terlihat:** banner risiko, kartu komoditas + QR, kartu **Asal & penanganan** (lokasi lahan, tanggal panen, pupuk, sertifikat, kadar air, suhu tertinggi, rute, kondisi muatan), lalu timeline perjalanan
- **Catatan:** konsumen tidak melihat tombol mencatat apa pun — hanya memeriksa

---

## Ringkasan alur data (satu baris per tahap)

```
Form di browser
   → POST /api/block/petani atau /api/block/distributor
   → app.py validasi (field, tanggal, angka, batch unik/terikat)
   → blockchain.py membuat blok + hash SHA-256 (terikat hash blok sebelumnya)
   → ledger_data.json ditulis ulang
   → GET /api/chain / GET /api/trace/<batch>
   → browser menggambar Dashboard, Lacak, Buku Besar
```

**Yang dijamin sistem:** catatan yang sudah masuk tidak bisa diubah tanpa ketahuan (dibuktikan Langkah 9–10).
**Yang tidak dijamin:** apakah angka yang diketik pertama kali itu jujur — semua angka diketik manual manusia.

---

## Urutan klik tercepat untuk demo (10 menit)

| Menit | Yang dilakukan |
|---|---|
| 0–1 | `run-agrichain.bat` → login admin |
| 1–2 | Dashboard (lihat kondisi awal) |
| 2–4 | Input → Petani → preset → Simpan |
| 4–6 | Distributor → preset hangat → Perbarui |
| 6–7 | Dashboard (angka & peringatan berubah) |
| 7–8 | Lacak `ORG-BRS-001` (banner risiko) |
| 8–9 | Buku Besar (hash & status) |
| 9–10 | Uji Ubah → tamper → Buku Besar berubah → Reset |
| 10 | Keluar → login `user` → Lacak (tampilan konsumen) |

---

## Kalau ada masalah

| Gejala | Penyebab | Solusi |
|---|---|---|
| Jendela hitam: "Server gagal merespons di port 5000" | port 5000 masih dipakai proses lama / server gagal start | `stop-agrichain.bat`, lalu `run-agrichain.bat` lagi |
| Browser balik ke halaman Masuk padahal baru masuk | sesi kedaluwarsa (browser ditutup / cookie dihapus) | masuk ulang; aplikasi otomatis kembali ke halaman terakhir |
| Perubahan HTML tidak terlihat | server mode normal menyimpan cache template | pakai `run-agrichain-dev.bat`, atau restart |
| "Koneksi ke node AgriChain terputus" | server sudah mati | jalankan `run-agrichain.bat` |
| Ingin mengosongkan data | — | admin → tab Uji Ubah → Kosongkan Buku |

Catatan teknis: launcher mengecek kesiapan server lewat `/healthz` (endpoint publik). Sebelumnya launcher memeriksa `/api/chain` yang sekarang butuh login, sehingga muncul deretan `401` di log dan launcher berhenti dengan pesan "gagal merespons".

---

## Catatan tambahan (16 Nov 2026)

- Di tab **Lacak** sekarang ada kartu **"Batch yang sudah tercatat"**: daftar semua batch yang sudah diisi admin, bisa diklik langsung. Konsumen tidak perlu tahu Batch ID lebih dulu.
- Data **tidak hilang** setelah logout. Yang dulu bikin bingung: (a) tab Lacak tidak menampilkan daftar batch, (b) skrip `tests/e2e_api.py` dulu mereset server yang sedang jalan. Sekarang tes memakai server sendiri (port 5099) dan ledger sementara, jadi data demo aman.

---

## Akses dari HP / laptop lain (satu jaringan)

Aplikasi bisa dibuka dari perangkat lain di jaringan yang sama (Wi-Fi atau hotspot HP).

1. **Sekali saja:** double-click `izinkan-jaringan.bat` → klik **Yes** pada jendela izin Administrator (membuka port 5000)
2. Sambungkan HP/laptop ke jaringan yang sama
3. Double-click `run-agrichain.bat` → di jendela hitam tertulis:
   - `Komputer ini : http://127.0.0.1:5000`
   - `Perangkat lain: http://192.168.x.x:5000`
4. Di HP buka alamat **Perangkat lain** itu → halaman Masuk (alamatnya juga tampil di kartu hijau)
5. Login seperti biasa; data dan buku besar sama

Kalau pindah jaringan, matikan lalu jalankan lagi `run-agrichain.bat` supaya alamat IP yang tertulis ikut berubah.

---

## Daftar akun sendiri (konsumen)

1. Di halaman Masuk, klik **"Daftar sebagai konsumen"**
2. Isi: Username (3–20 huruf kecil/angka/garis bawah), Nama tampilan, Password (minimal 8 karakter) dua kali
3. Klik **Daftar** → kembali ke halaman Masuk dengan pesan "Akun berhasil dibuat"
4. Masuk dengan akun baru → navbar hanya **Lacak** dan **Buku Besar** (peran USER). Mencatat transaksi tetap hanya untuk admin.
5. Akun tersimpan di `users.json`, jadi tetap ada setelah server dimatikan.

Catatan: peran **admin tidak bisa** dibuat lewat form daftar (sengaja), hanya akun awal `admin` di `users.json`.
