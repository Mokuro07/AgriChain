# SPESIFIKASI DESAIN UI/UX: SimpleAgriChain Web

**Dokumen:** UI/UX Specification, Design Tokens & User-Friendly System (Fase 2 + Revisi 1)  
**Penyusun:** @uiux (AG-03)  
**Root Proyek:** `C:\Ouput Shiro\SimpleAgriChain\`  
**Target:** Frontend Developer (@frontend), Backend Developer (@backend), QA Tester (@bug-report)  
**Status:** Diselaraskan Penuh dengan Addendum Revisi 1 & Siap Diuji  

---

## 1. Prinsip Desain, Filosofi Netralitas, & Bahasa Awam (Agrinova-Style)

Antarmuka SimpleAgriChain dirancang dengan gaya visual modern, bersih, dan ramah pengguna (*user-friendly*) bertema pertanian pangan organik (seperti platform **Agrinova**). Seluruh pengalaman pengguna mengedepankan transparansi objektif, keadilan bagi semua aktor rantai pasok, dan kemudahan pemahaman bagi masyarakat awam tanpa latar belakang kriptografi:

1. **Netralitas Dua Titik Risiko Mutu (Fair & Neutral Evaluation):**
   - Rantai pasok pangan tidak boleh memojokkan satu pihak. Petani maupun Distributor memiliki potensi risiko biologis dan fisik yang setara:
     - **Tahap Hulu (Petani):** Parameter **Kadar Air Panen** (<= 14.0%). Jika dipanen terlalu basah (> 14.0%), beras akan berjamur di perjalanan terlepas dari kondisi truk logistik.
     - **Tahap Hilir (Distributor):** Parameter **Suhu Transit** (<= 25.0°C). Jika suhu melebihi batas (> 25.0°C), terjadi penurunan mutu dan risiko pembusukan.
   - **Nol Bahasa Menuduh:** Seluruh UI menyebut *"Sumber Risiko Mutu Terindikasi: Tahap Panen / Tahap Transit"*, bukan *"Petani/Distributor Lalai"*, *"Pelanggaran"*, atau *"Kesalahan"*.
2. **Keterbukaan Batas Sistem (Analogi Buku Besar Lem Super):**
   - Blockchain adalah sistem *tamper-evident* (mendeteksi perubahan setelah data tercatat), **bukan alat pendeteksi kebohongan manusia saat data pertama kali diketik** (*The Oracle Problem*).
   - Di UI disediakan panel edukatif dengan analogi bahasa awam:
     > *"Bayangkan sebuah buku besar di mana setiap halaman langsung direkatkan lem super setelah ditulis. Catatan yang sudah masuk mustahil dihapus atau ditimpa tanpa merusak kertasnya. Namun, jika seseorang sejak awal menulis angka palsu (misal menulis suhu 15°C padahal aslinya 35°C), tulisan palsu tersebut akan tetap terkunci rapi dan sah di dalam buku besar."*
   - Skenario **"Bohong Sejak Awal"** pada Tab 1 didesain menghasilkan status rantai tetap **VALID**, dan antarmuka dengan jujur menjelaskan kepada pengguna bahwa ini adalah batas kemampuan ledger manual, bukan bukti kebenaran fisik.
3. **Transparansi Sumber Data Input:**
   - Setiap kartu blok di Explorer dan setiap kartu timeline di Pelacakan wajib memuat label tegas:  
     `"Sumber data: diisi manual oleh Petani"` atau `"Sumber data: diisi manual oleh Distributor"`.
4. **Penerjemahan Istilah Teknis ke Bahasa Sehari-hari:**
   - Istilah asing kriptografi tidak boleh berdiri sendiri tanpa padanan awam:
     - **Hash:** *"Sidik jari digital unik (64 karakter) — jika 1 huruf diubah, sidik jari berubah total."*
     - **Ledger / Chain:** *"Buku besar berantai pencatat transaksi yang saling mengunci."*
     - **Immutable:** *"Catatan permanen — tidak bisa dihapus atau diedit setelah masuk."*
     - **Append-Only:** *"Hanya bisa menambah lembaran baru, tidak bisa menimpa lembaran lama."*
     - **Previous Hash:** *"Sidik jari blok sebelumnya yang mengikat rantai."*
5. **Efisiensi Demonstrasi (Pre-fill Preset Buttons):**
   - Disediakan tombol aksi cepat (*1-click demo presets*) untuk demonstrasi skenario:
     - Tab Petani: *"Isi Contoh Beras Normal (12.5%)"* & *"Isi Contoh Panen Basah (18.0%)"*.
     - Tab Distributor: *"Isi Contoh Pengiriman Hangat (35.0°C)"* & *"Isi Contoh Distributor Menulis Suhu Aman (bohong sejak awal - 15.0°C)"*.
6. **Aksesibilitas & Ergonomi (Touch Target >= 44px):**
   - Seluruh elemen interaktif mematuhi WCAG 2.1 AA: tinggi area klik/sentuh minimum 44px, rasio kontras teks >= 4.5:1, dan umpan balik status instan.

---

## 2. Design Tokens Konkret (Tailwind CSS CDN)

Menggunakan konfigurasi native Tailwind CSS tanpa build-step (Node.js/npm) dengan sistem warna berbasis semantik:

### 2.1 Palet Warna (Color Palette)

| Kategori Token | Nama Token | Nilai HEX | Kelas Tailwind | Rasionalisasi & Peruntukan |
|---|---|---|---|---|
| **Primary (Brand / Agrinova Nature)** | Emerald 600 | `#059669` | `bg-emerald-600` / `text-emerald-600` | Warna identitas pertanian organik hijau segar; tombol submit petani, badge sistem aktif. |
| | Emerald 700 (Hover) | `#047857` | `hover:bg-emerald-700` | State hover tombol primary petani. |
| | Emerald 50 (Soft Canvas) | `#ecfdf5` | `bg-emerald-50` | Background container petani, badge status aman/valid. |
| | Emerald 800 (Text on Soft) | `#065f46` | `text-emerald-800` | Teks status sukses / aman agar kontras WCAG AAA. |
| **Secondary (Logistics / Cool Sky)** | Sky 600 | `#0284c7` | `bg-sky-600` / `text-sky-600` | Warna identitas logistik dan cold-chain; tombol submit distributor. |
| | Sky 700 (Hover) | `#0369a1` | `hover:bg-sky-700` | State hover tombol distributor. |
| | Sky 50 (Soft Canvas) | `#f0f9ff` | `bg-sky-50` | Background container distributor, chip aktor logistik. |
| | Sky 800 (Text on Soft) | `#075985` | `text-sky-800` | Teks label logistik distributor. |
| **Danger / Alarm (Tamper & Suhu / Kadar Air)** | Rose 600 | `#e11d48` | `bg-rose-600` / `text-rose-600` | Aksi manipulasi tamper, status rantai INVALID, peringatan risiko mutu. |
| | Rose 700 (Hover) | `#be123c` | `hover:bg-rose-700` | State hover tombol bahaya / reset. |
| | Rose 100 (Alert BG) | `#ffe4e6` | `bg-rose-100` | Background banner alert manipulasi data dan peringatan mutu. |
| | Rose 900 (Alert Text) | `#881337` | `text-rose-900` | Teks peringatan bahaya agar terbaca jelas (kontras > 7:1). |
| **Warning / Boundary (Edukasi Batas Sistem)** | Amber 500 | `#f59e0b` | `bg-amber-500` / `text-amber-500` | Banner edukasi batas sistem (Bohong Sejak Awal / Oracle Problem). |
| | Amber 50 (Soft BG) | `#fffbeb` | `bg-amber-50` | Background card penjelasan buku besar lem super. |
| | Amber 800 (Text on Soft) | `#92400e` | `text-amber-800` | Teks keterangan batas kepercayaan sistem. |
| **Neutral / Surfaces** | Slate 50 (App Canvas) | `#f8fafc` | `bg-slate-50` | Latar belakang aplikasi web secara keseluruhan, lembut untuk mata. |
| | White (Cards / Surfaces) | `#ffffff` | `bg-white` | Latar kartu form, timeline, blok explorer. |
| | Slate 100 (Borders/Muted) | `#f1f5f9` | `bg-slate-100` | Border subtle, disabled button, chip sample. |
| | Slate 200 (Lines/Dividers)| `#e2e8f0` | `border-slate-200` | Garis pembatas kartu, separator timeline. |
| | Slate 400 (Placeholder) | `#94a3b8` | `text-slate-400` | Placeholder input, ikon sekunder. |
| | Slate 600 (Secondary Text) | `#475569` | `text-slate-600` | Label pembantu, label sumber data manual, timestamp. |
| | Slate 900 (Main Heading) | `#0f172a` | `text-slate-900` | Teks heading judul, nilai data penting. |

