import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Bike Rental Analytics",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Css kustom untuk styling dashboard
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

# Muat data
DATA_PATH = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxSI7pMaN11YErTn8eN9pRMWho1-CdQGBqyk5M4IMbD8cTLGWSWBbjrnCGh-o4COcZJHerW6ATVvSA/pub?output=csv"

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

    sel_musim  = st.selectbox("🌤 Pilih Musim",
                              ["Semua"] + sorted(df["season_name"].unique().tolist()))
    sel_tahun  = st.multiselect("📅 Pilih Tahun",
                                sorted(df["year_label"].unique().tolist()),
                                default=sorted(df["year_label"].unique().tolist()))
    sel_cuaca  = st.multiselect("🌦 Kondisi Cuaca",
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

# Filter data sesuai pilihan sidebar
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
    (c1, f"{total:,}",      "Total Peminjaman",   f"↑ {rasio}% terdaftar",                                    "#06D6A0"),
    (c2, f"{kasual:,}",     "Pengguna Kasual",    f"{round(kasual/total*100,1) if total else 0}% dari total",  "#FFB347"),
    (c3, f"{terdaftar:,}",  "Pengguna Terdaftar", f"{rasio}% dari total",                                      "#118AB2"),
    (c4, f"{rata_hr:,.0f}", "Rata-rata/Hari",     f"{len(dff['dteday'].unique())} hari data",                  "#EF476F"),
]:
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color:{color};">
          <div class="kpi-value" style="color:{color};">{val}</div>
          <div class="kpi-label">{label}</div>
          <div class="kpi-delta" style="color:{color};">{delta}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Palet warna
