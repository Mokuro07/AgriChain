# PANDUAN PEMAKAIAN & NARASI DEMO — SimpleAgriChain Web

Semua yang ditulis di sini sudah diuji langsung di mesin ini (bukan teori).

---

## 1. TUJUAN PROYEK — kenapa ini dibikin

Masalah nyata di rantai pasok pertanian organik:

1. **Klaim organik gampang dipalsukan.** Label kertas / sertifikat fisik bisa difoto-ulang, diedit,
   atau diganti tengkulak di tengah jalan. Konsumen di ujung nggak punya cara untuk cek.
2. **Pelacakan sumber kontaminasi lambat.** Kalau ada kasus keracunan, pengecekan manual berbasis
   kertas butuh hitungan hari untuk tahu produk ini dari lahan mana dan rusak di tahap mana.

SimpleAgriChain menjawab dua hal itu:
- Setiap catatan dikunci dengan **SHA-256** dan dirantai ke catatan sebelumnya. Ubah satu angka di
  catatan lama, seluruh rantai langsung ketahuan rusak. Itu yang bikin klaim nggak bisa dipalsukan diam-diam.
- Semua catatan bisa dicari dengan satu kode `Batch_ID` dalam hitungan detik, ditampilkan sebagai
  timeline hulu-ke-hilir. Jadi tahu persis rusaknya di petani atau di truk distributor.

Catatan penting soal kejujuran sistem ini: ini **blockchain permissioned sederhana tanpa mining/nonce**.
Jadi ini bukan jaringan terdesentralisasi antar-organisasi. Yang diambil dari blockchain cuma sifat
**append-only + hash chain + tamper-evident**. Cukup untuk membuktikan konsep di tugas semester, tapi
jangan diklaim sebagai blockchain publik penuh.

---

## 2. CARA PAKAI — 3 langkah, tanpa terminal

1. Klik ganda **`SimpleAgriChain.lnk`** di Desktop (atau `run-agrichain.bat` di dalam foldernya).
2. Jendela hitam muncul sendiri, tulis "[SimpleAgriChain] Menunggu server aktif...", lalu **otomatis
   browser kebuka** ke `http://127.0.0.1:5000`. Kalau lama sedikit, tunggu maksimal ~40 detik — script-nya
   polling port, bukan ngasal sleep.
3. Kalau sudah selesai: klik ganda **`stop-agrichain.bat`**. Muncul "Press any key to continue" — tekan Enter.

Nggak ada UAC, nggak ada instalasi. Python + Flask sudah dibungkus di folder `.venv` dalam proyek.

**Kalau presenter mau mengulang demo dari nol:** jangan hapus file manual. Pakai tombol
**"Reset Buku Besar ke Genesis"** di Tab 4.

---

## 3. TIGA AKTOR & HAK AKSES

| Aktor | Tab | Boleh ngapain |
|---|---|---|
| Petani / Produsen | Tab 1 (form kiri) | Daftarkan batch baru: Batch_ID, komoditas, lokasi, tanggal panen, pupuk, no sertifikat |
| Distributor / Logistik | Tab 1 (form kanan) | Update pengiriman: tanggal kirim, rute, suhu °C, kondisi muatan |
| Konsumen / Auditor | Tab 2 (read-only) | Cari Batch_ID, lihat timeline + alert suhu |

Sistem menolak distributor yang mencoba mencatat batch yang belum pernah didaftarkan petani
(HTTP 400 "belum diinisiasi oleh Petani"). Jadi nggak ada catatan logistik yatim.

---

## 4. NARASI DEMO LIVE — urutan klik dan apa yang terjadi

### Bagian A — Sekilas struktur blockchain (Tab 3, sebelum ada data)

Buka **Tab 3: Live Blockchain Explorer**.

Lihat: cuma ada **Blok #0 GENESIS**, `Previous Hash: 0`. Ini blok fondasi yang dibuat sistem otomatis
saat server nyala. `Previous Hash = 0` karena nggak ada blok sebelum dia.

Narasi: *"Setiap blok menyimpan hash blok sebelumnya. Rantai ini yang bikin buku besar nggak bisa
diubah diam-diam."*

### Bagian B — Petani mencatat panen (Tab 1, form kiri)

Buka **Tab 1**. Klik tombol **"⚡ Isi Contoh Beras Organik"** (biar nggak ngetik pas presentasi).
Field terisi otomatis:

```
Batch ID        : ORG-BRS-001
Komoditas       : Beras Merah Organik
Lokasi Lahan    : Desa Sukatani, Karawang
Tanggal Panen   : 2026-11-05
No. Sertifikat  : SNI-ORGANIK-2026-0881
Pupuk           : Kompos Kotoran Sapi Fermentasi (Organik)
```

Klik **"Simpan Blok Panen ke Blockchain"**. Muncul popup:

```
Blok Berhasil Dicatat!
Nomor Indeks : Blok #1
Aktor        : PETANI
Hash SHA-256 : 1e5d728ef2f1db0bc4d77e7098439dd93249239961bfe289b1d9722df380c135
```

