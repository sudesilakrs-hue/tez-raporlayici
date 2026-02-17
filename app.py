import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tez Veri Raporlayıcı", layout="wide")
st.title("📊 CSV / Excel → Otomatik Analiz Raporu")

# Dosya yükleme
uploaded = st.file_uploader("CSV veya Excel dosyası yükleyin", type=["csv", "xlsx"])

if uploaded is not None:
    
    # Dosya okuma
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)

    st.subheader("🔍 Veri Önizleme")
    st.dataframe(df.head())

    st.subheader("📌 Genel Bilgiler")
    st.write(f"Satır sayısı: {df.shape[0]}")
    st.write(f"Sütun sayısı: {df.shape[1]}")

    st.subheader("📈 Özet İstatistik")
    st.dataframe(df.describe())

    st.subheader("❗ Eksik Değerler")
    missing = df.isnull().sum()
    st.dataframe(missing[missing > 0])

    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

    if len(numeric_columns) > 0:
        st.subheader("📊 Grafik")

        selected_column = st.selectbox(
            "Grafik için sayısal sütun seçin",
            numeric_columns
        )

        fig, ax = plt.subplots()
        df[selected_column].hist(bins=20, ax=ax)
        ax.set_title(f"{selected_column} Histogram")
        st.pyplot(fig)

    else:
        st.warning("Sayısal sütun bulunamadı.")