---

### 2.2 Skala Tipografi (Typography Hierarchy)

- **Font Antarmuka Utama:** `Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`  
- **Font Kriptografi (Hash SHA-256):** `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace`  

| Peran Tipografi | Ukuran (px / rem) | Font Weight | Line Height | Kelas Tailwind | Contoh Penggunaan |
|---|---|---|---|---|---|
| **App Title** | 24px / 1.5rem | Bold (700) | 1.25 | `text-xl sm:text-2xl font-bold` | Header navigasi aplikasi SimpleAgriChain. |
| **Section Header (H2)**| 18px / 1.125rem | Semibold (600) | 1.3 | `text-lg sm:text-xl font-semibold` | Judul Tab, judul kartu form, judul explorer. |
| **Card Header (H3)** | 15px / 0.9375rem| Semibold (600) | 1.4 | `text-sm sm:text-base font-semibold`| Judul sub-seksi form, judul step timeline. |
| **Body Primary** | 14px / 0.875rem | Regular (400) | 1.5 | `text-sm font-normal` | Isi teks deskripsi, instruksi form, nilai data. |
| **Body Emphasized** | 14px / 0.875rem | Medium (500) | 1.5 | `text-sm font-medium` | Label input form, tombol tab navigasi aktif. |
| **Caption / Helper** | 12px / 0.75rem | Regular (400) | 1.4 | `text-xs font-normal` | Helper text batas aman (<=14%, <=25°C), sumber manual. |
| **Code / Hash Display**| 12px / 0.75rem | Medium (500) | 1.4 | `text-xs font-mono` | String 64 karakter `previous_hash` & `current_hash`. |

---

### 2.3 Skala Spacing & Elevated Surfaces

- **Grid Base:** Kelipatan 4px (`p-1` = 4px, `p-2` = 8px, `p-3` = 12px, `p-4` = 16px, `p-6` = 24px, `p-8` = 32px).
- **Border Radius:**
  - `rounded-md` (`6px`): Chip preset sample data, badge kecil.
  - `rounded-lg` (`8px`): Elemen form `<input>`, `<select>`, tombol aksi.
  - `rounded-xl` (`12px`): Kartu form hulu/hilir, kartu blok explorer, banner alert.
  - `rounded-2xl` (`16px`): Modal receipt hash, box timeline utama.
  - `rounded-full` (`9999px`): Lingkaran node timeline, pill status rantai.
- **Elevation / Shadows:**
  - `shadow-sm`: Kartu statis berlatar canvas slate-50.
  - `shadow-md`: Hover state kartu blok explorer, floating toast notification.
  - `shadow-xl`: Modal konfirmasi pencatatan blok baru.

---

## 3. Glosarium Bahasa Awam (Wajib Muncul di UI)

Agar pengguna awam tidak terintimidasi oleh jargon teknis, antarmuka menyediakan penjelasan ringkas dalam kurung atau tooltip pada setiap istilah teknis:

1. **Hash (SHA-256):**  
   *Penjelasan Awam:* **Sidik Jari Digital**.  
   *Teks Bantuan UI:* *"Kombinasi unik 64 karakter acak yang dihitung dari isi data. Jika satu huruf saja diubah, sidik jari ini berubah total."*
2. **Blockchain / Ledger:**  
   *Penjelasan Awam:* **Buku Besar Digital Berantai**.  
   *Teks Bantuan UI:* *"Buku catatan yang setiap halamannya saling terikat nomor sidik jari dengan halaman sebelumnya."*
3. **Immutable / Append-Only:**  
   *Penjelasan Awam:* **Terkunci Permanen**.  
   *Teks Bantuan UI:* *"Catatan yang sudah masuk hanya bisa ditambah lembaran baru, tidak bisa dihapus atau diedit kembali."*
4. **Previous Hash:**  
   *Penjelasan Awam:* **Sidik Jari Blok Sebelumnya**.  
   *Teks Bantuan UI:* *"Kunci rantai yang memastikan urutan kronologis tidak dapat disisipi data asing."*
5. **The Oracle Problem (Batas Sistem Input):**  
   *Penjelasan Awam:* **Batas Kejujuran Input Manual**.  
   *Teks Bantuan UI:* *"Buku besar menjamin catatan tidak bisa diubah setelah masuk, tetapi tidak bisa memeriksa apakah manusia mengetik angka yang jujur saat pertama kali menginput."*

---

## 4. Spesifikasi Komponen UI

### 4.1 Tombol (Button System — WCAG 2.1 AA >= 44px)

