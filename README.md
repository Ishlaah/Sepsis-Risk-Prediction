# Sepsis Risk Prediction

## 1. Deskripsi Proyek

Proyek ini merupakan implementasi **API berbasis Machine Learning untuk memprediksi risiko sepsis** berdasarkan data klinis pasien.
Model yang digunakan memanfaatkan pendekatan **ensemble learning** dengan menggabungkan **XGBoost** dan **Artificial Neural Network (ANN)** untuk meningkatkan performa prediksi.

API dikembangkan menggunakan **FastAPI** dan dikemas dalam **Docker container** sehingga mudah dijalankan dan direproduksi di berbagai environment.

Tujuan utama dari proyek ini adalah menyediakan layanan prediksi sederhana yang mampu memperkirakan **probabilitas risiko sepsis** berdasarkan beberapa indikator klinis seperti:

* Heart rate
* Respiratory rate
* Temperature
* White blood cell count (WBC)
* Lactate level
* Age
* Number of comorbidities

---

# 2. Pendekatan Machine Learning

## Data Processing

Beberapa tahapan yang dilakukan dalam proses persiapan data:

* Data cleaning
* Penanganan missing values menggunakan **imputation**
* Feature scaling menggunakan **StandardScaler**
* Pembagian dataset menjadi **data training dan data testing**

Pipeline preprocessing disimpan dalam file `preprocessor.pkl` untuk memastikan proses transformasi data saat **training dan inference tetap konsisten**.

---

## Arsitektur Model

Sistem menggunakan pendekatan **ensemble learning** dengan dua model utama:

### Model 1 — XGBoost

Model berbasis **gradient boosting** yang sangat efektif untuk data tabular dan mampu menangkap hubungan kompleks antar fitur.

### Model 2 — Artificial Neural Network (ANN)

Model deep learning yang mampu menangkap **pola non-linear** dalam data.

---

## Strategi Ensemble

Prediksi akhir dihitung menggunakan **weighted average** dari kedua model:

```id="wqle8s"
Final Probability = 0.6 × XGBoost + 0.4 × ANN
```

Pendekatan ini bertujuan untuk memanfaatkan kelebihan masing-masing model sehingga menghasilkan prediksi yang lebih stabil.

---

# 3. Performa Model

Evaluasi model dilakukan menggunakan beberapa metrik utama:

| Metric    | Score |
| --------- | ----- |
| ROC-AUC   | 1.00  |
| Precision | 1.00  |
| Recall    | 1.00  |

Nilai ROC-AUC yang sangat tinggi menunjukkan bahwa model mampu memisahkan kelas **sepsis** dan **non-sepsis** dengan sangat baik pada dataset yang digunakan.

---

# 4. Struktur Proyek

```id="w9ejup"
prediksi-sepsis/
│
├── api/
│   └── app.py
│
├── model/
│   ├── preprocessor.pkl
│   ├── xgb_model.pkl
│   └── ann_model.h5
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# 5. Menjalankan API Menggunakan Docker

## Langkah 1 — Build Docker Image

Jalankan perintah berikut pada folder proyek:

```id="klo0ob"
docker build -t sepsis-api .
```

---

## Langkah 2 — Menjalankan Docker Container

```id="d6t6a7"
docker run -p 8000:8000 sepsis-api
```

Setelah container berjalan, API dapat diakses melalui:

```id="24pnn3"
http://localhost:8000
```

Dokumentasi API otomatis tersedia di:

```id="qmt2bg"
http://localhost:8000/docs
```

---

# 6. Endpoint API

## POST /predict

Endpoint ini digunakan untuk memprediksi risiko sepsis berdasarkan data pasien.

### Contoh Input JSON

```id="kwr8ht"
{
  "heart_rate": 110,
  "respiratory_rate": 28,
  "temperature": 39,
  "wbc_count": 15,
  "lactate_level": 3.5,
  "age": 65,
  "num_comorbidities": 2
}
```

### Contoh Output

```id="nlbdie"
{
  "sepsis_risk_prediction": 1,
  "risk_probability": 0.92
}
```

Keterangan:

* `1` → Risiko tinggi sepsis
* `0` → Risiko rendah sepsis

---

# 7. Contoh Mengirim Request ke API

## Menggunakan curl

```id="dzfd29"
curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{
  "heart_rate": 110,
  "respiratory_rate": 28,
  "temperature": 39,
  "wbc_count": 15,
  "lactate_level": 3.5,
  "age": 65,
  "num_comorbidities": 2
}'
```

---

## Menggunakan Python

```id="2c0zh3"
import requests

url = "http://localhost:8000/predict"

data = {
    "heart_rate":110,
    "respiratory_rate":28,
    "temperature":39,
    "wbc_count":15,
    "lactate_level":3.5,
    "age":65,
    "num_comorbidities":2
}

response = requests.post(url, json=data)

print(response.json())
```

---
