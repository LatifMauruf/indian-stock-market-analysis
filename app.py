import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Indian Stock Market Analysis",
    page_icon="🇮🇳",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 16px;
    color: #666;
    margin-bottom: 25px;
}

[data-testid="stMetric"] {
    border: 1px solid rgba(128,128,128,0.20);
    border-radius: 12px;
    padding: 15px;
    background: rgba(128,128,128,0.05);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "dataset/indian_stock_market.csv",
        sep=";"
    )

    return df


df = load_data()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🇮🇳 Indian Stock Market Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Exploratory Data Analysis & Composite Performance Ranking '
    'of Indian Stock Market Companies'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Pilih Analisis",
    [
        "📋 Overview",
        "💰 Market Cap",
        "📊 P/E Ratio",
        "📈 Sales Growth",
        "💹 Profit Growth",
        "⚙️ ROCE",
        "🔄 Sales vs Profit",
        "🔗 Correlation",
        "🏆 Composite Ranking",
        "🔎 Key Findings",
        "📝 Conclusion",
        "⚠️ Limitations"
    ]
)

st.sidebar.divider()

st.sidebar.subheader("📌 About")

st.sidebar.caption(
    "Exploratory Data Analysis and "
    "Composite Performance Ranking "
    "of Indian Stock Market Companies."
)

st.sidebar.caption(
    f"Dataset: {len(df):,} companies"
)

st.sidebar.caption(
    "Analysis Date: 2026-06-26"
)


# =========================================================
# OVERVIEW
# =========================================================

if page == "📋 Overview":

    st.header("📋 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Jumlah Perusahaan",
            f"{len(df):,}"
        )

    with col2:
        st.metric(
            "Jumlah Kolom",
            f"{df.shape[1]}"
        )

    with col3:
        st.metric(
            "Tanggal Data",
            str(df["Collection_Date"].iloc[0])
        )

    with col4:
        st.metric(
            "Duplicate Rows",
            f"{df.duplicated().sum()}"
        )
    
    st.divider()
    st.subheader("📌 Project Objective")

    st.markdown("""
    Project ini bertujuan untuk menganalisis karakteristik perusahaan
    di Indian Stock Market berdasarkan:

    - **Market Capitalization**
    - **P/E Ratio**
    - **Quarterly Sales Growth**
    - **Quarterly Profit Growth**
    - **ROCE**

    Selain exploratory analysis, project ini menggunakan **Composite Score**
    untuk membuat ranking performa perusahaan berdasarkan beberapa indikator
    fundamental.
    """)

    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(10),
        width="stretch",
        hide_index=True
    )

    st.subheader("Missing Values")

    missing_data = df.isnull().sum()

    missing_df = pd.DataFrame({
        "Column": missing_data.index,
        "Missing Values": missing_data.values
    })

    st.dataframe(
        missing_df,
        width="stretch",
        hide_index=True
    )


# =========================================================
# MARKET CAP
# =========================================================

elif page == "💰 Market Cap":

    st.header("💰 Market Capitalization Analysis")

    market_cap_95 = df[
        "Market_Cap_Crore"
    ].quantile(0.95)

    st.metric(
        "Market Cap 95th Percentile",
        f"{market_cap_95:,.2f}"
    )

    st.subheader("Market Cap Distribution")

    market_cap_filtered = df[
        df["Market_Cap_Crore"] <= market_cap_95
    ]["Market_Cap_Crore"].dropna()

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        market_cap_filtered,
        bins=50
    )

    ax.set_xlabel("Market Cap (Crore)")
    ax.set_ylabel("Number of Companies")
    ax.set_title(
        "Market Cap Distribution (≤ 95th Percentile)"
    )

    st.pyplot(fig)

    plt.close(fig)

    st.subheader("🏆 Top 10 Companies by Market Cap")

    top_market_cap = (
        df[
            [
                "Company",
                "Market_Cap_Crore"
            ]
        ]
        .dropna()
        .sort_values(
            "Market_Cap_Crore",
            ascending=False
        )
        .head(10)
        .reset_index(drop=True)
    )

    top_market_cap.index += 1

    st.dataframe(
        top_market_cap,
        width="stretch"
    )


# =========================================================
# P/E
# =========================================================