| Tipe Tombol | Visual & Kelas Tailwind | Ukuran Sentuh | Interaksi & State |
|---|---|---|---|
| **Primary Petani** | `bg-emerald-600 text-white font-medium rounded-lg shadow-sm hover:bg-emerald-700 active:scale-[0.99] focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2` | Min tinggi 44px (`h-11 px-5`) | - Hover: `bg-emerald-700`<br>- Loading: `opacity-75 cursor-not-allowed` + SVG spinner berputar<br>- Disabled: `bg-slate-300 text-slate-500` |
| **Primary Distributor** | `bg-sky-600 text-white font-medium rounded-lg shadow-sm hover:bg-sky-700 active:scale-[0.99] focus:ring-2 focus:ring-sky-500 focus:ring-offset-2` | Min tinggi 44px (`h-11 px-5`) | - Hover: `bg-sky-700`<br>- Loading: spinner aktif<br>- Disabled: `bg-slate-300` |
| **Danger / Tamper** | `bg-rose-600 text-white font-medium rounded-lg shadow-sm hover:bg-rose-700 focus:ring-2 focus:ring-rose-500 focus:ring-offset-2` | Min tinggi 44px (`h-11 px-5`) | - Hover: `bg-rose-700`<br>- Active: `bg-rose-800` |
| **Secondary / Outline** | `bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 font-medium rounded-lg` | Min tinggi 44px (`h-11 px-4`) | - Hover: `bg-slate-50 border-slate-400` |
| **Preset Sample Pill** | `bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium rounded-md px-3 py-2 transition-colors border border-slate-200 inline-flex items-center gap-1.5` | Hit-box >= 44px (lewat padding vertikal) | Sekali klik langsung mengisi form untuk mempermudah demonstrasi. |
| **Salin Sidik Jari (Copy)** | `p-2 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-md transition-colors` | Hit-box 44 x 44px | Menyalin 64 karakter hash dan menampilkan status *"Tersalin!"* selama 1.5 detik. |

---

### 4.2 Form Input Fields & Validasi Hulu-Hilir

Setiap input wajib memiliki pasangan `<label>` eksplisit dengan `for="id"`:

1. **Input Standar:**
   - Tinggi elemen: `h-11` (44px).
   - Border normal: `border-slate-300 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200`.
   - Error: `border-rose-500 bg-rose-50/20 text-rose-900`.
2. **Field Khusus Petani: `kadar_air` (Kadar Air Panen %):**
   - Label: `Kadar Air Panen (%) *`
   - Helper Text: `Standar aman: <= 14.0%. Nilai > 14.0% berisiko memicu pertumbuhan jamur saat pengiriman.`
   - Placeholder: `Contoh: 12.5`
   - Validasi: Angka desimal/bulat 0.0 <= kadar_air <= 100.0.
3. **Field Khusus Distributor: `suhu` (Suhu Selama Transit °C):**
   - Label: `Suhu Selama Transit (°C) *`
   - Helper Text: `Standar aman: <= 25.0°C. Nilai > 25.0°C berisiko memicu kerusakan mutu transit.`
   - Placeholder: `Contoh: 23.5`
   - Validasi: Angka numerik -20.0 <= suhu <= 60.0.

---

### 4.3 Kartu & Badge Status Rantai

1. **Status Rantai Global (Header & Explorer):**
   - **VALID (Catatan Utuh):**  
     `bg-emerald-100 text-emerald-800 border border-emerald-300 font-semibold px-3.5 py-1.5 rounded-full text-xs flex items-center gap-2`  
     *Teks:* `● CATATAN UTUH` (Penjelasan: *Semua sidik jari terverifikasi cocok*).
   - **INVALID (Terjadi Manipulasi):**  
     `bg-rose-100 text-rose-800 border border-rose-300 font-bold px-3.5 py-1.5 rounded-full text-xs flex items-center gap-2 animate-pulse`  
     *Teks:* `▲ PERINGATAN: INTEGRITAS CATATAN RUSAK` (Penjelasan: *Ada data historis yang dimanipulasi*).
2. **Badge Aktor & Label Sumber Data Manual:**
   - Badge Petani: `bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs px-2.5 py-1 rounded font-medium`
   - Badge Distributor: `bg-sky-50 text-sky-700 border border-sky-200 text-xs px-2.5 py-1 rounded font-medium`
   - Label Sumber Data:  
     `<span class="text-xs text-slate-500 font-normal">Sumber data: diisi manual oleh Petani / Distributor</span>`

---

## 5. Alur Pengguna (User Flow) & Wireframe Layar 4 Tab

### 5.1 Navigasi Utama & Global Header

```
+--------------------------------------------------------------------------------------------------+
| [LOGO DAUN] SimpleAgriChain Web   [● CATATAN UTUH (Hijau)]   ← satu grup, ter-center |
| Sistem Ketertelusuran Pangan Organik           (Semua sidik jari digital blok cocok & sah)       |
+--------------------------------------------------------------------------------------------------+
| [ Tab 1: Input Transaksi ]  [ Tab 2: Pelacakan Konsumen ]  [ Tab 3: Explorer ]  [ Tab 4: Simulasi ] |
+--------------------------------------------------------------------------------------------------+
```

---

### 5.2 Layar 1: Tab Input Transaksi (Dual Form Hulu & Hilir)

**Tujuan:** Pendaftaran panen oleh Petani dan pencatatan transit oleh Distributor berdampingan, dilengkapi tombol preset skenario demo.

**Wireframe Layout Teks:**
```
+--------------------------------------------------------------------------------------------------+
| TAB 1: INPUT TRANSAKSI RANTAI PASOK                                                              |
| Catat inisiasi panen baru (Hulu) atau perbarui status logistik (Hilir) ke dalam buku besar.     |
+--------------------------------------------------+-----------------------------------------------+
| FORM PETANI (Inisiasi Panen Hulu)                | FORM DISTRIBUTOR (Pembaruan Logistik Transit) |
| Tombol Contoh Cepat:                             | Tombol Contoh Cepat:                          |
| [Padi Organik Normal (12.5%)] [Panen Basah (18%)]| [Pengiriman Hangat (35°C)] [Suhu Aman Bohong (15°C)] |
|                                                  |                                               |
| Keterangan: Data diisi manual oleh Petani        | Keterangan: Data diisi manual oleh Distributor|
|                                                  |                                               |
| Batch ID *                                       | Target Batch ID *                             |
| [ ORG-BRS-001                                  ] | [ ORG-BRS-001 (atau pilih dari daftar)      ] |
|                                                  |                                               |
| Nama Komoditas *                                 | Tanggal Pengiriman *                          |
| [ Beras Merah Organik                          ] | [ 2026-11-06                                ] |
|                                                  |                                               |
| Lokasi Lahan Panen *                             | Rute Pengiriman *                             |
| [ Desa Sukatani, Karawang                      ] | [ Karawang -> Gudang Jakarta Timur          ] |
|                                                  |                                               |
| Tanggal Panen *                                  | Suhu Selama Transit (°C) *                    |
| [ 2026-11-05                                   ] | [ 23.5                                      ] |
|                                                  |  (Batas aman: <= 25.0°C)                      |
| Kadar Air Panen (%) * [FIELD BARU]               |                                               |
| [ 12.5                                         ] | Status Kondisi Muatan *                       |
|  (Batas aman: <= 14.0%. >14% berisiko jamur)     | [ Kemasan Tersegel Aman, Transit Dingin     ] |
|                                                  |                                               |
| Jenis Pupuk Organik *                            |                                               |
| [ Kompos Kotoran Sapi Fermentasi               ] |                                               |
|                                                  |                                               |
| Nomor Sertifikat Organik *                       |                                               |
| [ SNI-ORGANIK-2026-0881                        ] |                                               |
|                                                  |                                               |
| [ Simpan Catatan Panen (Hijau - 44px)          ] | [ Perbarui Status Logistik (Biru - 44px)    ] |
+--------------------------------------------------+-----------------------------------------------+
```

