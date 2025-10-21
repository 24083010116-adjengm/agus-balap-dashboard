import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# 1. KONFIGURASI DASAR
# ==========================
st.set_page_config(page_title="Dashboard Kuisioner", layout="wide")

# ==========================
# 2. TEMA & WARNA SESUAI CONFIG.TOML (langsung di sini)
# ==========================
st.markdown("""
<style>
/* ====== WARNA UTAMA ====== */
body, [data-testid="stAppViewContainer"] {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* ====== SIDEBAR ====== */
[data-testid="stSidebar"] {
    background-color: #ea0093 !important;
}
[data-testid="stSidebar"] * {
    color: #ffffff !important;
    font-weight: bold;
}

/* ====== TEKS & JUDUL ====== */
h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, label, p {
    color: #ffffff !important;
}

/* ====== TOMBOL ====== */
div.stButton > button {
    background-color: #7d004c !important;
    color: white !important;
    border-radius: 10px;
    font-weight: bold;
    border: none;
}
div.stButton > button:hover {
    background-color: #ea0093 !important;
    color: white !important;
}

/* ====== ALERT (SUCCESS, WARNING, DLL) ====== */
.stAlert {
    background-color: #7d004c !important;
    color: white !important;
    border-radius: 10px;
}

/* ====== TABEL ====== */
.dataframe, .stDataFrame, .stTable {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* ====== HAPUS LOGO STREAMLIT ====== */
#MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================
# 3. JUDUL UTAMA
# ==========================
st.title("🎮 Dashboard Analisis Gaming dan Hobi Digital Mahasiswa: Antara Hiburan, Produktivitas, dan Gaya Hidup")

# ==========================
# 4. LOAD DATA
# ==========================
@st.cache_data
def load_data():
    df = pd.read_csv("kuisioner_final.csv", low_memory=False)
    return df

df = load_data()

# ==========================
# 5. SIDEBAR MENU
# ==========================
st.sidebar.title("📂 Menu Navigasi")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Home", "📄 Data", "📈 Statistik", "📊 Visualisasi"]
)

# ==========================
# 6. HALAMAN HOME
# ==========================
if menu == "🏠 Home":
    st.header("by AGUS BALAP - SAINS DATA - UPN VETERAN JAWA TIMUR 🧠")
    st.write("""
    **Anggota Kelompok:**  
    Nadia Raissa Romadhoni (24083010031) | Muhammad Jafier Nur Aldany (24083010070) | Adjeng Mustikaningrum (24083010116)
    """)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("📌 Deskripsi Data")
        st.write("""
        Dataset ini merupakan hasil survei terhadap mahasiswa UPN “Veteran” Jawa Timur untuk menganalisis **fenomena aktivitas gaming dan hobi digital** di kalangan mahasiswa serta keterkaitannya dengan **produktivitas dan gaya hidup**.  
        Data yang digunakan telah melalui proses pembersihan (*data cleaning*) agar valid dan siap untuk dianalisis.  

        Dataset mencakup **13 variabel**, meliputi:
        - **Identitas responden** (Jenis Kelamin, Usia, Program Studi)  
        - **Kebiasaan digital** (Jenis Hobi, Frekuensi, Durasi Bermain, Platform yang digunakan)  
        - **Dampak terhadap akademik** (Produktivitas Belajar, Manajemen Waktu, Motivasi)  
        - **Aspek sosial dan gaya hidup** (Kualitas Istirahat, Interaksi Sosial, Kesehatan Mental)  
        """)

    with col2:
        st.subheader("📎 Sumber Data")
        st.write("""
        Data dikumpulkan melalui **kuisioner online** yang disebarkan kepada mahasiswa dari berbagai program studi di UPN “Veteran” Jawa Timur.  
        Sebanyak **172 responden** berpartisipasi, mewakili beragam jurusan dan angkatan.
        """)

        st.subheader("🎯 Tujuan Dashboard")
        st.write("""
        Dashboard ini bertujuan untuk:
        - Menyajikan **gambaran menyeluruh** mengenai kebiasaan digital mahasiswa  
        - Menganalisis **hubungan antara intensitas aktivitas digital dan produktivitas akademik**  
        - Menyediakan **insight interaktif** untuk eksplorasi data secara visual
        """)

    st.success("Silakan pilih menu di sidebar untuk memulai!")

# ==========================
# 7. HALAMAN DATA
# ==========================
elif menu == "📄 Data":
    st.header("📄 Data Kuisioner")
    st.write("Berikut adalah data yang telah dibersihkan:")
    st.dataframe(df)

    st.download_button(
        label="📥 Download Data CSV",
        data=df.to_csv(index=False),
        file_name="kuisioner_final.csv",
        mime="text/csv"
    )

# ==========================
# 8. HALAMAN STATISTIK
# ==========================
elif menu == "📈 Statistik":
    st.header("📈 Statistik Deskriptif")
    st.write(df.describe())

    st.subheader("🔍 Informasi Data")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Jumlah Baris:", df.shape[0])
    with col2:
        st.write("Jumlah Kolom:", df.shape[1])

# ==========================
# 9. HALAMAN VISUALISASI
# ==========================
elif menu == "📊 Visualisasi":
    st.header("📊 Visualisasi Data")

    # Deteksi tipe kolom
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    excluded_cols = ['Nama', 'Ketersediaan']
    categorical_cols = [col for col in categorical_cols if col not in excluded_cols]
    numeric_cols = [col for col in numeric_cols if col not in excluded_cols]

    # Dua kolom layout
    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.subheader("⚙️ Pengaturan Visualisasi")
        chart_type = st.selectbox("Pilih Jenis Grafik:", ["Bar Chart", "Pie Chart", "Scatter Plot"])

        if chart_type == "Bar Chart":
            col = st.selectbox("Pilih Kolom Kategorik:", categorical_cols)
        elif chart_type == "Pie Chart":
            col = st.selectbox("Pilih Kolom Kategorik:", categorical_cols)
        elif chart_type == "Scatter Plot":
            if len(numeric_cols) >= 2:
                x = st.selectbox("Pilih Sumbu X:", numeric_cols)
                y = st.selectbox("Pilih Sumbu Y:", numeric_cols)
            else:
                st.warning("Tidak cukup kolom numerik untuk scatter plot.")

    with right_col:
        st.subheader("📈 Hasil Visualisasi")

        if chart_type == "Bar Chart":
            fig, ax = plt.subplots()
            df[col].value_counts().plot(kind='bar', color='#EA0093', ax=ax)
            ax.set_title(f"Distribusi {col}", color='#ffffff')
            ax.set_xlabel(col, color='#ffffff')
            ax.set_ylabel("Frekuensi", color='#ffffff')
            ax.tick_params(colors='white')
            fig.patch.set_facecolor('#000000')
            st.pyplot(fig)

        elif chart_type == "Pie Chart":
            fig, ax = plt.subplots()
            df[col].value_counts().plot(
                kind='pie',
                autopct='%1.1f%%',
                startangle=90,
                ax=ax,
                colors=["#EA0093", "#7D004C", "#FF66CC", "#FF99FF"]
            )
            ax.set_ylabel("")
            ax.set_title(f"Proporsi {col}", color='#ffffff')
            fig.patch.set_facecolor('#000000')
            st.pyplot(fig)

        elif chart_type == "Scatter Plot":
            if len(numeric_cols) >= 2:
                fig, ax = plt.subplots()
                ax.scatter(df[x], df[y], color='#EA0093')
                ax.set_xlabel(x, color='#ffffff')
                ax.set_ylabel(y, color='#ffffff')
                ax.set_title(f"Scatter Plot: {x} vs {y}", color='#ffffff')
                ax.tick_params(colors='white')
                fig.patch.set_facecolor('#000000')
                st.pyplot(fig)