elif page == "📊 P/E Ratio":

    st.header("📊 P/E Ratio Analysis")

    pe_95 = df[
        "PE_Ratio"
    ].quantile(0.95)

    st.metric(
        "P/E Ratio 95th Percentile",
        f"{pe_95:,.2f}"
    )

    st.subheader("P/E Ratio Distribution")

    pe_filtered = df[
        df["PE_Ratio"] <= pe_95
    ]["PE_Ratio"].dropna()

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        pe_filtered,
        bins=50
    )

    ax.set_xlabel("P/E Ratio")
    ax.set_ylabel("Number of Companies")
    ax.set_title(
        "P/E Ratio Distribution (≤ 95th Percentile)"
    )

    st.pyplot(fig)

    plt.close(fig)

    st.subheader("🏆 Top 10 Companies by P/E Ratio")

    top_pe = (
        df[
            [
                "Company",
                "PE_Ratio"
            ]
        ]
        .dropna()
        .sort_values(
            "PE_Ratio",
            ascending=False
        )
        .head(10)
        .reset_index(drop=True)
    )

    top_pe.index += 1

    st.dataframe(
        top_pe,
        width="stretch"
    )


# =========================================================
# SALES GROWTH
# =========================================================

elif page == "📈 Sales Growth":

    st.header("📈 Sales Growth Analysis")

    sales_95 = df[
        "Quarterly_Sales_Growth_Percent"
    ].quantile(0.95)

    st.metric(
        "Sales Growth 95th Percentile",
        f"{sales_95:,.2f}%"
    )

    st.subheader("Sales Growth Distribution")

    sales_filtered = df[
        df["Quarterly_Sales_Growth_Percent"] <= sales_95
    ]["Quarterly_Sales_Growth_Percent"].dropna()

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        sales_filtered,
        bins=50
    )

    ax.set_xlabel("Quarterly Sales Growth (%)")
    ax.set_ylabel("Number of Companies")
    ax.set_title(
        "Sales Growth Distribution (≤ 95th Percentile)"
    )

    st.pyplot(fig)

    plt.close(fig)

    st.subheader("🏆 Top 10 Companies by Sales Growth")

    top_sales = (
        df[
            [
                "Company",
                "Quarterly_Sales_Growth_Percent"
            ]
        ]
        .dropna()
        .sort_values(
            "Quarterly_Sales_Growth_Percent",
            ascending=False
        )
        .head(10)
        .reset_index(drop=True)
    )

    top_sales.index += 1

    st.dataframe(
        top_sales,
        width="stretch"
    )


# =========================================================
# PROFIT GROWTH
# =========================================================

elif page == "💹 Profit Growth":

    st.header("💹 Profit Growth Analysis")

    profit_95 = df[
        "Quarterly_Profit_Growth_Percent"
    ].quantile(0.95)

    st.metric(
        "Profit Growth 95th Percentile",
        f"{profit_95:,.2f}%"
    )

    st.subheader("Profit Growth Distribution")

    profit_filtered = df[
        df["Quarterly_Profit_Growth_Percent"] <= profit_95
    ]["Quarterly_Profit_Growth_Percent"].dropna()

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        profit_filtered,
        bins=50
    )

    ax.set_xlabel("Quarterly Profit Growth (%)")
    ax.set_ylabel("Number of Companies")
    ax.set_title(
        "Profit Growth Distribution (≤ 95th Percentile)"
    )

    st.pyplot(fig)

    plt.close(fig)

    st.subheader("🏆 Top 10 Companies by Profit Growth")

    top_profit = (
        df[
            [
                "Company",
                "Quarterly_Profit_Growth_Percent"
            ]
        ]
        .dropna()
        .sort_values(
            "Quarterly_Profit_Growth_Percent",
            ascending=False
        )
        .head(10)
        .reset_index(drop=True)
    )

    top_profit.index += 1

    st.dataframe(
        top_profit,
        width="stretch"
    )


# =========================================================
# ROCE
# =========================================================