**Detail Presets Tab 1:**
1. **"Padi Organik Normal (12.5%)":** Mengisi data panen ideal dengan `kadar_air: 12.5` (Aman).
2. **"Panen Basah (18%)":** Mengisi data panen lembap dengan `kadar_air: 18.0` (Memicu evaluasi risiko jamur hulu pada Tab 2).
3. **"Pengiriman Hangat (35°C)":** Mengisi logistik dengan `suhu: 35.0` (Memicu evaluasi risiko suhu transit pada Tab 2).
4. **"Suhu Aman Bohong (15°C)":** Mengisi logistik dengan `suhu: 15.0` (Mendemonstrasikan bahwa sistem tetap menyatakan rantai VALID karena catatan sah tercatat sejak awal, bukan bukti kebenaran suhu fisik di truk).

---

### 5.3 Layar 2: Tab Pelacakan Konsumen & Evaluasi Dua Titik Risiko

**Tujuan:** Memberikan transparansi publik dengan penilaian risiko objektif di kedua tahap (hulu & hilir) serta panel penjelasan batas sistem.

**Wireframe Layout Teks:**
```
+--------------------------------------------------------------------------------------------------+
| TAB 2: PELACAKAN KONSUMEN & KETERTELUSURAN                                                       |
| Lacak jejak pangan organik dari sawah hingga distribusi menggunakan nomor Batch ID.              |
+--------------------------------------------------------------------------------------------------+
| Masukkan Batch ID Komoditas:                                                                     |
| [ ORG-BRS-001                                                 ] [ Lacak Riwayat Pangan (44px) ]  |
| Contoh Cepat: [ ORG-BRS-001 ]                                                                    |
+--------------------------------------------------------------------------------------------------+
| (Kondisi: Ditemukan Riwayat Dua Titik Risiko)                                                    |
|                                                                                                  |
| [STATUS BANNER EVALUASI RISIKO MUTU - BAHASA NETRAL]                                             |
| ▲ PERHATIAN MUTU PANGAN: Terindikasi 2 Titik Risiko Pada Perjalanan Komoditas Ini:               |
| 1. Tahap Panen: Kadar air gabah tercatat 18.5% (melebihi ambang batas aman 14.0% - risiko jamur)  |
| 2. Tahap Transit: Suhu ruang muat tercatat 35.0°C (melebihi ambang batas aman 25.0°C)           |
| Sertifikat Organik: SNI-ORGANIK-2026-0881 [TERVERIFIKASI TERCATAT DI BUKU BESAR]                 |
+--------------------------------------------------------------------------------------------------+
| TIMELINE RIWAYAT PERJALANAN (HULU -> HILIR):                                                     |
|                                                                                                  |
| (○) LANGKAH 1: INISIASI PANEN OLEH PETANI (Blok #1)                     [ 2026-11-08 10:15 UTC ] |
|  │  Sumber data: diisi manual oleh Petani                                                        |
|  │  - Lokasi Lahan : Desa Sukatani, Karawang                                                     |
|  │  - Kadar Air    : [ 18.5 % ] (Perhatian: Melebihi standar aman 14.0% - potensi jamur)        |
|  │  - Pupuk        : Kompos Kotoran Sapi Fermentasi                                              |
|  │  - Sertifikat   : SNI-ORGANIK-2026-0881                                                       |
|  │  - Sidik Jari Blok (Hash): 4a5e1e4b...afdeda33b [Salin Sidik Jari]                            |
|  │                                                                                               |
|  ▼                                                                                               |
|                                                                                                  |
| (○) LANGKAH 2: LOGISTIK DISTRIBUSI (Blok #2)                            [ 2026-11-08 10:20 UTC ] |
|     Sumber data: diisi manual oleh Distributor                                                   |
|     - Rute         : Karawang -> Gudang Distributor Jakarta Timur                                |
|     - Suhu Transit : [ 35.0 °C ] (Perhatian: Melebihi standar dingin 25.0°C)                     |
|     - Kondisi Muatan: Dalam Pengiriman                                                           |
|     - Sidik Jari Blok (Hash): 8f480329...e0e35f502 [Salin Sidik Jari]                            |
+--------------------------------------------------------------------------------------------------+
| [PANEL EDUKASI: MEMAHAMI BATAS SISTEM & BUKU BESAR LEM SUPER]                                    |
| 1. Yang Dijamin Sistem: Catatan yang sudah masuk terkunci permanen dan tidak bisa diubah         |
|    diam-diam oleh siapa pun (anti-manipulasi pasca-pencatatan).                                  |
| 2. Yang TIDAK Dijamin: Sistem tidak memeriksa apakah operator mengetik angka yang benar di awal. |
| 3. Solusi Masa Depan: Di dunia nyata, kelemahan input manual dapat diatasi menggunakan sensor IoT |
|    otomatis atau tanda tangan digital pihak ketiga bersertifikat.                                |
+--------------------------------------------------------------------------------------------------+
```

---

### 5.4 Layar 3: Tab Live Blockchain Explorer

**Tujuan:** Menampilkan rantai blok secara transparan dengan istilah awam dan label sumber data manual pada setiap blok.

**Wireframe Layout Teks:**
```
+--------------------------------------------------------------------------------------------------+
| TAB 3: LIVE BUKU BESAR DIGITAL (BLOCKCHAIN EXPLORER)                                            |
| Lembaran catatan transaksi yang saling terikat oleh sidik jari digital (kriptografi SHA-256).    |
+--------------------------------------------------------------------------------------------------+
| METRIK BUKU BESAR:                                                                               |
| [ Total Lembaran/Blok: 3 ] | [ Status Rantai: ● CATATAN UTUH & SAH ] | [ Tombol: Segarkan Data ] |
+--------------------------------------------------------------------------------------------------+
| DAFTAR BLOK BERANTAI:                                                                            |
|                                                                                                  |
| +----------------------------------------------------------------------------------------------+ |
| | BLOK #0 (LEMBARAN PERDANA / GENESIS)                               Aktor: SYSTEM             |
| | Waktu Pencatatan: 2026-11-08T10:00:00Z                            Batch ID: GENESIS          |
| | Sumber data: diinisialisasi otomatis oleh Sistem                                              |
| | Isi Catatan: {"message": "Genesis Block SimpleAgriChain", "version": "1.0.0"}                |
| | Sidik Jari Sebelumnya (Previous Hash): 0                                                     |
| | Sidik Jari Blok Ini   (Current Hash) : 6b86b273ff34...7875b4b [Salin]                        |
| +----------------------------------------------------------------------------------------------+ |
|                                       │                                                          |
|                                       ▼ Sidik jari Blok 1 mengikat sidik jari Blok 0             |
| +----------------------------------------------------------------------------------------------+ |
| | BLOK #1                                                            Aktor: PETANI             |
| | Waktu Pencatatan: 2026-11-08T10:15:30Z                            Batch ID: ORG-BRS-001      |
| | Sumber data: diisi manual oleh Petani                                                        |
| | Isi Catatan: {"komoditas": "Beras Merah...", "kadar_air": 18.5, "sertifikat": "SNI..."}      |
| | Sidik Jari Sebelumnya (Previous Hash): 6b86b273ff34...7875b4b                                |
| | Sidik Jari Blok Ini   (Current Hash) : 4a5e1e4baab8...fdeda33b [Salin]                       |
| +----------------------------------------------------------------------------------------------+ |
|                                       │                                                          |
|                                       ▼ Sidik jari Blok 2 mengikat sidik jari Blok 1             |
| +----------------------------------------------------------------------------------------------+ |
| | BLOK #2                                                            Aktor: DISTRIBUTOR        |
| | Waktu Pencatatan: 2026-11-08T10:20:15Z                            Batch ID: ORG-BRS-001      |
| | Sumber data: diisi manual oleh Distributor                                                   |
| | Isi Catatan: {"rute": "Karawang -> Jakarta", "suhu": 35.0, "status_kondisi": "..."}          |
| | Sidik Jari Sebelumnya (Previous Hash): 4a5e1e4baab8...fdeda33b                                |
| | Sidik Jari Blok Ini   (Current Hash) : 8f480329ac61...e0e35f502 [Salin]                       |
| +----------------------------------------------------------------------------------------------+ |
+--------------------------------------------------------------------------------------------------+
```

