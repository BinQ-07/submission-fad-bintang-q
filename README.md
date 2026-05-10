# Proyek Analisis Data: Bike Sharing Dataset 🚲
Selamat datang di repositori Proyek Analisis Data Bike Sharing. Dashboard ini dirancang untuk mengeksplorasi pola peminjaman sepeda dari dataset Capital Bikeshare secara intuitif dan informatif. Dengan tampilan yang bersih dan filter yang fleksibel, kamu dapat memahami bagaimana musim, kondisi cuaca, dan waktu memengaruhi perilaku pengguna sepeda.

## 📊 Dashboard Demo
Visualisasi dapat dilihat secara langsung di: [Streamlit App](https://submission-fad-bintang-q.streamlit.app/)

---

## 📜 Tentang Dataset

Dataset yang digunakan adalah **Capital Bikeshare** yang mencatat peminjaman sepeda per jam selama dua tahun (2011–2012) di Washington D.C., Amerika Serikat. Dataset mencakup 17.379 baris data dengan informasi seperti musim, cuaca, suhu, kelembapan, hari kerja, serta jumlah pengguna kasual dan terdaftar.

---

## Pertanyaan Bisnis

Analisis ini dirancang untuk menjawab beberapa pertanyaan bisnis utama:

1.  Bagaimana kondisi cuaca ekstrem memengaruhi penurunan rata-rata jumlah penyewaan sepeda harian pada tahun 2011 dan 2012 di Washington D.C.?
2. Pada musim apa terjadi puncak permintaan penyewaan sepeda tertinggi, dan bagaimana proporsi pengguna `casual` dan `registered` pada periode tersebut?

---

## ✨ Fitur Dashboard

- **KPI Summary Cards** — Menampilkan total peminjaman, jumlah pengguna kasual, pengguna terdaftar, dan rata-rata peminjaman per hari secara ringkas di bagian atas halaman.
- **Filter Interaktif** — Sidebar dilengkapi filter berdasarkan musim, tahun, dan kondisi cuaca yang dapat dikombinasikan secara bebas untuk menyesuaikan tampilan grafik.
- **Tab Penyewaan per Musim** — Grouped bar chart yang membandingkan total peminjaman kasual vs terdaftar per musim, dilengkapi label pertumbuhan antar musim, stacked bar proporsi, dan donut chart kontribusi.
- **Tab Penyewaan per Cuaca** — Grouped bar chart rata-rata peminjaman harian berdasarkan kondisi cuaca untuk tahun 2011 dan 2012, serta heatmap interaktif cuaca × musim.

---

## 🛠️ Teknologi yang Digunakan

-   **Analisis Data**: Python, Pandas, NumPy
-   **Visualisasi Data**: Matplotlib, Seaborn
-   **Dashboard Interaktif**: Streamlit

---

## 🚀 Cara Menjalankan Proyek Secara Lokal

**1. Setup Environment**
- pipenv
```bash
pipenv install
pipenv shell
```

**2. Install dependensi**

```bash
pip install -r requirements.txt
```

**3. Jalankan dashboard Streamlit**

```bash
streamlit run dashboard/dashboard.py
```

---

## 📁 Struktur Repositori
```
.
├── dashboard/
│   └── dashboard.py      # File utama aplikasi Streamlit
│
├── data/
│   ├── day.csv           # Dataset bike sharing harian
│   └── hour.csv          # Dataset bike sharing per jam
│
├── notebook.ipynb        # Notebook Jupyter berisi proses analisis data
├── requirements.txt      # File daftar dependensi Python yang diperlukan
└── README.md             # Dokumentasi proyek (file ini)
```