elif page == "⚙️ ROCE":

    st.header("⚙️ ROCE Analysis")

    roce_95 = df[
        "ROCE_Percent"
    ].quantile(0.95)

    st.metric(
        "ROCE 95th Percentile",
        f"{roce_95:,.2f}%"
    )

    st.subheader("ROCE Distribution")

    roce_data = df[
        "ROCE_Percent"
    ].dropna()

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        roce_data,
        bins=50
    )

    ax.set_xlabel("ROCE (%)")
    ax.set_ylabel("Number of Companies")
    ax.set_title("ROCE Distribution")

    st.pyplot(fig)

    plt.close(fig)

    st.subheader("🏆 Top 10 Companies by ROCE")

    top_roce = (
        df[
            [
                "Company",
                "ROCE_Percent"
            ]
        ]
        .dropna()
        .sort_values(
            "ROCE_Percent",
            ascending=False
        )
        .head(10)
        .reset_index(drop=True)
    )

    top_roce.index += 1

    st.dataframe(
        top_roce,
        width="stretch"
    )


# =========================================================
# SALES VS PROFIT
# =========================================================

elif page == "🔄 Sales vs Profit":

    st.header("🔄 Sales Growth vs Profit Growth")

    growth_df = df[
        [
            "Company",
            "Quarterly_Sales_Growth_Percent",
            "Quarterly_Profit_Growth_Percent"
        ]
    ].dropna().copy()

    def classify_growth(row):

        sales = row[
            "Quarterly_Sales_Growth_Percent"
        ]

        profit = row[
            "Quarterly_Profit_Growth_Percent"
        ]

        if sales >= 0 and profit >= 0:
            return "Sales ↑ / Profit ↑"

        elif sales >= 0 and profit < 0:
            return "Sales ↑ / Profit ↓"

        elif sales < 0 and profit >= 0:
            return "Sales ↓ / Profit ↑"

        else:
            return "Sales ↓ / Profit ↓"

    growth_df["Growth_Category"] = growth_df.apply(
        classify_growth,
        axis=1
    )

    st.subheader("Growth Category")

    category_count = (
        growth_df["Growth_Category"]
        .value_counts()
    )

    category_percentage = (
        growth_df["Growth_Category"]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
    )

    category_df = pd.DataFrame({
        "Number of Companies": category_count,
        "Percentage (%)": category_percentage
    })

    st.dataframe(
        category_df,
        width="stretch"
    )

    st.subheader("Sales Growth vs Profit Growth")

    sales_limit = growth_df[
        "Quarterly_Sales_Growth_Percent"
    ].quantile(0.95)

    profit_limit = growth_df[
        "Quarterly_Profit_Growth_Percent"
    ].quantile(0.95)

    growth_plot = growth_df[
        (
            growth_df[
                "Quarterly_Sales_Growth_Percent"
            ] <= sales_limit
        )
        &
        (
            growth_df[
                "Quarterly_Profit_Growth_Percent"
            ] <= profit_limit
        )
    ]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        growth_plot[
            "Quarterly_Sales_Growth_Percent"
        ],
        growth_plot[
            "Quarterly_Profit_Growth_Percent"
        ],
        alpha=0.5
    )

    ax.axhline(
        0,
        linestyle="--"
    )

    ax.axvline(
        0,
        linestyle="--"
    )

    ax.set_xlabel(
        "Quarterly Sales Growth (%)"
    )

    ax.set_ylabel(
        "Quarterly Profit Growth (%)"
    )

    ax.set_title(
        "Sales Growth vs Profit Growth"
    )

    st.pyplot(fig)

    plt.close(fig)

    pearson_corr = growth_df[
        "Quarterly_Sales_Growth_Percent"
    ].corr(
        growth_df[
            "Quarterly_Profit_Growth_Percent"
        ],
        method="pearson"
    )

    spearman_corr = growth_df[
        "Quarterly_Sales_Growth_Percent"
    ].corr(
        growth_df[
            "Quarterly_Profit_Growth_Percent"
        ],
        method="spearman"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Pearson Correlation",
            f"{pearson_corr:.3f}"
        )

    with col2:
        st.metric(
            "Spearman Correlation",
            f"{spearman_corr:.3f}"
        )


# =========================================================
# CORRELATION
# =========================================================

