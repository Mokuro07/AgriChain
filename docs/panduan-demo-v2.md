# PANDUAN DEMO v2 — SimpleAgriChain Web (setelah revisi adil)

Semua yang tertulis di sini sudah diuji langsung di mesin ini. Angka dan potongan teks diambil dari
hasil nyata, bukan karangan.

**Perubahan besar dari versi sebelumnya:** sistem dan narasinya sekarang NETRAL. Petani dan distributor
sama-sama bisa jadi sumber risiko, dan sistem juga jujur menyebut apa yang TIDAK bisa dijaminnya.

---

## 1. Kenapa versi ini direvisi

Versi pertama punya tiga lubang yang ditemukan saat review:

1. Ceritanya bias — seolah petani tidak mungkin salah, distributor selalu yang salah.
2. Petani punya lubang yang persis sama: **kadar air panen**. Beras dipanen terlalu basah (> 14%) akan
   berjamur di jalan walau suhu truk distributor dingin dan benar. Nilainya pun diketik petani sendiri.
3. Pertanyaan kunci: siapa yang menentukan angka suhu truk? Jawaban jujur: operator distributor,
   diketik manual. Jadi angkanya bisa bohong sejak awal, dan sistem ini TIDAK bisa mendeteksinya.

Revisi ini menjawab ketiganya: tambah kadar air sebagai sumber risiko hulu, nilai dua sumber risiko
secara seimbang, dan menyatakan batas kepercayaan secara terbuka di UI.

---

## 2. Cara pakai (tidak berubah)

