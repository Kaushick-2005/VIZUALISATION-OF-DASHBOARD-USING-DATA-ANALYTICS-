# 📊 Visual Analytics Dashboard for Region-Wise Sales and Customer Insights

## 📌 Project Overview
This project focuses on developing an interactive visual analytics dashboard to analyze region-wise sales performance and customer insights using real-world business data.

## 🔗 Dataset
Superstore Dataset from Kaggle  
https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

## 🛠 Tech Stack
# 📊 Visual Analytics Dashboard for Region-Wise Sales and Customer Insights

## 📌 Project Overview
This project provides an interactive Streamlit dashboard to explore region-wise sales, customer insights, product performance, and basic segmentation using the Superstore dataset.

## 🔗 Dataset
Superstore Dataset (included in `data/superstore.csv`)

## 🛠 Tech Stack
- Python
- Pandas & NumPy
- Plotly & Seaborn
- Streamlit

## ▶️ How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📦 What I added
- Modularized code under `src/` (`data_processing.py`, `visuals.py`) for reuse and testing.
- Multi-page Streamlit app in `app.py` (Overview, Region Insights, Customer Insights, Product Insights).
- RFM calculation and a US-state choropleth (uses state mapping in `src/data_processing.py`).
- Updated `requirements.txt` and added `.gitignore`.

## 🔧 Prepare & Push to GitHub
If you already have a GitHub repo, run:

```bash
git init
git add .
git commit -m "Add modular Streamlit dashboard and data processing"
git branch -M main
git remote add origin <YOUR_REMOTE_URL>
git push -u origin main
```

Replace `<YOUR_REMOTE_URL>` with your GitHub repository URL.

## ✅ Notes
- The dataset (`data/superstore.csv`) is included for local runs; remove or ignore it if you do not want to commit data.
- For production, consider Dockerizing the app and adding CI/CD.