elif page == "🔗 Correlation":

    st.header("🔗 Correlation Analysis")

    corr_columns = [
        "Market_Cap_Crore",
        "PE_Ratio",
        "Quarterly_Sales_Growth_Percent",
        "Quarterly_Profit_Growth_Percent",
        "ROCE_Percent"
    ]

    corr_df = df[
        corr_columns
    ].corr()

    st.subheader("Correlation Matrix")

    st.dataframe(
        corr_df.round(3),
        width="stretch"
    )

    st.subheader("ROCE vs P/E")

    roce_pe_df = df[
        [
            "ROCE_Percent",
            "PE_Ratio"
        ]
    ].dropna()

    pearson_roce_pe = roce_pe_df[
        "ROCE_Percent"
    ].corr(
        roce_pe_df["PE_Ratio"],
        method="pearson"
    )

    spearman_roce_pe = roce_pe_df[
        "ROCE_Percent"
    ].corr(
        roce_pe_df["PE_Ratio"],
        method="spearman"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Pearson",
            f"{pearson_roce_pe:.3f}"
        )

    with col2:
        st.metric(
            "Spearman",
            f"{spearman_roce_pe:.3f}"
        )


# =========================================================
# COMPOSITE RANKING
# =========================================================

elif page == "🏆 Composite Ranking":

    st.header("🏆 Composite Performance Ranking")

    st.markdown("""
    Composite Score menggabungkan empat indikator performa perusahaan
    menggunakan percentile ranking.

    **Bobot indikator:**

    - Market Cap → 20%
    - Sales Growth → 20%
    - Profit Growth → 30%
    - ROCE → 30%

    Semakin tinggi Composite Score, semakin tinggi posisi perusahaan
    dalam ranking.
    """)

    ranking_df = df[
        [
            "Company",
            "Market_Cap_Crore",
            "Quarterly_Sales_Growth_Percent",
            "Quarterly_Profit_Growth_Percent",
            "ROCE_Percent"
        ]
    ].dropna().copy()

    st.write(
        f"Perusahaan yang dapat dinilai: "
        f"**{len(ranking_df):,}**"
    )

    # Percentile Ranking
    ranking_df["Market_Cap_Score"] = (
        ranking_df[
            "Market_Cap_Crore"
        ].rank(pct=True) * 100
    )

    ranking_df["Sales_Growth_Score"] = (
        ranking_df[
            "Quarterly_Sales_Growth_Percent"
        ].rank(pct=True) * 100
    )

    ranking_df["Profit_Growth_Score"] = (
        ranking_df[
            "Quarterly_Profit_Growth_Percent"
        ].rank(pct=True) * 100
    )

    ranking_df["ROCE_Score"] = (
        ranking_df[
            "ROCE_Percent"
        ].rank(pct=True) * 100
    )

    # Composite Score
    ranking_df["Composite_Score"] = (
        ranking_df["Market_Cap_Score"] * 0.20
        + ranking_df["Sales_Growth_Score"] * 0.20
        + ranking_df["Profit_Growth_Score"] * 0.30
        + ranking_df["ROCE_Score"] * 0.30
    )

    # Ranking
    ranking = (
        ranking_df
        .sort_values(
            "Composite_Score",
            ascending=False
        )
        .reset_index(drop=True)
    )

    ranking["Rank"] = (
        ranking.index + 1
    )

    top_10 = ranking.head(10)

    result = top_10[
        [
            "Rank",
            "Company",
            "Market_Cap_Crore",
            "Quarterly_Sales_Growth_Percent",
            "Quarterly_Profit_Growth_Percent",
            "ROCE_Percent",
            "Composite_Score"
        ]
    ].copy()

    st.subheader(
        "🥇 Top 10 Companies by Composite Score"
    )

    st.dataframe(
        result,
        width="stretch",
        hide_index=True
    )

    st.subheader(
        "Composite Score Components"
    )

    score_components = top_10[
        [
            "Company",
            "Market_Cap_Score",
            "Sales_Growth_Score",
            "Profit_Growth_Score",
            "ROCE_Score",
            "Composite_Score"
        ]
    ].copy()

    st.dataframe(
        score_components,
        width="stretch",
        hide_index=True
    )
    

    st.subheader("📊 Composite Score – Top 10")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.barh(
        result["Company"][::-1],
        result["Composite_Score"][::-1]
)

    ax.set_xlabel("Composite Score")
    ax.set_ylabel("Company")
    ax.set_title("Top 10 Companies by Composite Score")

    st.pyplot(fig)

    plt.close(fig)

    csv = result.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Top 10 Composite Ranking",
        data=csv,
        file_name="top_10_composite_ranking.csv",
        mime="text/csv"
    )


