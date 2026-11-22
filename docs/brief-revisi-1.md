# BRIEF REVISI 1 — SimpleAgriChain Web

Root: `C:\Ouput Shiro\SimpleAgriChain\`
Acuan lama tetap berlaku: `docs/brief.md`, dokumen fase 1-2 (`plan.md`, `architecture.md`, `ui-spec.md`),
`docs/bug-report.md`. Revisi ini MENGUBAH sebagian di antaranya — yang berubah ditulis ulang di dokumen
masing-masing, jangan cuma ditempel di chat.

## Kenapa revisi ini ada (temuan user, valid)

Demonstrasi versi sekarang menceritakan: petani selalu benar, distributor selalu yang salah. Itu BUKAN
sifat sistem, itu bias narasi penyaji. Tiga masalah nyata:

1. **Sistem cuma mendeteksi perubahan SETELAH tercatat, bukan kebohongan SEJAK input.**
   Distributor boleh langsung mengetik `suhu: 15` di form Tab 1 walaupun di dunia nyata truknya 35 °C.
   Rantai tetap VALID, karena tidak ada data yang diubah setelah masuk — dia memang menulis 15 dari awal.
   Panel Tab 4 hanya menangkap manipulasi pasca-catat. Jadi klaim "anti-manipulasi suhu" versi sekarang
   belum lengkap dan gampang dipatahkan penguji.

2. **Petani punya lubang yang persis sama: KADAR AIR PANEN.**
   Beras dipanen dengan kadar air > 14% akan berjamur di jalan, WALAUPUN suhu truk distributor dingin
   dan benar. Berarti risiko mutu bisa berasal dari hulu (petani), bukan cuma dari transit.
   Dan nilai kadar air diisi oleh petani sendiri — jadi bisa dibohongi juga.

3. **Pertanyaan kunci user: "yang nentuin suhu truk siapa?"**
   Jawaban jujur untuk prototipe ini: operator distributor, manual, diketik. Maka nilainya bisa bohong.
   Ini yang di dunia blockchain disebut masalah oracle (data dunia nyata masuk ke ledger lewat manusia).

Kesimpulan yang HARUS tercermin di sistem dan narasi:
- Yang dijamin sistem: catatan yang sudah masuk tidak bisa diubah diam-diam (tamper-evident, append-only).
- Yang TIDAK dijamin: kebenaran data saat pertama kali ditulis. Garbage in, garbage out.

## Target utama revisi

Bikin sistem ini **adil dan jujur**: kedua aktor diperlakukan sama-sama bisa curang, batas kepercayaan
dinyatakan terbuka di UI, dan bahasa UI dipahami orang awam (bukan istilah teknis).

---

## Perubahan yang diminta

### R1. Field baru: Kadar Air Panen (hulu)
- Form Petani tambah field `kadar_air` (persen, angka desimal, contoh `12.5`).
- Validasi: wajib, harus angka, rentang wajar 0–100. Di luar itu -> HTTP 400 pesan Indonesia.
- Ambang risiko: **> 14.0 %** = risiko jamur/penurunan mutu saat pengiriman.
- Simpan di dalam objek `data` blok Petani (jangan nambah field di level atas blok — struktur 7 field
  blok tetap, ikuti `docs/architecture.md` bagian 2.2).

### R2. Pelacakan harus menilai DUA sumber risiko secara netral
`GET /api/trace/<batch_id>` sekarang punya penanda suhu saja. Tambah penilaian hulu:
- `kadar_air_max` (angka), `moisture_threshold` (14.0), `has_moisture_alert` (bool),
  `has_quality_risk` (bool, gabungan suhu ATAU kadar air),
  dan `risk_sources` (array string, isi yang benar-benar terpenuhi: `"PETANI"` dan/atau `"DISTRIBUTOR"`).
- Setiap entri timeline yang kadarnya terlalu basah dapat `moisture_alert: true`.
- Nada bahasa: SEBUT SUMBER RISIKO, jangan menuduh pelaku. Contoh benar:
  "Terindikasi risiko mutu dari tahap panen (kadar air 18.5% > 14%)" — bukan "Petani lalai".
- Kalau suhu tinggi DAN kadar air tinggi: dua-duanya disebut, keduanya `risk_sources: ["PETANI","DISTRIBUTOR"]`.
  Jadi skenario tidak bisa lagi dibuat seolah cuma distributor yang bisa salah.

### R3. Panel/fitur baru: batas kepercayaan dinyatakan terbuka
Tambah penjelasan dalam bahasa awam, terlihat di UI (bukan cuma di dokumen):
- Setiap entri timeline dan tiap kartu blok explorer diberi label sumber data, contoh:
  `Sumber data: diisi manual oleh Distributor` atau `... oleh Petani`.
- Tambah blok penjelasan singkat (bisa di Tab 2 atau Tab baru, keputusan UIUX) berisi 3 poin bahasa awam:
  1. Yang sistem ini jamin: catatan yang sudah masuk tidak bisa diubah atau dihapus diam-diam.
  2. Yang sistem ini TIDAK jamin: apakah angka yang diketik pertama kali itu jujur.
  3. Kalau angka ditulis bohong sejak awal, catatan bohong itu ikut terkunci dan terlihat sah.
- Analogi yang dipakai (pakai ini atau yang lebih bagus): "Buku besar yang halamannya direkatkan lem
  super: nggak bisa dihapus atau ditimpa. Tapi kalau sejak awal ditulis angka bohong, tulisan bohong itu
  juga ikut terkunci rapi."

### R4. Demo baru: "Bohong Sejak Awal" (bukti batas sistem)
Ini wajib ada dan wajib bisa diperagakan, karena inilah jawaban jujur atas pertanyaan user:
- Distributor mengetik `suhu: 15.0` LANGSUNG di form Tab 1 (bukan lewat panel serangan).
- Buka Tab 3 / Tab 2: status rantai tetap **VALID**. Tidak ada peringatan merah.
- UI harus menyatakan dengan terang bahwa ini memang batas sistem: catatan tampak sah walau angkanya bohong,
  karena tuduhan tidak bisa dibuktikan dari ledger sendirian.
- Sediakan tombol preset di Tab 1: `Isi Contoh Panen Basah (kadar air 18%)` dan
  `Isi Contoh Distributor Menulis Suhu Aman (bohong sejak awal)`.
- Boleh ditambah penjelasan apa yang dibutuhkan di dunia nyata agar ini tertutup: sensor suhu
  yang mencatat sendiri lalu ditandatangani digital, atau pihak ketiga/auditor yang ikut menandatangani
  catatan. Tulis sebagai penjelasan, bukan fitur yang harus dibangun (di luar scope tugas).

### R5. Bahasa awam menyeluruh
- Ganti istilah teknis di UI jadi bahasa sehari-hari, atau beri penjelasan dalam tanda kurung.
  Yang tidak boleh tampil tanpa penjelasan: `hash`, `immutable`, `ledger`, `append-only`, `oracle`,
  `previous_hash`, `current_hash`, `canonical JSON`.
  Contoh ganti: "Hash SHA-256 Blok Ini" boleh tetap, tapi beri baris kecil
  "sidik jari digital blok ini — ubah 1 huruf saja, sidik jarinya berubah total".
- Tidak ada istilah yang menyalahkan satu aktor. Netral: "sumber risiko", bukan "pelaku/pelanggar".
- Semua kalimat penjelasan bahasa Indonesia, sasaran pembaca: orang yang belum pernah dengar blockchain.

---

## Acceptance criteria revisi

- AC-R1: `POST /api/block/petani` tanpa `kadar_air` -> 400. `kadar_air` = 18.5 -> 201 dan tersimpan.
- AC-R2: `GET /api/trace/<batch>` untuk batch dengan kadar air 18.5 dan suhu 24 (dingin, benar) ->
  `has_moisture_alert: true`, `has_temperature_alert: false`, `has_quality_risk: true`,
  `risk_sources: ["PETANI"]`. Ini membuktikan petani bisa jadi sumber risiko.
- AC-R3: batch dengan kadar air 18.5 DAN suhu 35 -> `risk_sources` memuat `["PETANI","DISTRIBUTOR"]`.
- AC-R4: Distributor menulis suhu 15.0 sejak awal lewat form -> `GET /api/chain` mengembalikan
  `is_valid: true` dan `tampered_indices: []`. UI tetap tampil VALID, TANPA peringatan merah,
  dan ada penjelasan tertulis bahwa ini batas sistem.
- AC-R5: Tidak ada teks UI yang menuduh satu aktor. Cari kata "lalai", "pelanggar", "salah petani",
  "kesalahan distributor" di `templates/index.html` -> nol hasil.
- AC-R6: Setiap entri timeline menampilkan label sumber data ("diisi manual oleh ...").
- AC-R7: Regresi: semua AC lama tetap lolos (genesis, trace, tamper, reset, XSS escape, array JSON 400,
  batch_id duplikat 400, distributor orphan 400). Tamper 35 -> 15 lewat Tab 4 tetap VALID -> INVALID.

## Target files (tetap di dalam root yang sama)
Dokumen: `docs/plan.md` (revisi), `docs/architecture.md` (kontrak API baru), `docs/ui-spec.md` (bahasa awam),
`docs/bug-report.md` (putaran 3).
Kode: `blockchain.py`, `app.py`, `templates/index.html`, `notebook/SimpleAgriChain_Colab.ipynb`
(tambah skenario kadar air), `README.md`.
Boleh tambah `docs/panduan-demo.md` versi revisi.

## Batas
- Jangan bikin sensor IoT, login, tanda tangan digital, atau QR code. Cukup penjelasan tertulis.
- Jangan ubah struktur 7 field blok. Field kadar air masuk ke dalam `data`.
- Jangan hapus atau ganti endpoint lama; tambah yang baru, lama harus tetap kompatibel.
