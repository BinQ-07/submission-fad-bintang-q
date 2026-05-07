import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bike Rental Analytics",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #F0F4F8;
}

.stApp {
    background-color: #F0F4F8;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0F4C75 0%, #1B6CA8 60%, #118AB2 100%);
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: #E8F4FD !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #A8D8EA !important;
    font-weight: 500;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
[data-testid="stSidebar"] [data-baseweb="select"] {
    background-color: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #06D6A0 !important;
    color: #0F4C75 !important;
    font-weight: 600;
}

/* Header */
.dash-header {
    background: linear-gradient(135deg, #0F4C75 0%, #118AB2 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 18px;
    box-shadow: 0 8px 32px rgba(15,76,117,0.18);
}
.dash-header h1 {
    font-family: 'Space Mono', monospace;
    font-size: 1.85rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0;
    letter-spacing: -0.5px;
}
.dash-header p {
    color: #A8D8EA;
    font-size: 0.9rem;
    margin: 4px 0 0 0;
}

/* KPI cards */
.kpi-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 22px 24px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    border-top: 4px solid;
    transition: transform 0.2s;
}
.kpi-card:hover { transform: translateY(-3px); }
.kpi-value {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-label {
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #6B7280;
    font-weight: 500;
}
.kpi-delta {
    font-size: 0.82rem;
    font-weight: 600;
    margin-top: 6px;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    padding: 0;
}
.stTabs [data-baseweb="tab"] {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 8px 20px;
    font-weight: 500;
    font-size: 0.88rem;
    color: #6B7280;
    border: 1px solid #E5E7EB;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0F4C75, #118AB2) !important;
    color: #FFFFFF !important;
    border-color: transparent !important;
}

/* Section title */
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    color: #0F4C75;
    margin-bottom: 2px;
}
.section-sub {
    font-size: 0.82rem;
    color: #9CA3AF;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)


# ── Synthetic Data ────────────────────────────────────────────────────────────
np.random.seed(42)

months = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]

data_2011 = {
    "casual":    [5000, 5500, 15000, 22000, 35000, 40000, 42000, 45000, 38000, 28000, 12000, 6000],
    "registered":[40000,42000,65000,80000,110000,135000,150000,155000,140000,110000,70000,45000],
}
data_2012 = {
    "casual":    [6000, 7000, 18000, 28000, 42000, 50000, 55000, 58000, 50000, 35000, 15000, 7000],
    "registered":[50000,52000,80000,95000,130000,160000,175000,180000,165000,130000,85000,55000],
}

musim_map = {1:"Semi",2:"Panas",3:"Gugur",4:"Dingin"}
cuaca_map = {1:"Cerah",2:"Berawan",3:"Hujan Ringan",4:"Hujan Lebat"}

# Build hourly-pattern data
hours = list(range(24))
weekday_pattern  = [200,150,120,110,120,300,1100,1900,2200,1600,1400,1500,1800,1700,1600,1800,2500,2900,2400,2000,1600,1200,800,400]
weekend_pattern  = [300,200,160,140,130,200,400, 700, 1100,1400,1600,1700,1800,1850,1800,1750,1700,1600,1400,1200,900, 700, 500,350]

# Monthly season data for all combinations
monthly_data = []
for year in [2011, 2012]:
    d = data_2011 if year==2011 else data_2012
    for i, m in enumerate(months):
        season = [4,4,1,1,2,2,3,3,3,4,4,4][i]
        weather_choices = np.random.choice([1,2,3], size=1, p=[0.6,0.3,0.1])[0]
        monthly_data.append({
            "bulan": m, "bulan_idx": i+1, "tahun": year,
            "kasual": d["casual"][i],
            "terdaftar": d["registered"][i],
            "total": d["casual"][i]+d["registered"][i],
            "musim": musim_map[season],
            "cuaca": cuaca_map[weather_choices],
        })

df = pd.DataFrame(monthly_data)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚲 Filter Data")
    st.markdown("---")

    musim_opts  = ["Semua"] + list(df["musim"].unique())
    tahun_opts  = list(df["tahun"].unique())
    cuaca_opts  = list(df["cuaca"].unique())

    sel_musim  = st.selectbox("🌤 Pilih Musim", musim_opts)
    sel_tahun  = st.multiselect("📅 Pilih Tahun", tahun_opts, default=tahun_opts)
    sel_cuaca  = st.multiselect("🌦 Kondisi Cuaca", cuaca_opts, default=cuaca_opts)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#A8D8EA; line-height:1.6;'>
    <b style='color:#06D6A0;'>Dataset:</b> Capital Bikeshare<br>
    <b style='color:#06D6A0;'>Periode:</b> 2011 – 2012<br>
    <b style='color:#06D6A0;'>Catatan:</b> Data disimulasikan untuk keperluan demo.
    </div>
    """, unsafe_allow_html=True)

# ── Filter Application ────────────────────────────────────────────────────────
dff = df.copy()
if sel_musim != "Semua":
    dff = dff[dff["musim"] == sel_musim]
if sel_tahun:
    dff = dff[dff["tahun"].isin(sel_tahun)]
if sel_cuaca:
    dff = dff[dff["cuaca"].isin(sel_cuaca)]

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div style="font-size:2.8rem;">🚲</div>
  <div>
    <h1>Bike Rental Analytics</h1>
    <p>Eksplorasi pola peminjaman sepeda berdasarkan waktu, musim, dan kondisi cuaca.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ────────────────────────────────────────────────────────────────────
total    = dff["total"].sum()
kasual   = dff["kasual"].sum()
terdaftar= dff["terdaftar"].sum()
rasio    = round(terdaftar / total * 100, 1) if total > 0 else 0

c1, c2, c3, c4 = st.columns(4)
kpi_data = [
    (c1, f"{total:,.0f}", "Total Peminjaman", f"↑ {rasio}% terdaftar", "#06D6A0"),
    (c2, f"{kasual:,.0f}", "Pengguna Kasual",  f"{round(kasual/total*100,1) if total else 0}% dari total", "#FFB347"),
    (c3, f"{terdaftar:,.0f}", "Pengguna Terdaftar", f"{rasio}% dari total", "#118AB2"),
    (c4, f"{len(dff)}", "Rekaman Data", f"{len(sel_tahun)} tahun dipilih", "#EF476F"),
]

for col, val, label, delta, color in kpi_data:
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color:{color};">
          <div class="kpi-value" style="color:{color};">{val}</div>
          <div class="kpi-label">{label}</div>
          <div class="kpi-delta" style="color:{color};">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Perbandingan Pengguna",
    "📈 Tren Tahunan",
    "🌿 Distribusi Musiman",
    "⏰ Pola Harian",
])

COLORS = {
    "kasual":     "#FFB347",
    "terdaftar":  "#118AB2",
    "avg_kasual": "#FF6B35",
    "avg_terdaftar": "#06D6A0",
    "teal":       "#06D6A0",
    "navy":       "#0F4C75",
    "grid":       "rgba(0,0,0,0.06)",
}

PLOTLY_LAYOUT = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="DM Sans", color="#374151"),
    xaxis=dict(showgrid=False, linecolor="#E5E7EB"),
    yaxis=dict(gridcolor=COLORS["grid"], linecolor="#E5E7EB"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
    margin=dict(t=40, b=40, l=50, r=30),
)

# ── TAB 1: Perbandingan Pengguna ───────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-title">Jumlah Pengguna Kasual vs Terdaftar per Bulan</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Perbandingan volume peminjaman berdasarkan segmen pengguna</div>', unsafe_allow_html=True)

    # Group by month order
    monthly_agg = dff.groupby("bulan_idx").agg(
        kasual=("kasual","sum"), terdaftar=("terdaftar","sum")
    ).reindex(range(1,13)).fillna(0).reset_index()
    monthly_agg["bulan"] = months

    avg_k = monthly_agg["kasual"].mean()
    avg_r = monthly_agg["terdaftar"].mean()

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name="Kasual", x=monthly_agg["bulan"], y=monthly_agg["kasual"],
                          marker_color=COLORS["kasual"], marker_line_width=0))
    fig1.add_trace(go.Bar(name="Terdaftar", x=monthly_agg["bulan"], y=monthly_agg["terdaftar"],
                          marker_color=COLORS["terdaftar"], marker_line_width=0))
    fig1.add_hline(y=avg_k, line_dash="dot", line_color=COLORS["avg_kasual"],
                   annotation_text=f"Rata-rata Kasual: {avg_k:,.0f}",
                   annotation_font_color=COLORS["avg_kasual"])
    fig1.add_hline(y=avg_r, line_dash="dot", line_color=COLORS["avg_terdaftar"],
                   annotation_text=f"Rata-rata Terdaftar: {avg_r:,.0f}",
                   annotation_position="bottom right",
                   annotation_font_color=COLORS["avg_terdaftar"])
    fig1.update_layout(**PLOTLY_LAYOUT, barmode="group", height=420,
                        title_text="Jumlah Pengguna per Bulan", title_font_size=14)
    st.plotly_chart(fig1, use_container_width=True)

    # Proportion stacked
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-title" style="font-size:0.9rem;">Komposisi Per Bulan</div>', unsafe_allow_html=True)
        fig1b = go.Figure()
        fig1b.add_trace(go.Bar(name="Kasual", x=monthly_agg["bulan"], y=monthly_agg["kasual"],
                               marker_color=COLORS["kasual"]))
        fig1b.add_trace(go.Bar(name="Terdaftar", x=monthly_agg["bulan"], y=monthly_agg["terdaftar"],
                               marker_color=COLORS["terdaftar"]))
        fig1b.update_layout(**PLOTLY_LAYOUT, barmode="stack", height=300, showlegend=False)
        st.plotly_chart(fig1b, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title" style="font-size:0.9rem;">Proporsi Keseluruhan</div>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=["Kasual","Terdaftar"],
            values=[dff["kasual"].sum(), dff["terdaftar"].sum()],
            marker_colors=[COLORS["kasual"], COLORS["terdaftar"]],
            hole=0.55,
            textinfo="label+percent",
        ))
        fig_pie.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                               height=300, margin=dict(t=20,b=20,l=20,r=20),
                               font=dict(family="DM Sans"))
        st.plotly_chart(fig_pie, use_container_width=True)


# ── TAB 2: Tren Tahunan ────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">Fluktuasi Tren Tahunan</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Perbandingan total peminjaman antar tahun per bulan</div>', unsafe_allow_html=True)

    fig2 = go.Figure()
    palette = ["#0F4C75","#06D6A0","#FFB347","#EF476F"]

    for idx, yr in enumerate(sorted(dff["tahun"].unique())):
        ydf = dff[dff["tahun"]==yr].groupby("bulan_idx").agg(total=("total","sum")).reindex(range(1,13)).fillna(0).reset_index()
        ydf["bulan"] = months
        fig2.add_trace(go.Scatter(
            name=str(yr), x=ydf["bulan"], y=ydf["total"],
            mode="lines+markers",
            line=dict(color=palette[idx], width=3),
            marker=dict(size=8, color=palette[idx], line=dict(width=2, color="white")),
            fill="tozeroy", fillcolor=f"rgba{tuple(int(palette[idx].lstrip('#')[i:i+2],16) for i in (0,2,4)) + (0.08,)}",
        ))

    fig2.update_layout(**PLOTLY_LAYOUT, height=420, title_text="Total Peminjaman per Bulan per Tahun",
                        title_font_size=14)
    st.plotly_chart(fig2, use_container_width=True)

    # YoY growth
    if len(dff["tahun"].unique()) > 1:
        st.markdown('<div class="section-title" style="font-size:0.9rem; margin-top:12px;">Pertumbuhan YoY (%)</div>', unsafe_allow_html=True)
        pivot = dff.groupby(["tahun","bulan_idx"])["total"].sum().unstack(0).reindex(range(1,13))
        if 2011 in pivot.columns and 2012 in pivot.columns:
            growth = ((pivot[2012] - pivot[2011]) / pivot[2011] * 100).fillna(0)
            fig_g = go.Figure(go.Bar(
                x=months, y=growth.values,
                marker_color=[COLORS["teal"] if v>=0 else COLORS["avg_kasual"] for v in growth.values],
                marker_line_width=0,
            ))
            fig_g.update_layout(**PLOTLY_LAYOUT, height=280, title_text="% Pertumbuhan 2011→2012",
                                  title_font_size=13)
            fig_g.add_hline(y=0, line_color="#374151", line_width=1)
            st.plotly_chart(fig_g, use_container_width=True)


# ── TAB 3: Distribusi Musiman ──────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-title">Distribusi Berdasarkan Musim & Cuaca</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Pengaruh kondisi lingkungan terhadap volume peminjaman</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="section-title" style="font-size:0.9rem;">Rata-rata Peminjaman per Musim</div>', unsafe_allow_html=True)
        season_agg = dff.groupby("musim")[["kasual","terdaftar"]].mean().reset_index()
        fig_s = go.Figure()
        fig_s.add_trace(go.Bar(name="Kasual", x=season_agg["musim"], y=season_agg["kasual"],
                               marker_color=COLORS["kasual"]))
        fig_s.add_trace(go.Bar(name="Terdaftar", x=season_agg["musim"], y=season_agg["terdaftar"],
                               marker_color=COLORS["terdaftar"]))
        fig_s.update_layout(**PLOTLY_LAYOUT, barmode="group", height=340)
        st.plotly_chart(fig_s, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title" style="font-size:0.9rem;">Distribusi per Kondisi Cuaca</div>', unsafe_allow_html=True)
        weather_agg = dff.groupby("cuaca")["total"].mean().reset_index()
        fig_w = go.Figure(go.Bar(
            x=weather_agg["total"], y=weather_agg["cuaca"],
            orientation="h",
            marker=dict(
                color=weather_agg["total"],
                colorscale=[[0,"#A8D8EA"],[0.5,"#118AB2"],[1,"#0F4C75"]],
                showscale=False,
            ),
        ))
        fig_w.update_layout(**PLOTLY_LAYOUT, height=340, xaxis_title="Rata-rata Total")
        st.plotly_chart(fig_w, use_container_width=True)

    # Heatmap musim x bulan
    st.markdown('<div class="section-title" style="font-size:0.9rem; margin-top:8px;">Peta Panas: Total per Musim & Bulan</div>', unsafe_allow_html=True)
    heat_data = dff.groupby(["musim","bulan_idx"])["total"].sum().unstack(fill_value=0)
    fig_heat = go.Figure(go.Heatmap(
        z=heat_data.values,
        x=[months[i-1] for i in heat_data.columns],
        y=heat_data.index,
        colorscale=[[0,"#EAF6FB"],[0.5,"#118AB2"],[1,"#0F4C75"]],
        text=heat_data.values,
        texttemplate="%{text:,.0f}",
        textfont_size=10,
    ))
    fig_heat.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                            height=280, margin=dict(t=20,b=40,l=80,r=20),
                            font=dict(family="DM Sans"))
    st.plotly_chart(fig_heat, use_container_width=True)


# ── TAB 4: Pola Harian ─────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-title">Pola Penggunaan Berdasarkan Jam</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Distribusi peminjaman sepanjang hari pada hari kerja vs akhir pekan</div>', unsafe_allow_html=True)

    fig_h = go.Figure()
    fig_h.add_trace(go.Scatter(
        name="Hari Kerja", x=hours, y=weekday_pattern,
        mode="lines", fill="tozeroy",
        line=dict(color=COLORS["terdaftar"], width=3),
        fillcolor="rgba(17,138,178,0.15)",
    ))
    fig_h.add_trace(go.Scatter(
        name="Akhir Pekan", x=hours, y=weekend_pattern,
        mode="lines", fill="tozeroy",
        line=dict(color=COLORS["kasual"], width=3),
        fillcolor="rgba(255,179,71,0.15)",
    ))
    fig_h.update_layout(**PLOTLY_LAYOUT, height=400,
                         title_text="Rata-rata Peminjaman per Jam", title_font_size=14)
    fig_h.update_xaxes(tickmode="linear", dtick=2, title="Jam", showgrid=False, linecolor="#E5E7EB")
    fig_h.update_yaxes(title="Jumlah Peminjaman", gridcolor=COLORS["grid"])
    st.plotly_chart(fig_h, use_container_width=True)

    col_m, col_e = st.columns(2)
    with col_m:
        st.markdown('<div class="section-title" style="font-size:0.9rem;">Pola Pagi (05.00–12.00)</div>', unsafe_allow_html=True)
        fig_am = go.Figure()
        fig_am.add_trace(go.Bar(name="Kerja", x=hours[5:13], y=weekday_pattern[5:13],
                                marker_color=COLORS["terdaftar"]))
        fig_am.add_trace(go.Bar(name="Akhir Pekan", x=hours[5:13], y=weekend_pattern[5:13],
                                marker_color=COLORS["kasual"]))
        fig_am.update_layout(**PLOTLY_LAYOUT, barmode="group", height=280, showlegend=False)
        st.plotly_chart(fig_am, use_container_width=True)

    with col_e:
        st.markdown('<div class="section-title" style="font-size:0.9rem;">Pola Sore (13.00–20.00)</div>', unsafe_allow_html=True)
        fig_pm = go.Figure()
        fig_pm.add_trace(go.Bar(name="Kerja", x=hours[13:21], y=weekday_pattern[13:21],
                                marker_color=COLORS["terdaftar"]))
        fig_pm.add_trace(go.Bar(name="Akhir Pekan", x=hours[13:21], y=weekend_pattern[13:21],
                                marker_color=COLORS["kasual"]))
        fig_pm.update_layout(**PLOTLY_LAYOUT, barmode="group", height=280, showlegend=False)
        st.plotly_chart(fig_pm, use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; font-size:0.78rem; color:#9CA3AF; padding:12px 0;'>
  🚲 Bike Rental Analytics Dashboard &nbsp;·&nbsp; Data: Capital Bikeshare (Simulasi) &nbsp;·&nbsp; Built with Streamlit + Plotly
</div>
""", unsafe_allow_html=True)