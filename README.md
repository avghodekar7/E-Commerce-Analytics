# 🛍️ E-Commerce Analytics

An interactive **E-Commerce Customer and Product Analysis** dashboard built using **Apache Hive, Hadoop/HDFS, Python, and Streamlit**.

The project analyzes the **Online Retail dataset** to identify revenue trends, product performance, customer insights, and international market patterns. The results generated through HiveQL are compiled into an Excel dataset and visualized through an interactive Streamlit dashboard.

---

## 📌 Project Overview

The objective of this project is to perform e-commerce data analysis using the Hadoop and Hive ecosystem and present the resulting business insights through an interactive dashboard.

### Project Workflow

```text
Online Retail Dataset
        ↓
     Hadoop
      HDFS
        ↓
   Apache Hive
        ↓
     HiveQL
        ↓
Compiled Analysis Results
        ↓
      Excel
        ↓
    Streamlit
        ↓
Interactive Dashboard
```

---

## ✨ Dashboard Features

### 📊 Revenue Analysis
- Monthly revenue trends
- Revenue performance across different periods
- Overall revenue KPIs

### 🛍️ Product Analysis
- Top products by revenue
- Top products by quantity sold
- Product-level performance comparison

### 🌍 Market Analysis
- Revenue by country
- Transaction/record distribution by country
- International market performance

### 📈 Key Performance Indicators
- Total Revenue
- Completed Orders
- Unique Customers
- Cancellation Line Items
- Valid Records

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Hadoop HDFS** | Distributed storage of the retail dataset |
| **Apache Hive** | Data warehousing and analysis |
| **HiveQL** | Querying and aggregating e-commerce data |
| **Python** | Data processing and dashboard development |
| **Pandas** | Data handling and analysis |
| **Plotly** | Interactive visualizations |
| **Streamlit** | Interactive dashboard |
| **Excel** | Compiled Hive analysis results |

---

## 📂 Project Structure

```text
E-Commerce/
│
├── app.py
├── Ecommerce_Hive_PowerBI_Data.xlsx
├── requirements.txt
├── .gitignore
└── README.md
```

### File Description

- `app.py` — Streamlit dashboard application
- `Ecommerce_Hive_PowerBI_Data.xlsx` — compiled results generated from Hive analysis
- `requirements.txt` — required Python packages
- `.gitignore` — files excluded from Git tracking
- `README.md` — project documentation

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/avghodekar7/E-Commerce-Analytics.git
cd E-Commerce-Analytics
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit dashboard

```bash
python -m streamlit run app.py
```

The dashboard will open locally at:

```text
http://localhost:8501
```

---

## 📊 Data Source

The project uses the **Online Retail dataset**, containing transactional e-commerce data including:

- Invoice number
- Product/stock code
- Product description
- Quantity
- Invoice date
- Unit price
- Customer ID
- Country

The dataset was processed and analyzed using **Hadoop HDFS and Apache Hive**.

---

## 🔍 Analysis Performed

The Hive-based analysis focuses on:

- Monthly revenue trends
- Top-selling products
- Highest-revenue products
- Country-wise revenue
- Country-wise transaction records
- Customer-related metrics
- Order and cancellation analysis

The resulting datasets are compiled into an Excel workbook that is consumed by the Streamlit dashboard.

---

## 🎯 Project Objective

To demonstrate an end-to-end **Big Data Analytics workflow** by combining distributed storage, Hive-based data analysis, and interactive visualization for extracting meaningful insights from e-commerce transaction data.

---

## 👩‍💻 Author

**Anushka Ghodekar**

GitHub: [@avghodekar7](https://github.com/avghodekar7)