Narasi: *"Data panen dan nomor sertifikat organik sudah dikunci jadi hash 64 karakter. Mulai detik ini,
kalau ada yang mengubah tulisan sertifikat itu, hash-nya nggak akan cocok lagi."*

Klik **Tutup**.

### Bagian C — Distributor update logistik (Tab 1, form kanan)

Klik **"⚡ Isi Contoh Pengiriman Hangat (>25°C)"**. Field terisi:

```
Batch ID        : ORG-BRS-001
Tanggal Kirim   : 2026-11-06
Rute            : Karawang -> Gudang Distributor Jakarta Timur
Suhu            : 35.0
Status Kondisi  : Dalam Pengiriman - Transit Hangat
```

Klik **"Perbarui Status Logistik ke Rantai"** -> popup **Blok #2, Aktor DISTRIBUTOR** dengan hash baru.

Narasi: *"Perhatikan, hash blok 2 ini menempel ke hash blok 1. Kalau blok 1 berubah, blok 2 ikut
kelihatan rusak. Ini yang namanya chain — mata rantai."*

Klik **Tutup**.

### Bagian D — Konsumen melacak produk (Tab 2)

Buka **Tab 2: Pelacakan Konsumen**. Ketik `ORG-BRS-001` (ada tombol pintasan juga), klik **"Lacak Komoditas"**.

Yang muncul (ini hasil asli dari pengujian):

```
PERINGATAN RISIKO KEAMANAN MUTU PANGAN:
Ditemukan suhu transit mencapai 35°C (melebihi ambang batas toleransi 25°C)!
Komoditas berisiko mengalami penurunan mutu/kesegaran organik.

KOMODITAS TERVERIFIKASI
Beras Merah Organik · Batch ID: ORG-BRS-001 · SNI Organik Terdaftar

Step 1 : Inisiasi Panen Pertanian — PETANI
         Lokasi Lahan: Desa Sukatani, Karawang
         No. Sertifikat: SNI-ORGANIK-2026-0881
Step 2 : Pemberangkatan Transit Logistik — DISTRIBUTOR
         Suhu Selama Transit: ⚠️ 35°C (Suhu Kritis > 25°C)
```

Narasi: *"Ini skenario simulasi kasus keracunan. Konsumen tinggal masukkan satu kode, dan dalam
hitungan detik kelihatan: produk dari Desa Sukatani, sertifikat organik terdaftar, dan yang bikin
masalah bukan petaninya — tapi truk distributor yang transit di 35 derajat. Waktu pelacakan turun
dari berhari-hari jadi sekejap."*

### Bagian E — Bukti rantai utuh (Tab 3)

Buka **Tab 3** lagi. Sekarang ada 3 blok. Perhatikan tiap kartu blok ada baris:

```
Blok #0  Current Hash : 43e8bdcc853711e45135...
         ↓ previous_hash Blok #1 = current_hash Blok #0
Blok #1  Current Hash : 4bacc5dcb49205d8f05d...
         ↓ previous_hash Blok #2 = current_hash Blok #1
Blok #2  Current Hash : 90f9d1ee534e68c98a08...
```

Header atas: **Total Blok Tercatat 3**, **Status Validitas Rantai: VALID (Semua Hash Cocok)** —
badge hijau.

Narasi: *"Panah-panah ini artinya hash blok berikutnya cocok dengan hash blok sebelumnya. Selama
semua panah nyambung, rantai VALID."*

### Bagian F — PUNCAK DEMO: oknum mencoba curang (Tab 4)

Buka **Tab 4: Panel Simulasi Serangan (Tamper Attack Lab)**.

Klik **"⚡ Muat Skenario Manipulasi Suhu"**. Form otomatis terisi:

```
Pilih Indeks Blok Target : 2
Data Payload (JSON)      : {"tanggal_kirim":"2026-11-06",
                            "rute":"Karawang -> Gudang Distributor Jakarta Timur",
                            "suhu": 15,   <-- dari 35 diubah jadi 15
                            "status_kondisi":"Suhu Dingin Terjaga Baik (Palsu)"}
```

Narasi: *"Skenarionya: distributor sadar dia lalai, suhu truknya 35 derajat. Dia coba edit catatan
lama supaya kelihatan cuma 15 derajat. Kita simulasikan itu sekarang."*

Klik **"Jalankan Serangan Manipulasi"**.

Hasil langsung:
1. Header paling atas halaman berubah jadi **▲ RANTAI INVALID** merah.
2. Muncul **"PERINGATAN KRITIS: Integritas buku besar rusak! Blok yang terkompromi: #2."**
3. Pesan panel: **"Status Rantai: INVALID | Indeks Rusak: #2"**.

Pindah ke **Tab 3**: Status Validitas Rantai sekarang **"INVALID (Blok yang terkompromi: #2)"**,
dan kartu Blok #2 dibingkai merah karena hash-nya nggak cocok lagi dengan isinya.