C = {
    "kasual":    "#FFB347",
    "terdaftar": "#118AB2",
    "teal":      "#06D6A0",
    "navy":      "#0F4C75",
    "red":       "#EF476F",
    "grid":      "#D1D5DB",
}
BASE_LAYOUT = dict(
    plot_bgcolor="white", paper_bgcolor="white",
    font=dict(family="DM Sans", color="#000000"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
    margin=dict(t=50, b=40, l=55, r=30),
)
SEASON_ORDER  = ["Spring", "Summer", "Fall", "Winter"]
WEATHER_ORDER = ["Cerah", "Kabut/Mendung", "Hujan/Salju Ringan", "Hujan/Salju Lebat"]

# TABS
tab1, tab2 = st.tabs(["🌿 Penyewaan per Musim", "🌦 Penyewaan per Cuaca"])

# TAB 1 · Penyewaan per Musim
with tab1:
    st.markdown('<div class="section-title">Total Penyewaan Sepeda per Musim</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Perbandingan pengguna kasual vs terdaftar per musim beserta pertumbuhan antar musim</div>', unsafe_allow_html=True)

    # Agregasi: sum per hari → sum total (hindari double-count per jam)
    day_agg = dff.groupby(["dteday", "season_name"], as_index=False)[["casual", "registered", "cnt"]].sum()
    s_agg   = day_agg.groupby("season_name", as_index=False)[["casual", "registered", "cnt"]].sum()
    s_agg["season_name"] = pd.Categorical(s_agg["season_name"], categories=SEASON_ORDER, ordered=True)
    s_agg = s_agg.sort_values("season_name").reset_index(drop=True)
    s_agg["pct_change"] = s_agg["cnt"].pct_change() * 100

    max_cas_season = s_agg.loc[s_agg["casual"].idxmax(),     "season_name"]
    max_reg_season = s_agg.loc[s_agg["registered"].idxmax(), "season_name"]

    clr_k = [C["navy"] if s == max_cas_season else C["kasual"]    for s in s_agg["season_name"]]
    clr_r = [C["teal"] if s == max_reg_season else C["terdaftar"] for s in s_agg["season_name"]]

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        name="Kasual", x=s_agg["season_name"], y=s_agg["casual"],
        marker=dict(color=clr_k, line=dict(color="#333", width=1)),
        text=s_agg["casual"].apply(lambda v: f"{v:,.0f}"),
        textposition="inside", textfont=dict(size=11, color="black"),
    ))
    fig1.add_trace(go.Bar(
        name="Terdaftar", x=s_agg["season_name"], y=s_agg["registered"],
        marker=dict(color=clr_r, line=dict(color="#333", width=1)),
        text=s_agg["registered"].apply(lambda v: f"{v:,.0f}"),
        textposition="inside", textfont=dict(size=11, color="black"),
    ))

    annots = []
    for _, row in s_agg.iterrows():
        if not np.isnan(row["pct_change"]):
            clr_lbl   = C["red"] if row["pct_change"] < 0 else "#16A34A"
            arrow_chr = "↑" if row["pct_change"] >= 0 else "↓"
            annots.append(dict(
                x=row["season_name"],
                y=max(row["casual"], row["registered"]) + s_agg["cnt"].max() * 0.03,
                text=f"{arrow_chr} {abs(row['pct_change']):.1f}%",
                showarrow=False,
                font=dict(color=clr_lbl, size=13, family="Space Mono"),
                xanchor="center",
            ))

    fig1.update_layout(
        **BASE_LAYOUT, barmode="group", height=460, annotations=annots,
        title=dict(text="Total Penyewaan Sepeda per Musim dengan Pertumbuhan Musiman", font_size=14),
        xaxis=dict(title="Musim",          showgrid=False, linecolor="#9CA3AF"),
        yaxis=dict(title="Total Penyewaan", gridcolor=C["grid"], linecolor="#9CA3AF"),
    )
    st.plotly_chart(fig1, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-title" style="font-size:0.9rem;">Proporsi Kasual vs Terdaftar per Musim</div>', unsafe_allow_html=True)
        fig1b = go.Figure()
        for name, clr in [("casual", C["kasual"]), ("registered", C["terdaftar"])]:
            fig1b.add_trace(go.Bar(
                name=name.capitalize(),
                x=s_agg["season_name"],
                y=s_agg[name] / s_agg["cnt"] * 100,
                marker_color=clr,
            ))
        fig1b.update_layout(**BASE_LAYOUT, barmode="stack", height=300,
                             yaxis=dict(title="%", gridcolor=C["grid"]),
                             xaxis=dict(showgrid=False))
        st.plotly_chart(fig1b, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title" style="font-size:0.9rem;">Kontribusi per Musim</div>', unsafe_allow_html=True)
        fig1c = go.Figure(go.Pie(
            labels=s_agg["season_name"], values=s_agg["cnt"],
            marker_colors=["#A8D8EA", "#118AB2", "#06D6A0", "#0F4C75"],
            hole=0.5, textinfo="label+percent",
        ))
        fig1c.update_layout(paper_bgcolor="white", height=300,
                             margin=dict(t=20, b=20, l=20, r=20),
                             font=dict(family="DM Sans", color="black"))
        st.plotly_chart(fig1c, use_container_width=True)



# TAB 2 · Penyewaan per Cuaca 
with tab2:
    st.markdown('<div class="section-title">Rata-rata Penyewaan Berdasarkan Kondisi Cuaca</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Perbandingan rata-rata harian antara tahun 2011 dan 2012 per kondisi cuaca</div>', unsafe_allow_html=True)

    weather_labels = {1:"Cerah", 2:"Kabut/Mendung", 3:"Hujan/Salju Ringan", 4:"Hujan/Salju Lebat"}

    day_w   = dff.groupby(["dteday", "weathersit", "year_label"], as_index=False)["cnt"].sum()
    w_agg   = day_w.groupby(["weathersit", "year_label"], as_index=False)["cnt"].mean()
    w_agg["weather_name"] = w_agg["weathersit"].map(weather_labels)
    w_agg["weather_name"] = pd.Categorical(w_agg["weather_name"], categories=WEATHER_ORDER, ordered=True)
    w_agg   = w_agg.sort_values("weather_name")

    yr_colors = {"2011": "#440154", "2012": "#35B779"}

    fig2 = go.Figure()
    for yr in ["2011", "2012"]:
        sub = w_agg[w_agg["year_label"] == yr]
        fig2.add_trace(go.Bar(
            name=yr, x=sub["weather_name"], y=sub["cnt"],
            marker=dict(color=yr_colors[yr], line=dict(color="#333", width=0.8)),
            text=sub["cnt"].apply(lambda v: f"{v:,.0f}"),
            textposition="outside", textfont=dict(size=10, color="black"),
        ))

    fig2.update_layout(
        **BASE_LAYOUT, barmode="group", height=460,
        title=dict(
            text="Rata-rata Penyewaan Sepeda Harian berdasarkan Kondisi Cuaca (2011 vs 2012)",
            font_size=14,
        ),
        xaxis=dict(title="Kondisi Cuaca",                   showgrid=False, linecolor="#9CA3AF", tickangle=-15),
        yaxis=dict(title="Rata-rata Jumlah Penyewaan Harian", gridcolor=C["grid"], linecolor="#9CA3AF"),
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-title" style="font-size:0.9rem; margin-top:4px;">Peta Panas: Cuaca × Musim</div>', unsafe_allow_html=True)
    heat_df = dff.groupby(["weather_name", "season_name"])["cnt"].mean().unstack(fill_value=0)
    heat_df = heat_df.reindex(
        index  =[w for w in WEATHER_ORDER if w in heat_df.index],
        columns=[s for s in SEASON_ORDER  if s in heat_df.columns],
    )
    fig2b = go.Figure(go.Heatmap(
        z=heat_df.values,
        x=heat_df.columns.tolist(),
        y=heat_df.index.tolist(),
        colorscale=[[0, "#EAF6FB"], [0.5, "#118AB2"], [1, "#0F4C75"]],
        text=np.round(heat_df.values, 0),
        texttemplate="%{text:,.0f}",
        textfont=dict(size=11, color="black"),
    ))
    fig2b.update_layout(paper_bgcolor="white", plot_bgcolor="white", height=260,
                         margin=dict(t=20, b=40, l=160, r=20),
                         font=dict(family="DM Sans"))
    st.plotly_chart(fig2b, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;font-size:0.78rem;color:#9CA3AF;padding:12px 0;'>
  © 2026 Bintang Qaulan Tsaqiila | Proyek Akhir Analisis Data
</div>
""", unsafe_allow_html=True)