
# Tugas 3 — Data Acquisition

## Analisis Pertumbuhan Ekonomi dan Tingkat Pengangguran Negara G20 Periode 2010–2024

**Nama:** Ayang Nova Anggraeni  
**NIM:** 2310631170126  
**Mata Kuliah:** Data Engineering

---

## 1. Deskripsi Kasus

Pertumbuhan ekonomi dan tingkat pengangguran merupakan dua indikator yang dapat digunakan untuk menggambarkan kondisi perekonomian suatu negara.

Pada tugas ini dilakukan proses data acquisition untuk memperoleh data pertumbuhan ekonomi dan tingkat pengangguran dari World Bank Open Data. Data yang dikumpulkan mencakup 19 negara anggota G20 selama periode 2010–2024.

Proses akuisisi dilakukan menggunakan World Bank REST API dengan metode HTTP GET. Response API dalam format JSON kemudian dikonversi menjadi Pandas DataFrame, dilakukan transformasi dan pemeriksaan kualitas data, kemudian disimpan dalam format CSV dan Parquet.

---

## 2. Tujuan

Tujuan dari project ini adalah:

1. Mengambil data ekonomi dari World Bank Open Data menggunakan REST API.
2. Menggunakan HTTP GET untuk melakukan proses data acquisition.
3. Mengambil data dari beberapa negara dan indikator.
4. Menerapkan pagination untuk memperoleh seluruh data dari API.
5. Mengubah response JSON menjadi Pandas DataFrame.
6. Melakukan transformasi dan cleaning dasar terhadap data.
7. Melakukan pemeriksaan kualitas data.
8. Menyimpan dataset hasil akuisisi dalam format CSV dan Parquet.

---

## 3. Sumber Data

### World Bank Open Data

**Website:**  
https://data.worldbank.org/

**World Bank REST API:**  
https://api.worldbank.org/v2/

Data diperoleh menggunakan World Bank REST API v2.

Tidak diperlukan API key untuk endpoint yang digunakan pada project ini.

---

## 4. API Endpoint

Endpoint utama yang digunakan:

```text
https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}
```
````

Parameter yang digunakan:

| Parameter  | Keterangan                              |
| ---------- | --------------------------------------- |
| `date`     | Membatasi periode data, yaitu 2010–2024 |
| `format`   | Format response JSON                    |
| `per_page` | Jumlah data yang diminta per halaman    |
| `page`     | Nomor halaman API                       |

Contoh struktur request:

```text
https://api.worldbank.org/v2/country/ARG;AUS;BRA/indicator/NY.GDP.MKTP.KD.ZG?date=2010:2024&format=json&per_page=100&page=1
```

---

## 5. Indikator

Project menggunakan dua indikator World Bank.

| Variabel     | Indikator                                    | Indicator Code      | Satuan     |
| ------------ | -------------------------------------------- | ------------------- | ---------- |
| GDP Growth   | GDP growth (annual %)                        | `NY.GDP.MKTP.KD.ZG` | Persen (%) |
| Unemployment | Unemployment, total (% of total labor force) | `SL.UEM.TOTL.ZS`    | Persen (%) |

### 5.1 GDP Growth

**Indicator Code:**

```text
NY.GDP.MKTP.KD.ZG
```

Indikator ini merepresentasikan pertumbuhan GDP tahunan dalam persen.

### 5.2 Unemployment

**Indicator Code:**

```text
SL.UEM.TOTL.ZS
```

Indikator ini merepresentasikan tingkat pengangguran sebagai persentase dari total angkatan kerja.

---

## 6. Negara dan Periode

### Negara

Data dikumpulkan untuk 19 negara anggota G20 berikut:

| Country        | ISO3 Code |
| -------------- | --------- |
| Argentina      | `ARG`     |
| Australia      | `AUS`     |
| Brazil         | `BRA`     |
| Canada         | `CAN`     |
| China          | `CHN`     |
| France         | `FRA`     |
| Germany        | `DEU`     |
| India          | `IND`     |
| Indonesia      | `IDN`     |
| Italy          | `ITA`     |
| Japan          | `JPN`     |
| Mexico         | `MEX`     |
| Russia         | `RUS`     |
| Saudi Arabia   | `SAU`     |
| South Africa   | `ZAF`     |
| South Korea    | `KOR`     |
| Türkiye        | `TUR`     |
| United Kingdom | `GBR`     |
| United States  | `USA`     |

European Union (`EU`) tidak digunakan sebagai observasi karena merupakan agregat kawasan, bukan negara anggota individual.

### Periode

```text
2010–2024
```

Jumlah tahun:

```text
15 tahun
```

Jumlah observasi yang diharapkan:

```text
19 negara × 15 tahun × 2 indikator = 570 observasi
```

---

## 7. Metode Data Acquisition

Proses data acquisition terdiri dari beberapa tahap:

```text
World Bank REST API
        ↓
Extract
        ↓
Transform
        ↓
Validate
        ↓
Load
        ↓
CSV + Parquet
```

### 7.1 Extract

Tahap extraction dilakukan menggunakan Python `requests` dengan HTTP GET.

Implementasi mencakup:

- HTTP GET request
- request timeout 30 detik
- HTTP status checking menggunakan `raise_for_status()`
- penanganan timeout
- penanganan HTTP error
- penanganan request error
- validasi dasar terhadap format JSON
- pagination otomatis

API menggunakan pagination karena jumlah response lebih besar dari satu halaman. Program membaca metadata API untuk mengetahui jumlah halaman dan mengambil data hingga seluruh halaman selesai.

### 7.2 Transform