Narasi penutup: *"Ini inti seluruh proyeknya. Nilai suhu di buku besar sekarang memang tertulis 15,
tapi hash blok 2 masih hash dari data yang lama — 35. Sistem hitung ulang, nggak cocok, langsung
ditandai. Jadi kecurangan bukan dicegah dengan kunci akses, tapi dengan matematika: setiap perubahan
meninggalkan jejak yang nggak bisa dihapus. Itulah kenapa catatan blockchain disebut immutable."*

### Bagian G — Bersih-bersih untuk demo ulang

Di Tab 4, klik **"🔄 Reset Buku Besar ke Genesis"**. Rantai kembali 1 blok, badge hijau VALID lagi.
Siap dipresentasikan dari awal.

---

## 5. LATIHAN TEKNIS — kalau dosen minta lihat "mesin"-nya

Bukti rantai lewat API (bukan tampilan):

```bash
curl -s http://127.0.0.1:5000/api/chain
```

Contoh hasil nyata setelah 2 blok:

```json
{
  "is_valid": true,
  "tampered_indices": [],
  "total_blocks": 3,
  "chain": [
    { "index": 0, "batch_id": "GENESIS",     "actor": "SYSTEM",
      "previous_hash": "0",
      "current_hash": "43e8bdcc853711e451352ad39cc4011218f9000bb4c46bfe8e712496451b6d2f" },
    { "index": 1, "batch_id": "ORG-BRS-001", "actor": "PETANI",
      "previous_hash": "43e8bdcc853711e451352ad39cc4011218f9000bb4c46bfe8e712496451b6d2f",
      "current_hash": "4bacc5dcb49205d8f05d..." },
    { "index": 2, "batch_id": "ORG-BRS-001", "actor": "DISTRIBUTOR",
      "previous_hash": "4bacc5dcb49205d8f05d...",
      "current_hash": "90f9d1ee534e68c98a08..." }
  ]
}
```

Setelah tamper: `"is_valid": false`, `"tampered_indices": [2]`, dan `suhu` di blok 2 jadi `15`
sementara `current_hash`-nya masih hash data lama. Itu bukti mati bahwa hash nggak pernah ikut berubah
saat data diubah paksa.

---

## 6. NOTEBOOK COLAB (Fase 1 roadmap PRD)

`notebook/SimpleAgriChain_Colab.ipynb` — 4 code cell, sudah diuji run-all tanpa error.
Isi: teori singkat -> implementasi class -> Skenario 1 (input normal) -> Skenario 2 (trace + alert suhu)
-> Skenario 3 (ganti suhu lalu audit). Contoh output asli skenario 3:

```
Hash Blok #3 sebelum tamper      : da36f3d622d990bb...
Data Blok #3 setelah dimanipulasi: Suhu=18.0°C
Hash Blok #3 di ledger tetap     : da36f3d622d990bb...
Hash Blok #3 yang seharusnya     : c92c780f901e3bde...
Hasil Audit -> Status: INVALID  |  Indeks Rusak: [3]
```

Cara pakai: buka https://colab.research.google.com -> File -> Upload notebook -> pilih file itu ->
Runtime -> Run all.

---

## 7. PEMBAGIAN KERJA (kalau ditanya "ini bikin sendiri?")

| Peran | Output |
|---|---|
| Planner | `docs/plan.md` — spec, acceptance criteria, edge case, task breakdown |
| Architect | `docs/architecture.md` — skema blok, kontrak API 7 endpoint |
| UI/UX | `docs/ui-spec.md` — design token, wireframe 4 tab, state |
| Backend | `blockchain.py`, `app.py`, notebook Colab, launcher .bat, README |
| Frontend | `templates/index.html` — SPA 4 tab |
| QA | `docs/bug-report.md` — 22 checklist uji, temuan + status akhir ZERO CRITICAL BUG |

QA menemukan 2 bug Critical (XSS tersimpan di tampilan, dan crash HTTP 500 saat body request berupa
array JSON), 2 Medium (batch_id duplikat diizinkan, distributor bisa nulis batch tanpa hulu), 1 Low
(filter skrip stop nangkep PID 0). Semua sudah diperbaiki dan diuji ulang.

---

## 8. BATASAN — sebutkan ini kalau ditanya, jangan sampai diklaim berlebih

1. **Tidak ada mining / proof-of-work / konsensus jaringan.** Penambahan blok instan dan deterministik.
   Ini prototipe konsep, bukan jaringan blockchain terdistribusi.
2. **Penyimpanan satu file JSON lokal** (`ledger_data.json`), bukan database terdistribusi. Satu penulis.
3. **Tidak ada login/auth.** Tab input terbuka — siapa pun bisa menulis selama server jalan. Di produksi
   tiap aktor butuh identitas + tanda tangan digital (kunci privat).
4. **Tidak ada QR code.** FR-06 statusnya nice-to-have di PRD dan belum diimplementasikan; di Tab 2 ada
   tombol "Scan Verifikasi Publik" yang belum berfungsi.
5. **Batasan suhu 25 °C itu asumsi**, bukan standar resmi yang dikutip dari regulasi.
6. **Jalan lokal saja** di `http://127.0.0.1:5000`, belum ada deploy.