---

### 5.5 Layar 4: Tab Panel Simulasi Serangan (Tamper Attack Lab)

**Tujuan:** Menguji daya tahan buku besar terhadap manipulasi data historis (pasca-catat) dan membandingkannya dengan fenomena "Bohong Sejak Awal".

**Wireframe Layout Teks:**
```
+--------------------------------------------------------------------------------------------------+
| TAB 4: LABORATORIUM SIMULASI SERANGAN (TAMPER ATTACK LAB)                                        |
| Uji kemampuan sistem dalam mendeteksi kecurangan data yang sudah tersimpan di masa lalu.        |
+--------------------------------------------------------------------------------------------------+
| (Bila Rantai Diserang & Mengalami Manipulasi Data Historis)                                      |
| +----------------------------------------------------------------------------------------------+ |
| | ▲ PERINGATAN: INTEGRITAS BUKU BESAR TELAH DIRUSAK!                                           | |
| | Rantai terdeteksi INVALID. Blok yang tidak cocok: Blok #2.                                    | |
| | Isi data telah diubah diam-diam, sehingga rumus sidik jari menghasilkan nilai yang berbeda.  | |
| +----------------------------------------------------------------------------------------------+ |
|                                                                                                  |
| FORM UJI MANIPULASI DATA BLOK HISTORIS:                                                          |
| [Pilih Skenario Serangan: Ubah Suhu 35.0°C menjadi 15.0°C pada Blok #2]                         |
|                                                                                                  |
| Pilih Nomor Blok Target:                                                                         |
| [ Blok #2 (DISTRIBUTOR - ORG-BRS-001)                                                        ] |
|                                                                                                  |
| Data yang Dimodifikasi (Editor JSON):                                                            |
| +----------------------------------------------------------------------------------------------+ |
| | {                                                                                            | |
| |   "tanggal_kirim": "2026-11-06",                                                             | |
| |   "rute": "Karawang -> Gudang Distributor Jakarta Timur",                                    | |
| |   "suhu": 15.0,                                      <-- Dipalsukan setelah tercatat         | |
| |   "status_kondisi": "Suhu Dingin Terjaga Baik (Palsu)"                                       | |
| | }                                                                                            | |
| +----------------------------------------------------------------------------------------------+ |
|                                                                                                  |
| [ Jalankan Manipulasi Data (Merah - 44px) ]    [ Reset Buku Besar ke Genesis (Outline - 44px) ] |
+--------------------------------------------------------------------------------------------------+
| CATATAN PERBANDINGAN PENTING:                                                                    |
| - Jika distributor memalsukan suhu di Tab 4 ini: Rantai jadi INVALID (Merah) karena data diubah  |
|   setelah buku besar dikunci.                                                                    |
| - Jika distributor mengetik suhu 15°C sejak awal di Tab 1: Rantai tetap VALID (Hijau) karena     |
|   buku besar mencatat data awal apa adanya (inilah keterbatasan input manual).                   |
+--------------------------------------------------------------------------------------------------+
```

---

## 6. Spesifikasi Lengkap State Antarmuka

### 6.1 Loading State
- **Tombol Submit Form:** Menampilkan teks proses (*"Menyimpan ke Buku Besar..."*) dengan ikon putar SVG spinner, dan atribut `disabled` aktif untuk mencegah *double submit*.
- **Explorer & Trace:** Menampilkan kotak shimmer skeleton beranimasi (`animate-pulse bg-slate-200 h-28 rounded-xl`) sebelum JSON API selesai diambil.

### 6.2 Empty State
- **Pelacakan (Sebelum Mencari):** Kartu berpusat dengan ikon pencarian ramah, teks: *"Ketik nomor Batch ID atau klik tombol contoh untuk melihat perjalanan pangan organik dari sawah hingga tangan konsumen."*
- **Explorer (Bila Kosong):** Teks ramah: *"Buku besar sedang menyiapkan Lembaran Perdana (Genesis Block)..."*.

### 6.3 Error State
- **Input Form Gagal Validasi:** Kotak input berbingkai merah (`border-rose-500 ring-rose-200`) disertai pesan jelas di bawahnya, misalnya: *"Nilai kadar air harus berada dalam rentang 0.0 s.d. 100.0%"*.
- **Batch 404 (Tidak Ditemukan):** Kotak alert abu-abu netral: *"Batch ID 'ORG-XYZ-999' belum pernah didaftarkan oleh Petani dalam buku besar."*
- **Koneksi Node Terputus:** Toast mengambang merah: *"Koneksi ke server terputus. Pastikan server lokal berjalan di port 5000."*

### 6.4 Success State
- **Pencatatan Blok Berhasil:** Modal receipt muncul menampilkan indeks blok, sidik jari digital (hash) 64-karakter, tombol salin, dan tombol langsung beralih ke Tab Explorer.

---

## 7. Verifikasi Standar Aksesibilitas (WCAG 2.1 AA)

1. **Target Sentuh Minimum >= 44 x 44px:**
   - Semua tombol utama, tombol preset contoh, input form, dan tab navigasi memiliki tinggi minimal 44 piksel.
2. **Kontras Teks >= 4.5:1:**
   - Slate 900 pada Putih = 15:1.
   - Emerald 800 pada Emerald 50 = 5.2:1.
   - Rose 900 pada Rose 100 = 7.1:1.
3. **Screen Reader Support:**
   - Setiap elemen form memiliki `<label for="...">`.
   - Perubahan status validitas rantai dibungkus atribut `role="status"` dan `aria-live="polite"`.

---

## 8. Fitur Tambahan (Diberi Tanda OPSIONAL)