1. Klik ganda **`SimpleAgriChain.lnk`** di Desktop (atau `run-agrichain.bat` di folder
   `C:\Ouput Shiro\SimpleAgriChain\`).
2. Jendela hitam muncul, tunggu sampai browser otomatis terbuka ke `http://127.0.0.1:5000`.
3. Selesai: klik ganda **`stop-agrichain.bat`**, tekan Enter saat muncul "Press any key".

---

## 3. Dua hal berbeda yang sering dicampur — INI INTI SEMUANYA

| | Dijamin sistem ini? |
|---|---|
| Catatan yang sudah masuk tidak bisa diubah/dihapus diam-diam | **YA** (itu gunanya sidik jari digital / hash chain) |
| Angka yang ditulis pertama kali itu benar dan jujur | **TIDAK.** Semua angka diketik manual oleh manusia |

Tab 2 sekarang menampilkan penjelasan ini dalam bahasa awam, termasuk analogi:

> "Buku besar ini seperti buku catatan yang halamannya direkatkan lem super: nggak bisa dihapus atau
> ditimpa. Tapi kalau sejak awal ditulis angka bohong, tulisan bohong itu juga ikut terkunci rapi."

---

## 4. NARASI DEMO — urutan klik

> **Baru:** aplikasi sekarang terbuka di tab **Dashboard** (ringkasan: jumlah catatan, batch terdaftar, keutuhan, peringatan mutu, aktivitas terakhir). Untuk mulai demo, klik **Input** di navbar.

### Bagian A — Lihat dulu apa yang TIDAK dijamin (Tab 2)
Buka Tab 2. Kotak pencarian ada paling atas; panel "Sejauh mana sistem ini bisa dipercaya?" sekarang **terlipat** — klik untuk membuka. Isinya:
yang dijamin (catatan tidak bisa diubah), yang tidak dijamin (kebenaran angka saat pertama diketik),
dan apa yang dibutuhkan di dunia nyata (sensor yang mencatat sendiri + tanda tangan digital, atau auditor
pihak ketiga).

Narasi: *"Sebelum masuk demo, saya jujur dulu soal batas sistem ini. Yang dijamin: catatan yang sudah
masuk nggak bisa diubah diam-diam. Yang tidak dijamin: apakah angka yang diketik itu jujur, karena
semuanya diketik manual manusia."*

### Bagian B — Petani bisa jadi sumber masalah (Tab 1, peran Petani)
Di Tab 1, pastikan tombol **🧑‍🌾 Petani — catat panen** yang aktif (hanya satu form yang tampil).
Klik **"💧 Isi Contoh Panen Basah (kadar air 18%)"**. Form terisi dengan kadar air 18%.

Klik **"Simpan Catatan Panen"** → Blok #1, aktor PETANI.

Lalu klik **🚚 Distributor — catat kirim** untuk pindah form, isi dengan **"⚡ Isi Contoh Pengiriman Hangat (>25°C)"** → ubah suhu jadi `24`
(dingin, benar) → klik **"Perbarui Catatan Pengiriman"** → Blok #2.

Buka **Tab 2**, cari batch itu. Hasil nyata:

```
ADA TANDA RISIKO MUTU PADA BATCH INI:
Terindikasi risiko mutu dari tahap panen: kadar air 18.5% melebihi batas aman 14%.
Beras bisa berjamur di jalan walau truknya dingin.

Sumber risiko terdeteksi: tahap panen (Petani). Ini keterangan sumber masalah,
bukan tuduhan ke orang. Semua angka ini diketik manual, jadi bisa saja tidak sesuai kenyataan.
```

Bukti API: `risk_sources: ["PETANI"]`, `has_moisture_alert: true`, `has_temperature_alert: false`.

Narasi: *"Suhu truknya benar, dingin. Tapi produknya tetap bermasalah — karena dipanen terlalu basah.
Jadi sumber risiko bisa dari hulu, bukan selalu dari pengiriman. Perhatikan juga nada kalimatnya:
sistem menyebut sumber masalah, bukan menuduh orang."*

### Bagian C — Dua-duanya sekaligus (Tab 1)
Ulangi dengan batch baru: kadar air 18% DAN suhu 35°C. Hasil API:
`risk_sources: ["PETANI", "DISTRIBUTOR"]`.

Narasi: *"Kalau dua-duanya bermasalah, sistem sebut dua-duanya. Tidak ada yang dibela."*

### Bagian D — PUNCAK: bohong sejak awal (Tab 1 dan Tab 4)

> Catatan UI: Tab 1 hanya menampilkan satu formulir. Pindah peran lewat dua tombol di atas form (Petani / Distributor).
Ini bagian yang menjawab pertanyaan "yang nentuin suhu truk siapa?".

1. Isi form Petani normal (kadar air 12.5%), klik **"Simpan Catatan Panen"**.
2. Klik **"😇 Isi Contoh Distributor Menulis Suhu Aman (bohong sejak awal)"** — form terisi suhu `15.0`.
   Klik **"Perbarui Catatan Pengiriman"**.
3. Lihat header atas: **● CATATAN UTUH**. Tidak ada peringatan merah.
   Bukti API: `is_valid: true`, `tampered_indices: []`.
4. Buka Tab 2, lacak batch itu. Muncul:

```
TIDAK ADA TANDA RISIKO MUTU:
Seluruh angka tercatat dalam batas aman (kadar air ≤ 14%, suhu transit ≤ 25°C). Sertifikat organik SNI terdaftar.
Catatan: sistem hanya memeriksa angka yang ada di buku. Kalau ada angka yang ditulis bohong sejak awal,
sistem tidak bisa membuktikannya dari buku ini saja.
```

Narasi: *"Ini batas sistemnya, dan saya sengaja tunjukkan. Distributor di dunia nyata bisa saja menulis
15 derajat padahal truknya 35. Sistem ini tidak bisa membuktikan kebohongan itu dari buku besar sendiri —
karena tidak ada data pembanding. Yang bisa dilakukan sistem cuma memastikan catatan itu tidak bisa
diubah diam-diam setelah masuk. Untuk menutup celah ini di dunia nyata butuh sensor yang mencatat sendiri
dan ditandatangani digital, atau auditor pihak ketiga. Itu di luar cakupan prototipe ini."*

### Bagian E — Bukti sistem memang bekerja menangkap perubahan (Tab 4)
Buka Tab 4, klik **"⚡ Muat Contoh Ubah Suhu"** → klik **"Coba Ubah Catatan Ini"**. Hasil:
header jadi **▲ ADA CATATAN BERUBAH**, dan muncul:

```
TERDETEKSI: CATATAN INI SUDAH DIUBAH SETELAH MASUK BUKU
Isi Catatan #2 berubah, tetapi sidik jari digitalnya tidak diperbarui — jadi ketidakcocokannya
langsung kelihatan. Status Catatan: BERUBAH / TIDAK COCOK | Nomor yang bermasalah: #2
```

Narasi: *"Bandingkan dengan bagian D. Kalau angka ditulis dari awal, sistem diam. Kalau catatan yang
sudah masuk lalu diubah, sistem langsung menunjuk nomor catatannya. Itu bedanya — dan itulah nilai
sebenarnya dari blockchain untuk kasus ini."*

### Bagian F — Bersih-bersih
Klik **"🔄 Kosongkan Buku, Mulai dari Awal"** di Tab 4. Buku kembali ke satu catatan awal, status hijau.

---

## 5. Bahasa UI yang berubah (biar tidak bingung)

| Istilah lama | Sekarang di UI |
|---|---|
| Blok / Blockchain | Catatan / Buku Besar |
| Genesis Block | Catatan #0 / Awal Buku |
| Hash SHA-256 | Sidik jari digital |
| previous_hash | Sidik jari catatan sebelumnya |
| Ledger | Buku besar |
| Rantai VALID | CATATAN UTUH |
| Rantai INVALID | ADA CATATAN BERUBAH |
| Tab 4 Simulasi Serangan | Tab 4 Uji Coba Ubah Data |

Istilah teknis tetap ada di dokumen (`docs/architecture.md`) untuk keperluan laporan, tapi UI tidak lagi
memakainya tanpa penjelasan.

---

## 6. Hasil pengujian revisi (buktinya)

| No | Uji | Hasil nyata |
|---|---|---|
| 1 | Kadar air 18.5 + suhu 24 | `risk_sources: ["PETANI"]`, `has_temperature_alert: false` — petani bisa jadi sumber risiko |
| 2 | Kadar air 18.5 + suhu 35 | `risk_sources: ["PETANI","DISTRIBUTOR"]` |
| 3 | Distributor tulis suhu 15 sejak awal | `is_valid: true`, `tampered_indices: []` — sistem jujur soal batas |
| 4 | Ubah catatan lama lewat Tab 4 | status jadi ADA CATATAN BERUBAH, nomor catatan ditunjuk |
| 5 | Kadar air kosong / "abc" / -5 / 150 | HTTP 400 semua |
| 6 | Array JSON `[1,2,3]` | HTTP 400 |
| 7 | batch_id duplikat petani | HTTP 400 |
| 8 | Distributor batch tanpa hulu | HTTP 400 |
| 9 | Tamper indeks 999 | HTTP 400 |
| 10 | Teks menuduh satu aktor | 0 hasil di seluruh HTML |
| 11 | Label "Sumber data: diisi manual oleh ..." | ada di tiap entri timeline + tiap kartu Penjelajah |
| 12 | Reset | kembali 1 catatan, UTUH |

---

## 7. Batasan (sebutkan kalau ditanya)

1. Tidak ada mining/proof-of-work/konsensus jaringan — prototipe konsep, bukan jaringan terdistribusi.
2. Penyimpanan satu file JSON lokal (`ledger_data.json`), satu penulis.
3. **Tidak ada auth.** Tab input terbuka; siapa pun bisa menulis selama server jalan. Di produksi tiap
   aktor butuh identitas + tanda tangan digital.
4. **Tidak ada verifikasi kebenaran input.** Angka ditulis manual; bohong sejak awal tidak terdeteksi.
   Ini batas yang disengaja dan dinyatakan terbuka di UI.
5. Kadar air 14% dan suhu 25°C adalah asumsi ambang, bukan kutipan regulasi resmi.
6. Tidak ada QR code (FR-06 nice-to-have belum dikerjakan).
7. Jalan lokal saja, belum deploy.