Tahap transformasi dilakukan menggunakan Pandas.

Transformasi meliputi:

1. Memilih kolom yang relevan.
2. Mengekstrak nama negara dari nested object.
3. Mengekstrak nama indikator dari nested object.
4. Mengubah nama kolom menjadi lebih sederhana.
5. Mengubah tipe data tahun menjadi integer nullable.
6. Mengubah nilai indikator menjadi numeric.
7. Mengurutkan data berdasarkan negara, tahun, dan indikator.

Dataset akhir memiliki struktur:

| Column               | Description                                |
| -------------------- | ------------------------------------------ |
| `country_code`       | ISO3 country code                          |
| `country`            | Nama negara                                |
| `year`               | Tahun observasi                            |
| `indicator_name`     | Nama indikator                             |
| `indicator_variable` | Nama variabel yang digunakan dalam project |
| `value`              | Nilai indikator                            |

### 7.3 Validate

Pemeriksaan kualitas data meliputi:

- tipe data setiap kolom
- keberadaan nested dictionary setelah transformasi
- jumlah baris dan kolom
- missing values
- duplicate observations
- jumlah negara
- jumlah observasi setiap indikator
- rentang tahun

### 7.4 Load

Dataset hasil transformasi disimpan dalam dua format:

```text
data/hasil_data.csv
data/hasil_data.parquet
```

---

## 8. Hasil Data Acquisition

Hasil akhir proses acquisition:

| Parameter                 |     Hasil |
| ------------------------- | --------: |
| Jumlah negara             |        19 |
| Jumlah indikator          |         2 |
| Periode                   | 2010–2024 |
| Jumlah tahun              |        15 |
| Total observasi           |       570 |
| Missing values            |         0 |
| Duplicate observations    |         0 |
| GDP Growth observations   |       285 |
| Unemployment observations |       285 |

Jumlah observasi sesuai dengan jumlah observasi yang diharapkan:

```text
19 × 15 × 2 = 570
```

Dataset berhasil disimpan dalam format CSV dan Parquet.

---

## 9. Struktur Project

```text
Tugas3_2310631170126_Ayang_Nova_Anggraeni/
│
├── data/
│   ├── hasil_data.csv
│   └── hasil_data.parquet
│
├── notebooks/
│   └── Tugas3_2310631170126_Ayang_Nova_Anggraeni.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load.py
│   └── pipeline.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

### Penjelasan Folder

#### `data/`

Berisi dataset hasil akhir proses acquisition:

- `hasil_data.csv`
- `hasil_data.parquet`

#### `notebooks/`

Berisi Jupyter Notebook yang digunakan untuk mendokumentasikan dan mendemonstrasikan proses data acquisition.

#### `src/`

Berisi source code utama project:

- `config.py` — konfigurasi API, negara, indikator, dan periode.
- `extract.py` — proses pengambilan data dari World Bank API.
- `transform.py` — proses cleaning dan transformasi.
- `validate.py` — pemeriksaan kualitas data.
- `load.py` — penyimpanan dataset ke CSV dan Parquet.
- `pipeline.py` — menjalankan seluruh tahapan pipeline.

---

## 10. Requirements

Project menggunakan beberapa package utama berikut:

```text
pandas==3.0.5
requests==2.34.2
pyarrow==25.0.1
```

Install dependencies dengan:

```bash
pip install -r requirements.txt
```

---

## 11. Cara Menjalankan

Pastikan virtual environment telah aktif.

### Menjalankan Pipeline

Dari project root:

```bash
python -m src.pipeline
```

Pipeline akan menjalankan tahapan:

```text
Extract → Transform → Validate → Load
```

Hasil dataset akan disimpan ke:

```text
data/hasil_data.csv
data/hasil_data.parquet
```

### Menjalankan Notebook

Buka file:

```text
notebooks/Tugas3_2310631170126_Ayang_Nova_Anggraeni.ipynb
```

Kemudian jalankan cell secara berurutan untuk melihat dokumentasi dan demonstrasi proses data acquisition.

Notebook menggunakan fungsi yang terdapat pada folder `src/`, sehingga logic utama tidak diduplikasi di dalam notebook.

---

## 12. Acquisition Timestamp

Waktu akuisisi dicatat pada saat proses data acquisition dijalankan melalui Python Notebook.

Timestamp mengikuti waktu lokal environment tempat proses acquisition dijalankan.

---

## 13. Keterbatasan Data

Beberapa keterbatasan project ini adalah:

1. Data bergantung pada ketersediaan dan pembaruan data dari World Bank.
2. World Bank dapat melakukan revisi terhadap data historis.
3. Dataset hanya mencakup 19 negara G20.
4. Periode data dibatasi pada 2010–2024.
5. Dataset hanya menggunakan dua indikator.
6. Project berfokus pada proses data acquisition dan tidak melakukan analisis statistik, machine learning, atau dashboard lebih lanjut.

---

## 14. Kesimpulan

Proses data acquisition berhasil dilakukan menggunakan World Bank Open Data REST API.

Data berhasil diperoleh untuk 19 negara, 2 indikator, dan periode 2010–2024 dengan total 570 observasi.

Proses acquisition menggunakan HTTP GET, timeout handling, HTTP status checking, basic error handling, dan pagination.

Response JSON berhasil dikonversi menjadi Pandas DataFrame dan melalui tahapan transformasi serta validasi data. Hasil akhir tidak memiliki missing values maupun duplicate observations dan berhasil disimpan dalam format CSV dan Parquet.

Dengan demikian, seluruh tahapan data acquisition dari extraction, transformation, validation, hingga loading berhasil diimplementasikan.

```

```