1. **[OPSIONAL] Generator Kode QR Konsumen (FR-06):**
   - Menghasilkan gambar QR code di Tab 2 menggunakan library JavaScript ringan CDN (`qrcode.min.js`) agar konsumen dapat memindai tautan pelacakan langsung dari ponsel.
2. **[OPSIONAL] Tooltip Salin Cepat:**
   - Menampilkan animasi bubble kecil *"Sidik Jari Tersalin!"* selama 1.5 detik saat tombol salin diklik.

---

*Spesifikasi UI/UX ini menjadi acuan mutlak bagi tim pengembang dalam memastikan SimpleAgriChain ramah pengguna, adil tanpa bias, dan mudah dipahami orang awam.*


---

## 9. Revisi Penyederhanaan UI — 15 November 2026

**Pemicu:** umpan balik pengguna — tampilan terlalu ramai, pengguna bingung harus fokus ke mana.

**Prinsip revisi:** satu layar = satu keputusan. Elemen yang tidak dibutuhkan pada langkah saat ini disembunyikan, bukan dihapus (fitur demo tetap utuh).

| Area | Sebelum | Sesudah |
|---|---|---|
| Tab 1 | Dua formulir (Petani + Distributor) tampil bersamaan, 12 field terlihat | Pemilih peran `🧑‍🌾 Petani — catat panen` / `🚚 Distributor — catat kirim`; hanya 1 formulir (7 field) tampil |
| Tab 1 teks | 210 kata terlihat | 96 kata terlihat; field Pupuk + Kadar Air, Rute + Suhu jadi satu baris |
| Tab 2 | Panel "Sejauh mana sistem bisa dipercaya" (5 paragraf) di atas kotak pencarian | Kotak pencarian paling atas; panel jadi `<details>` terlipat (buka sesuai kebutuhan). 252 → 58 kata terlihat |
| Tab 3 | 3 kartu metrik terpisah | Satu strip ringkas: jumlah catatan + status keutuhan + catatan SHA-256 |
| Navigasi | `Tab 1: Input Transaksi` dst. (935 px di layar 390 px) | `1 · Input`, `2 · Lacak`, `3 · Buku Besar`, `4 · Uji Ubah` (548 px) |
| Judul tab | "Tab 1: Input Transaksi Rantai Pasok" dst. | "Catat Transaksi Baru", "Lacak Batch", "Buku Besar", "Uji Ubah Data" |

**Yang TIDAK berubah:** 4 tab, seluruh kontrak API, tombol preset demo (5 tombol tetap ada), alur tamper, badge status, QR, timeline. Panduan demo v2 tetap berlaku (hanya penyesuaian penyebutan "form kiri" → tombol peran).

**Bukti:** `docs/screenshots/05`–`08`, `tests/e2e_api.py` 35/35 PASS, nol error JavaScript, tanpa overflow horizontal di 390 px.


---

## 10. Revisi Perataan Layout (Presisi) — 15 November 2026

**Pemicu:** permintaan pengguna — "tinggal ketengahkan biar rapi, badge `▲ ADA CATATAN BERUBAH` di sebelah `SimpleAgriChain Web` dirapikan presisi, desktop & mobile".

**Satu kolom konten terpusat.** Header, navigasi, dan `<main>` memakai lebar sama `max-w-3xl` (768 px) dengan `mx-auto`, sehingga semua elemen berbagi satu sumbu tengah.

| Elemen | Sebelum | Sesudah |
|---|---|---|
| Header | Judul rata kiri, badge menempel di kanan (2 kolom, `justify-between`) | Judul + badge jadi **satu grup** yang di-center (`flex-wrap justify-center`); badge tepat di sebelah judul, jarak 12 px, satu baris di desktop dan turun ke baris kedua (tetap center) di mobile |
| Teks badge | `● CATATAN UTUH, TIDAK BERUBAH` (242 px) | `● CATATAN UTUH` (137 px) — versi panjang pindah ke strip Tab 3 |
| Navigasi tab | Rata kiri | `justify-center` di dalam kontainer selebar konten |
| `<main>` | `max-w-6xl` (1152 px) | `max-w-3xl` (768 px) ter-center |
| Pemilih peran + form Tab 1 | Rata kiri dalam kolom lebar | `mx-auto` di kolom 672 px ter-center |
| Judul tiap tab | Rata kiri | `text-center`; tombol Segarkan/Unduh di Tab 3 turun ke bawah judul, ikut center |
| Banner peringatan global | `max-w-6xl`, teks kiri | `max-w-3xl`, teks center di mobile |
| Metrik Tab 3 | `UTUH (semua sidik jari cocok)` / `BERUBAH (…)` | `UTUH` / `BERUBAH` supaya muat satu strip |

**Angka hasil ukur (viewport 1440, scrollbar 1425):** sumbu tengah viewport = 712,5 px; nav 713 px, `<main>` 713 px, pemilih peran 713 px, form 713 px, grup judul+badge 713 px → selisih ≤ 1 px. **Mobile 390 px:** badge `cx = 195` (tengah persis), `scrollWidth == clientWidth == 390`.

**Yang tidak berubah:** id elemen, kontrak API, alur demo, 4 tab, tombol preset, QR, timeline, banner tamper.


---

## 11. Realisasi Desain FigCraft ke Web — 15 November 2026

Sumber desain: `C:\Ouput Shiro\FigCraft\agrichain-v2\SimpleAgriChain-UI-v2.figcraft` (7 frame, sudah diedit pengguna).
File yang diubah: `templates/index.html`. Kontrak API, id elemen, dan alur demo tidak disentuh.

| Elemen | Desain FigCraft | Di web |
|---|---|---|
| Brand | kiri, icon `x=137` | `pl-[137px]` (desktop), center di mobile |
| Badge status | sejajar judul, `x=388`, tinggi 24 | `gap-7` dari brand, `py-1` (26 px) |
| Label nav | `Input` / `Lacak` / `Buku Besar` / `Uji Ubah` (tanpa angka) | sama, angka dihapus |
| Tinggi tab nav | 32 px | 32 px di ≥640 px (`.nav-tab-tight`), 44 px di mobile (touch target) |
| Tinggi header | 112 px | 114 px |
| Jarak header → konten | 28 px | `pt-7` |
| Jarak antar kartu | 16 px | `space-y-4` |
| Tab 1 | tanpa judul halaman | judul dihapus, `space-y-7` (28 px) |
| Tab 2 | judul tetap | judul tetap, `space-y-4` |
| Tab 3 | tanpa judul, tombol Segarkan/Unduh di atas strip | judul dihapus, tombol jadi baris ter-center |
| Tab 4 | tanpa judul | judul dihapus |
| Padding bawah | 32 px | `pb-8` |

**Selisih yang disengaja:** tab nav mobile tetap 44 px (touch target), bukan 32 px — header mobile jadi 160 px (desain 145 px). Semua id (`nav-tab-*`, `metric-*`, `chain-status-badge`, form fields) dipertahankan supaya JS dan `tests/e2e_api.py` tetap jalan.

**Verifikasi:** `tests/e2e_api.py` 35/35 PASS; submit petani + distributor, trace alert 35°C, tamper → badge `▲ ADA CATATAN BERUBAH`; nol error JS; mobile 390 px tanpa overflow horizontal.


