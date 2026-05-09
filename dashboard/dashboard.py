import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import seaborn as sns

# Page Config
st.set_page_config(
    page_title="Bike Rental Analytics",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #F0F4F8; }
.stApp { background-color: #F0F4F8; }
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0F4C75 0%, #1B6CA8 60%, #118AB2 100%);
}
[data-testid="stSidebar"] * { color: #E8F4FD !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #A8D8EA !important; font-weight: 500;
    font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase;
}
[data-testid="stSidebar"] [data-baseweb="select"] {
    background-color: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.25) !important; border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #06D6A0 !important; color: #0F4C75 !important; font-weight: 600;
}
.dash-header {
    background: linear-gradient(135deg, #0F4C75 0%, #118AB2 100%);
    border-radius: 16px; padding: 28px 36px; margin-bottom: 28px;
    display: flex; align-items: center; gap: 18px;
    box-shadow: 0 8px 32px rgba(15,76,117,0.18);
}
.dash-header h1 { font-family:'Space Mono',monospace; font-size:1.85rem; font-weight:700; color:#FFFFFF; margin:0; }
.dash-header p  { color:#A8D8EA; font-size:0.9rem; margin:4px 0 0 0; }
.kpi-card {
    background:#FFFFFF; border-radius:14px; padding:22px 24px;
    box-shadow:0 2px 16px rgba(0,0,0,0.07); border-top:4px solid;
}
.kpi-value { font-family:'Space Mono',monospace; font-size:2rem; font-weight:700; line-height:1; margin-bottom:4px; }
.kpi-label { font-size:0.78rem; letter-spacing:0.06em; text-transform:uppercase; color:#6B7280; font-weight:500; }
.kpi-delta { font-size:0.82rem; font-weight:600; margin-top:6px; }
.stTabs [data-baseweb="tab-list"] { gap:8px; background:transparent; padding:0; }
.stTabs [data-baseweb="tab"] {
    background:#FFFFFF; border-radius:10px; padding:8px 20px;
    font-weight:500; font-size:0.88rem; color:#6B7280; border:1px solid #E5E7EB;
}
.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#0F4C75,#118AB2) !important;
    color:#FFFFFF !important; border-color:transparent !important;
}
.section-title { font-family:'Space Mono',monospace; font-size:1.05rem; font-weight:700; color:#0F4C75; margin-bottom:2px; }
.section-sub   { font-size:0.82rem; color:#9CA3AF; margin-bottom:16px; }
</style>
""", unsafe_allow_html=True)

# Matplotlib global style
plt.rcParams.update({
    "figure.facecolor":  "white",
    "axes.facecolor":    "#FAFAFA",
    "axes.edgecolor":    "#9CA3AF",
    "axes.labelcolor":   "#374151",
    "axes.titlecolor":   "#0F4C75",
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
    "axes.labelsize":    11,
    "xtick.color":       "#374151",
    "ytick.color":       "#374151",
    "xtick.labelsize":   10,
    "ytick.labelsize":   10,
    "legend.framealpha": 1,
    "legend.edgecolor":  "#D1D5DB",
    "legend.fontsize":   10,
    "grid.color":        "#E5E7EB",
    "grid.linewidth":    0.8,
    "text.color":        "#1F2937",
    "font.family":       "DejaVu Sans",
})

# Palet warna
C_KASUAL    = "#FFB347"
C_TERDAFTAR = "#118AB2"
C_NAVY      = "#0F4C75"
C_TEAL      = "#06D6A0"
C_RED       = "#EF476F"
C_GREEN     = "#16A34A"
C_2011      = "#440154"
C_2012      = "#35B779"

SEASON_ORDER  = ["Spring", "Summer", "Fall", "Winter"]
WEATHER_ORDER = ["Cerah", "Kabut/Mendung", "Hujan/Salju Ringan", "Hujan/Salju Lebat"]

# Load Data
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "hour.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["dteday"] = pd.to_datetime(df["dteday"])
    df["season_name"]  = df["season"].map({1:"Spring", 2:"Summer", 3:"Fall", 4:"Winter"})
    df["weather_name"] = df["weathersit"].map({
        1:"Cerah", 2:"Kabut/Mendung", 3:"Hujan/Salju Ringan", 4:"Hujan/Salju Lebat"
    })
    df["year_label"] = df["yr"].map({0:"2011", 1:"2012"})
    return df

df = load_data()

# Sidebar
with st.sidebar:
    st.markdown("## 🚲 Filter Data")
    st.markdown("---")
    sel_musim = st.selectbox("🌤 Pilih Musim",
                             ["Semua"] + sorted(df["season_name"].unique().tolist()))
    sel_tahun = st.multiselect("📅 Pilih Tahun",
                               sorted(df["year_label"].unique().tolist()),
                               default=sorted(df["year_label"].unique().tolist()))
    sel_cuaca = st.multiselect("🌦 Kondisi Cuaca",
                               sorted(df["weather_name"].unique().tolist()),
                               default=sorted(df["weather_name"].unique().tolist()))
    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem;color:#A8D8EA;line-height:1.7;'>
    <b style='color:#06D6A0;'>Dataset:</b> Capital Bikeshare<br>
    <b style='color:#06D6A0;'>File:</b> data/hour.csv<br>
    <b style='color:#06D6A0;'>Periode:</b> 2011 – 2012<br>
    <b style='color:#06D6A0;'>Records:</b> 17,379 jam
    </div>
    """, unsafe_allow_html=True)

# Filter
dff = df.copy()
if sel_musim != "Semua":
    dff = dff[dff["season_name"] == sel_musim]
if sel_tahun:
    dff = dff[dff["year_label"].isin(sel_tahun)]
if sel_cuaca:
    dff = dff[dff["weather_name"].isin(sel_cuaca)]

# Header
st.markdown("""
<div class="dash-header">
  <div style="font-size:2.8rem;">🚲</div>
  <div>
    <h1>Bike Rental Analytics</h1>
    <p>Eksplorasi pola peminjaman sepeda berdasarkan musim dan kondisi cuaca · Dataset: hour.csv</p>
  </div>
</div>
""", unsafe_allow_html=True)

# KPI Cards
total     = int(dff["cnt"].sum())
kasual    = int(dff["casual"].sum())
terdaftar = int(dff["registered"].sum())
rasio     = round(terdaftar / total * 100, 1) if total > 0 else 0
rata_hr   = round(dff.groupby("dteday")["cnt"].sum().mean(), 0)

c1, c2, c3, c4 = st.columns(4)
for col, val, label, delta, color in [
    (c1, f"{total:,}",      "Total Peminjaman",   f"↑ {rasio}% terdaftar",                                   "#06D6A0"),
    (c2, f"{kasual:,}",     "Pengguna Kasual",    f"{round(kasual/total*100,1) if total else 0}% dari total", "#FFB347"),
    (c3, f"{terdaftar:,}",  "Pengguna Terdaftar", f"{rasio}% dari total",                                     "#118AB2"),
    (c4, f"{rata_hr:,.0f}", "Rata-rata/Hari",     f"{len(dff['dteday'].unique())} hari data",                 "#EF476F"),
]:
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color:{color};">
          <div class="kpi-value" style="color:{color};">{val}</div>
          <div class="kpi-label">{label}</div>
          <div class="kpi-delta" style="color:{color};">{delta}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# TABS
tab1, tab2 = st.tabs(["🌿 Penyewaan per Musim", "🌦 Penyewaan per Cuaca"])

# TAB 1 · Penyewaan per Musim
with tab1:
    st.markdown('<div class="section-title">Total Penyewaan Sepeda per Musim</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Perbandingan pengguna kasual vs terdaftar per musim beserta pertumbuhan antar musim</div>', unsafe_allow_html=True)

    # Agregasi
    day_agg = dff.groupby(["dteday", "season_name"], as_index=False)[["casual", "registered", "cnt"]].sum()
    s_agg   = day_agg.groupby("season_name", as_index=False)[["casual", "registered", "cnt"]].sum()
    s_agg["season_name"] = pd.Categorical(s_agg["season_name"], categories=SEASON_ORDER, ordered=True)
    s_agg = s_agg.sort_values("season_name").reset_index(drop=True)
    s_agg["pct_change"] = s_agg["cnt"].pct_change() * 100

    max_cas_season = s_agg.loc[s_agg["casual"].idxmax(),     "season_name"]
    max_reg_season = s_agg.loc[s_agg["registered"].idxmax(), "season_name"]

    seasons   = s_agg["season_name"].astype(str).tolist()
    x         = np.arange(len(seasons))
    bar_w     = 0.35

    # Grafik utama: grouped bar
    fig1, ax1 = plt.subplots(figsize=(10, 6))

    clr_k = [C_NAVY if s == max_cas_season else C_KASUAL    for s in seasons]
    clr_r = [C_TEAL if s == max_reg_season else C_TERDAFTAR for s in seasons]

    bars_k = ax1.bar(x - bar_w/2, s_agg["casual"],     bar_w, color=clr_k,
                     edgecolor="#333333", linewidth=0.8, label="Kasual")
    bars_r = ax1.bar(x + bar_w/2, s_agg["registered"], bar_w, color=clr_r,
                     edgecolor="#333333", linewidth=0.8, label="Terdaftar")

    # Label angka di dalam bar
    for bar in bars_k:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h * 0.5,
                 f"{h:,.0f}", ha="center", va="center",
                 color="white", fontsize=9, fontweight="bold")
    for bar in bars_r:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h * 0.5,
                 f"{h:,.0f}", ha="center", va="center",
                 color="white", fontsize=9, fontweight="bold")

    # Label % perubahan di atas kelompok
    for i, row in s_agg.iterrows():
        if not np.isnan(row["pct_change"]):
            max_val   = max(row["casual"], row["registered"])
            offset    = s_agg["cnt"].max() * 0.03
            clr_lbl   = C_RED if row["pct_change"] < 0 else C_GREEN
            arrow_chr = "↑" if row["pct_change"] >= 0 else "↓"
            ax1.text(i, max_val + offset,
                     f"{arrow_chr} {abs(row['pct_change']):.1f}%",
                     ha="center", va="bottom",
                     color=clr_lbl, fontsize=11, fontweight="bold")

    ax1.set_title("Total Penyewaan Sepeda per Musim dengan Pertumbuhan Musiman", pad=14)
    ax1.set_xlabel("Musim")
    ax1.set_ylabel("Total Penyewaan")
    ax1.set_xticks(x)
    ax1.set_xticklabels(seasons)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax1.grid(axis="y", linestyle="--", alpha=0.6)
    ax1.set_axisbelow(True)

    # Legend dengan patch warna terang + gelap
    legend_patches = [
        mpatches.Patch(color=C_KASUAL,    label="Kasual"),
        mpatches.Patch(color=C_NAVY,      label="Kasual (tertinggi)"),
        mpatches.Patch(color=C_TERDAFTAR, label="Terdaftar"),
        mpatches.Patch(color=C_TEAL,      label="Terdaftar (tertinggi)"),
    ]
    ax1.legend(handles=legend_patches, loc="upper left", ncol=2, framealpha=1)
    plt.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

    # Baris bawah: proporsi stacked + pie
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-title" style="font-size:0.9rem;">Proporsi Kasual vs Terdaftar per Musim</div>', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        pct_k = s_agg["casual"]     / s_agg["cnt"] * 100
        pct_r = s_agg["registered"] / s_agg["cnt"] * 100
        ax2.bar(seasons, pct_k, color=C_KASUAL,    edgecolor="#333", linewidth=0.7, label="Kasual")
        ax2.bar(seasons, pct_r, bottom=pct_k, color=C_TERDAFTAR, edgecolor="#333", linewidth=0.7, label="Terdaftar")
        ax2.set_ylabel("%")
        ax2.set_ylim(0, 110)
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
        ax2.grid(axis="y", linestyle="--", alpha=0.5)
        ax2.set_axisbelow(True)
        ax2.legend(loc="upper right")
        ax2.set_title("Proporsi per Musim")
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    with col_b:
        st.markdown('<div class="section-title" style="font-size:0.9rem;">Kontribusi per Musim</div>', unsafe_allow_html=True)
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        pie_colors = ["#A8D8EA", "#118AB2", "#06D6A0", "#0F4C75"]
        wedges, texts, autotexts = ax3.pie(
            s_agg["cnt"],
            labels=seasons,
            colors=pie_colors[:len(seasons)],
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops=dict(edgecolor="white", linewidth=1.5),
            pctdistance=0.75,
        )
        for t in texts:
            t.set_color("#1F2937")
            t.set_fontsize(10)
        for at in autotexts:
            at.set_color("white")
            at.set_fontsize(9)
            at.set_fontweight("bold")
        # Donut hole
        centre_circle = plt.Circle((0, 0), 0.50, fc="white")
        ax3.add_artist(centre_circle)
        ax3.set_title("Kontribusi per Musim")
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)


# TAB 2 · Penyewaan per Cuaca
with tab2:
    st.markdown('<div class="section-title">Rata-rata Penyewaan Berdasarkan Kondisi Cuaca</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Perbandingan rata-rata harian antara tahun 2011 dan 2012 per kondisi cuaca</div>', unsafe_allow_html=True)

    weather_labels = {1:"Cerah", 2:"Kabut/Mendung", 3:"Hujan/Salju Ringan", 4:"Hujan/Salju Lebat"}

    day_w = dff.groupby(["dteday", "weathersit", "year_label"], as_index=False)["cnt"].sum()
    w_agg = day_w.groupby(["weathersit", "year_label"], as_index=False)["cnt"].mean()
    w_agg["weather_name"] = w_agg["weathersit"].map(weather_labels)
    w_agg["weather_name"] = pd.Categorical(w_agg["weather_name"], categories=WEATHER_ORDER, ordered=True)
    w_agg = w_agg.sort_values("weather_name")

    # Grafik utama: grouped bar per cuaca
    fig4, ax4 = plt.subplots(figsize=(10, 6))

    weather_present = [w for w in WEATHER_ORDER if w in w_agg["weather_name"].values]
    x_w   = np.arange(len(weather_present))
    bar_w = 0.35

    for i, (yr, color) in enumerate([("2011", C_2011), ("2012", C_2012)]):
        sub = w_agg[w_agg["year_label"] == yr].set_index("weather_name").reindex(weather_present)
        offset = (i - 0.5) * bar_w
        bars = ax4.bar(x_w + offset, sub["cnt"], bar_w,
                       color=color, edgecolor="#333333", linewidth=0.8, label=yr)
        for bar in bars:
            h = bar.get_height()
            if not np.isnan(h) and h > 0:
                ax4.text(bar.get_x() + bar.get_width()/2, h + 30,
                         f"{h:,.0f}", ha="center", va="bottom",
                         color="#1F2937", fontsize=9, fontweight="bold")

    ax4.set_title("Rata-rata Penyewaan Sepeda Harian berdasarkan Kondisi Cuaca (2011 vs 2012)", pad=14)
    ax4.set_xlabel("Kondisi Cuaca")
    ax4.set_ylabel("Rata-rata Jumlah Penyewaan Harian")
    ax4.set_xticks(x_w)
    ax4.set_xticklabels(weather_present, rotation=15, ha="right")
    ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax4.grid(axis="y", linestyle="--", alpha=0.6)
    ax4.set_axisbelow(True)
    ax4.legend(title="Tahun", loc="upper right")
    plt.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)

    # Heatmap cuaca × musim
    st.markdown('<div class="section-title" style="font-size:0.9rem; margin-top:8px;">Peta Panas: Cuaca × Musim</div>', unsafe_allow_html=True)

    heat_df = dff.groupby(["weather_name", "season_name"])["cnt"].mean().unstack(fill_value=0)
    heat_df = heat_df.reindex(
        index  =[w for w in WEATHER_ORDER if w in heat_df.index],
        columns=[s for s in SEASON_ORDER  if s in heat_df.columns],
    )

    fig5, ax5 = plt.subplots(figsize=(8, 3.5))
    sns.heatmap(
        heat_df,
        ax=ax5,
        cmap=sns.color_palette("Blues", as_cmap=True),
        annot=True,
        fmt=".0f",
        linewidths=0.5,
        linecolor="#E5E7EB",
        cbar_kws={"shrink": 0.8, "label": "Rata-rata cnt"},
        annot_kws={"size": 10, "color": "#1F2937", "weight": "bold"},
    )
    ax5.set_title("Rata-rata Peminjaman per Jam: Cuaca × Musim", pad=10)
    ax5.set_xlabel("Musim",       labelpad=8)
    ax5.set_ylabel("Kondisi Cuaca", labelpad=8)
    ax5.tick_params(axis="x", rotation=0)
    ax5.tick_params(axis="y", rotation=0)
    # Warna teks anotasi adaptif: putih di sel gelap
    for text in ax5.texts:
        val = float(text.get_text().replace(",", ""))
        text.set_color("white" if val > heat_df.values.max() * 0.6 else "#1F2937")
    plt.tight_layout()
    st.pyplot(fig5)
    plt.close(fig5)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center;font-size:0.78rem;color:#9CA3AF;padding:12px 0;'>
    © 2026 Bintang Qaulan Tsaqiila | Proyek Akhir Analisis Data
</div>
""", unsafe_allow_html=True)