# =========================================================
# KEY FINDINGS
# =========================================================

elif page == "🔎 Key Findings":

    st.header("🔎 Key Findings")

    st.markdown("""
    ### 1. Market Capitalization

    Market Capitalization menunjukkan dominasi beberapa perusahaan besar
    seperti Reliance Industries, HDFC Bank, Bharti Airtel, ICICI Bank,
    dan SBI.
    """)

    st.markdown("""
    ### 2. Sales Growth

    Beberapa perusahaan memiliki pertumbuhan penjualan yang sangat tinggi.
    Distribusi Sales Growth bersifat sangat skewed karena terdapat
    extreme values.
    """)

    st.markdown("""
    ### 3. Profit Growth

    Profit Growth juga memiliki distribusi yang sangat ekstrem.
    95th percentile berada pada **600%**, sementara beberapa observasi
    memiliki nilai yang jauh lebih tinggi.
    """)

    st.markdown("""
    ### 4. Sales Growth vs Profit Growth

    Pertumbuhan penjualan tidak selalu diikuti oleh pertumbuhan laba
    secara sebanding. Hubungan linear keduanya sangat lemah berdasarkan
    Pearson Correlation.
    """)

    st.markdown("""
    ### 5. Composite Performance

    Composite Score menggunakan Market Cap 20%, Sales Growth 20%,
    Profit Growth 30%, dan ROCE 30%.

    Berdasarkan metode percentile ranking, **SPARC** berada pada
    peringkat pertama, diikuti **Sigma Advanced System** dan
    **Lloyds Metals**.
    """)

    st.markdown("""
    ### 6. ROCE vs P/E

    ROCE dan P/E menunjukkan hubungan negatif dalam dataset.
    """)


# =========================================================
# CONCLUSION
# =========================================================

elif page == "📝 Conclusion":

    st.header("📝 Conclusion")

    st.markdown("""
    Berdasarkan hasil exploratory analysis terhadap Indian Stock Market
    Dataset, terdapat perbedaan karakteristik yang cukup besar antar
    perusahaan dalam hal Market Capitalization, P/E Ratio, Sales Growth,
    Profit Growth, dan ROCE.

    Market Capitalization menunjukkan dominasi beberapa perusahaan besar,
    sementara indikator pertumbuhan Sales dan Profit memiliki distribusi
    yang sangat ekstrem.

    Analisis Sales Growth dan Profit Growth menunjukkan bahwa pertumbuhan
    penjualan tidak selalu diikuti oleh pertumbuhan laba secara linear.

    Composite Score digunakan untuk memberikan penilaian performa
    berdasarkan kombinasi Market Cap, Sales Growth, Profit Growth,
    dan ROCE.

    Berdasarkan hasil ranking, SPARC berada pada peringkat pertama,
    diikuti Sigma Advanced System dan Lloyds Metals.
    """)


# =========================================================
# LIMITATIONS
# =========================================================

elif page == "⚠️ Limitations":

    st.header("⚠️ Limitations")

    st.markdown("""
    - Dataset hanya merepresentasikan kondisi pada tanggal pengumpulan
      data dan tidak menggambarkan perubahan harga atau fundamental
      secara time-series.

    - Beberapa variabel memiliki missing values sehingga analisis tertentu
      menggunakan data yang tersedia setelah proses `dropna()`.

    - Sales Growth dan Profit Growth memiliki extreme values yang sangat
      tinggi sehingga distribusinya sangat skewed.

    - Penggunaan 95th percentile pada beberapa visualisasi hanya bertujuan
      meningkatkan keterbacaan grafik dan tidak menghapus nilai asli
      dari dataset.

    - Composite Score merkan metode ranking berdasarkan indikator
      yang tersedia dalam dataset dan bukan merupakan rekomendasi
      untuk membeli atau menjual saham.
    """)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Indian Stock Market Analysis • Exploratory Data Analysis "
    "and Composite Performance Ranking "
    "By @LatifMauruf"
)