---

## 12. Tab Dashboard — 15 November 2026

Tab **Dashboard** ditambahkan sebagai halaman awal (tab pertama di navbar), sebelum Input. Data dihitung dari `GET /api/chain` yang sudah ada — **tidak ada endpoint baru**, kontrak API tidak berubah.

| Blok | Isi | Sumber |
|---|---|---|
| Kartu "Catatan di buku" | jumlah blok termasuk #0 | `chain.length` |
| Kartu "Batch terdaftar" | Batch ID unik selain `GENESIS` | `chain[].batch_id` |
| Kartu "Keutuhan catatan" | `UTUH` / `BERUBAH` | `is_valid` |
| "Peringatan mutu" | batch dengan `kadar_air > 14` atau `suhu > 25`, lengkap alasannya; tombol Lacak | `chain[].data` |
| "Aktivitas terakhir" | 3 catatan terbaru (aktor, batch, waktu, ringkasan) | `chain[]` |
| Tombol aksi | `+ Catat transaksi` → Tab Input, `Lacak batch` → Tab Lacak | — |

**Perilaku:** `switchTab(5)` memuat ulang data; `loadBlockchain()` memanggil `renderDashboard()` sehingga angka ikut berubah setelah submit, tamper, atau reset. Tab 5 ikut di loop `switchTab` (`[5,1,2,3,4]`).

**Verifikasi:** keadaan kosong → total 1, batch 0, `UTUH`, "aman", "Belum ada transaksi"; setelah 2 batch (suhu 35°C + kadar air 18%) → total 4, batch 2, peringatan **2 batch** dengan alasan masing-masing; setelah tamper → `BERUBAH` + badge `▲ ADA CATATAN BERUBAH`; mobile 390 px tanpa overflow (nav digeser horizontal, 5 tab). Nol error JS.


---

## 13. Halaman Login & Pemisahan Peran — 15 November 2026

**Halaman baru:** `templates/login.html` — kartu tengah (max-w-md): brand, judul "Masuk", field Username + Password, tombol Masuk, kotak "Akun demo" berisi dua tombol isi-cepat (`admin / admin123`, `user / user123`), pesan galat merah kalau kredensial salah.

**Pemisahan di aplikasi:**

| Elemen | admin | user |
|---|---|---|
| Tab Dashboard, Lacak, Buku Besar | ✅ | ✅ |
| Tab Input (form petani/distributor) | ✅ | tidak dirender |
| Tab Uji Ubah (tamper + reset) | ✅ | tidak dirender |
| Tombol "+ Catat transaksi" di Dashboard | ✅ | tidak dirender |
| Tautan "Lihat di Tab Uji Coba" di banner | ✅ | tidak dirender |
| Badge peran di header | `ADMIN` (emerald) | `USER` (slate) |
| Tombol Keluar | ✅ | ✅ |

**Verifikasi (browser nyata):** tanpa sesi `/` → `302 /login`; password salah → pesan galat; login `user` → navbar 3 tab (`Dashboard`, `Lacak`, `Buku Besar`), `POST /api/block/petani` → **403**; login `admin` → navbar 5 tab, badge `ADMIN`, form petani ada; logout → kembali ke `/login`; mobile 390 px tanpa overflow.


---

## 14. Tampilan Konsumen (peran `user`) — 15 November 2026

**Alasan:** peran `user` sebelumnya hanya salinan layar admin tanpa tombol, sehingga tidak jelas untuk siapa. Sistem ini 3 aktor (Petani, Distributor, Konsumen/Auditor — `docs/plan.md` §1), jadi peran `user` diberi layar sendiri: **konsumen yang memverifikasi**, bukan operator yang mencatat.

| Aspek | admin (operator) | user (konsumen) |
|---|---|---|
| Halaman awal | Dashboard (ringkasan operasional) | **Lacak** (kotak cari + contoh Batch ID) |
| Navbar | Dashboard, Input, Lacak, Buku Besar, Uji Ubah | **Lacak, Buku Besar** |
| Dashboard internal (jumlah catatan, batch, peringatan) | ✅ | tidak dirender |
| Input transaksi & Uji Ubah | ✅ | tidak dirender |
| Kartu "Asal & penanganan" pada hasil lacak | tidak dirender (admin pakai timeline + buku besar) | ✅ 8 baris: lokasi lahan, tanggal panen, pupuk, sertifikat, kadar air, suhu transit tertinggi, rute, kondisi muatan |
| Label pencarian | "Cari Berdasarkan Batch ID Komoditas:" | "Masukkan Batch ID dari kemasan produk:" + hint bahwa ID ada di label/QR |
| QR & tautan `?batch=` | ✅ | ✅ (login dulu, lalu otomatis kembali ke batch tersebut) |

Banner risiko mutu, timeline perjalanan, kartu komoditas, dan QR tetap sama untuk kedua peran — itu inti bukti ketertelusuran.

**Verifikasi (browser):** user → navbar 2 tab, dashboard tidak ada, label konsumen, kartu asal 8 baris terisi (`Desa Sukatani, Karawang`, `12.5%`, `SNI-ORGANIK-2026-0881`), banner risiko suhu tampil, timeline 2 entri; alur QR anonim → login → kembali ke `/?batch=...` dan hasil langsung tampil; mobile 390 px tanpa overflow.


---

## 15. Audit & Perbaikan UI/UX Pro Max — 15 November 2026

Skill `ui-ux-pro-max` dipasang lalu dipakai untuk mengaudit UI yang **sudah jalan** (bukan menebak). Stack terdeteksi: `html-tailwind` (Flask + Jinja + vanilla JS, tanpa `package.json`). Design system dipersist ke `design-system/simpleagrichain/MASTER.md`.

### Temuan terukur (audit DOM langsung, semua tab + halaman login)

| Temuan | Nilai terukur | Aturan skill | Perbaikan | Hasil |
|---|---|---|---|---|
| Tombol hijau + teks putih | **3.77:1** (emerald-600 `#059669`) | Kontras ≥ 4.5:1 (prioritas 1) | emerald-600 → emerald-700 `#047857` | **5.48:1** ✅ |
| Tombol biru Distributor + putih | **4.10:1** (sky-600) | idem | sky-600 → sky-700 `#0369a1` | **5.93:1** ✅ |
| Teks chip "↓ catatan #N terikat…" | **2.56:1** (slate-400) | idem | slate-400 → slate-600 | **7.58:1** ✅ |
| Placeholder input | 2.56:1 (slate-400) | idem | placeholder slate-500 | **4.76:1** ✅ |
| Emoji sebagai ikon | 10 emoji (🧑‍🌾 🚚 ⚡ 💧 😇 🔄 ⚠️ ✓) | "Emoji as icons" = anti-pattern (prioritas 4) | semua diganti SVG inline (user, truck, bolt, droplet, eye, refresh, warning, check) | **0 emoji** ✅ |
| Loading state tombol | spinner ada, status aksesibilitas tidak | `aria-busy` untuk operasi async (prioritas 2/3) | `aria-busy=true` saat kirim, `false` setelah selesai (4 handler) | terverifikasi ✅ |
| Fokus keyboard | hanya sebagian kontrol punya `focus:ring` | Focus state wajib di semua kontrol (prioritas 1) | aturan global `:focus-visible` (outline 2px `#047857`, offset 2px) | ✅ |
| Animasi | `animate-pulse`/`animate-bounce` selalu jalan | `prefers-reduced-motion` (prioritas 7) | blok `@media (prefers-reduced-motion: reduce)` | ✅ |

**Sudah lulus tanpa perubahan:** `lang="id"`, `meta viewport`, target sentuh ≥ 44 px (0 pelanggaran), tidak ada scroll horizontal di 390 px, label form eksplisit (bukan placeholder-only), pesan galat dekat field (login), navigasi ≤ 5 tab.

**Bukti:** audit dijalankan ulang setelah perubahan → **0 pelanggaran kontras, 0 emoji** di login + 5 tab. `tests/e2e_api.py` **40/40 PASS**, `window.__errs` kosong.


---

## 16. Perbaikan: Data "Hilang" Setelah Logout + Daftar Batch untuk Konsumen — 16 November 2026

**Laporan pengguna:** setelah admin mengisi data lalu logout dan login lagi, seolah semua kembali dari awal; sebagai `user` data yang diisi admin tidak terlihat.

**Hasil pemeriksaan (bukan asumsi):** data **tidak pernah hilang**. Diuji lewat API dan browser:

| Uji | Hasil |
|---|---|
| Admin isi 3 blok → logout → login admin lagi | tetap **3 blok** |
| Restart server (`stop` + `run`) → buka lagi | tetap **3 blok** (dibaca dari `ledger_data.json`) |
| Login sebagai `user` | `GET /api/chain` mengembalikan **3 blok** |

**Penyebab sebenarnya — dua hal di tampilan/alat uji:**

1. **Konsumen tidak punya jalan masuk.** Halaman `user` membuka tab Lacak dengan kotak kosong dan chip contoh statis (`ORG-BRS-001`, `ORG-BRS-BASAH-001`) yang belum tentu ada. Data ada di buku besar, tapi tidak ada satu pun elemen yang menampilkannya → terlihat seperti "reset".
2. **Skrip uji menghapus data asli.** `tests/e2e_api.py` memanggil `/api/reset` pada server yang sedang jalan (port 5000). Setiap kali tes dijalankan, data demo pengguna ikut terhapus.

**Perbaikan:**

| Perubahan | Detail |
|---|---|
| Kartu **"Batch yang sudah tercatat"** di tab Lacak | daftar chip diambil dari `GET /api/chain` (bukan contoh statis), menampilkan jumlah batch, bisa diklik langsung untuk melacak. Muncul untuk admin maupun konsumen |
| Chip contoh statis dihapus | diganti daftar nyata; teks empty-state tidak lagi menyebut batch tertentu |
| `switchTab(2)` memuat data | sebelumnya tab Lacak tidak memicu `loadBlockchain()`, sehingga daftar kosong saat konsumen baru masuk |
| Tes terisolasi | `tests/e2e_api.py` menyalakan **server sendiri di port 5099** dengan `AGRICHAIN_LEDGER` sementara; data asli di port 5000 tidak disentuh |

**Bukti akhir (browser):** admin Dashboard 5 blok / 2 batch → logout → login admin → tetap 5 blok / 2 batch → logout → login `user` → daftar **2 batch** (ORG-PANEN-001, ORG-PANEN-002) → klik batch pertama → hasil lacak tampil (Beras Merah Organik, 8 baris asal & penanganan) → tab Buku Besar konsumen menunjukkan **5 catatan, UTUH**. Tes: **40/40 PASS** tanpa mengubah `ledger_data.json` (tetap 5 blok sebelum dan sesudah tes).


---

## 17. Halaman Daftar Akun — 16 November 2026

**Halaman baru:** `templates/register.html` (gaya sama dengan halaman Masuk: kartu putih, brand di atas, kartu hijau alamat LAN, tombol utama emerald-700).

| Elemen | Detail |
|---|---|
| Judul | "Daftar akun konsumen" + penjelasan bahwa akun baru berperan USER |
| Field | Username (hint aturan), Nama tampilan, Password, Ulangi password |
| Pesan galat | kotak merah di atas form, memakai `role="alert"` |
| Pesan sukses | muncul di halaman Masuk setelah redirect (`?registered=1`), kotak hijau `role="status"` |
| Tautan silang | halaman Masuk → "Daftar sebagai konsumen"; halaman Daftar → "Masuk di sini" |
| Aksesibilitas | semua field punya `<label>`, `autocomplete` benar (`username`, `new-password`), target sentuh ≥44 px, fokus terlihat |

**Verifikasi (browser):** halaman `/register` 200 dengan 4 field; daftar valid → `/login?registered=1` + pesan "Akun berhasil dibuat"; login akun baru → navbar 2 tab (Lacak · Buku Besar), badge **USER**, dan `POST /api/block/petani` → **403**; daftar dengan username kembar / password pendek / konfirmasi beda → 400 dengan pesan yang sesuai.


---

## 18. Realisasi Mockup FigCraft v3 ke Web — 22 November 2026

Mockup `SimpleAgriChain-UI-v3.figcraft` (11 frame) dipakai sebagai spesifikasi. Yang berubah di web:

| Perubahan | Detail |
|---|---|
| Halaman Masuk tanpa kartu alamat LAN | kartu hijau "Buka dari HP / laptop lain" dihapus; alamat hanya muncul di jendela server |
| Halaman Masuk tanpa blok "Akun demo" | tombol isi-cepat `admin/admin123` dan `user/user123` dihapus; akun tetap ada, diisi manual |
| Halaman Daftar tanpa judul + paragraf penjelasan | kartu langsung berisi 4 isian |
| Header tanpa chip alamat LAN | chip `http://192.168.x.x:5000` dihapus dari header semua peran |
| Navbar 5 tab untuk semua peran | konsumen kini melihat Dashboard, Input, Lacak, Buku Besar, Uji Ubah |
| Tab khusus admin dinonaktifkan untuk konsumen | tiga tab memakai `aria-disabled="true"`, teks `text-slate-300`, `cursor-not-allowed`, `title="Khusus admin"`, tanpa handler |
| Kotak "Contoh isian cepat" jadi satu baris | latar kotak dihapus; label "Isi contoh:" + dua tombol kecil tetap ada supaya demo tidak perlu mengetik 7 isian |

**Gerbang:** `tests/e2e_api.py` **48/48 PASS**; tanpa overflow horizontal pada 1440 dan 390; kartu Masuk 448x362, kartu Daftar 448x478.

**Tambahan (22 Nov):** baris catatan kaki `AgriChain — prototipe ketertelusuran pangan berbasis buku besar` dihapus dari halaman Masuk dan Daftar. Kedua halaman kini berakhir di tautan silang (Daftar sebagai konsumen / Masuk di sini).
