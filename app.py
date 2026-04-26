"""
Fiscal Storyteller BA — Histórias fiscais dos municípios da Bahia
Dados: PNCP + IBGE + SICONFI

Rodar: streamlit run app.py
Dependências: pip install streamlit pandas plotly pillow kaleido
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib.parse
import base64
import io
import json
import re

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fiscal Storyteller BA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PALETTE = {
    "bg":       "#0F1117",
    "card":     "#1A1D27",
    "border":   "#2A2D3E",
    "accent":   "#F5A623",
    "accent2":  "#E84393",
    "text":     "#E8EAF0",
    "muted":    "#7C7F9A",
    "good":     "#27D9A4",
    "bad":      "#F55B5B",
    "blue":     "#4A9EF5",
}

CAT_LABELS = {
    "artistico":     "🎭 Artístico / Shows",
    "locacao":       "🏗️ Locação",
    "consultoria":   "💼 Consultoria",
    "outros":        "📦 Outros",
    "saude":         "🏥 Saúde",
    "capacitacao":   "📚 Capacitação",
    "aquisicao":     "🛒 Aquisição",
    "credenciamento":"🪪 Credenciamento",
    "manutencao":    "🔧 Manutenção",
}

SUBCAT_LABELS = {
    "outros_show":   "Show Genérico",
    "forro_sao_joao":"Forró / São João",
    "carnaval":      "Carnaval",
}

CAT_COLORS = {
    "artistico":     "#F5A623",
    "locacao":       "#4A9EF5",
    "consultoria":   "#27D9A4",
    "outros":        "#9B7FE8",
    "saude":         "#F55B5B",
    "capacitacao":   "#E84393",
    "aquisicao":     "#FF8C42",
    "credenciamento":"#6BCB77",
    "manutencao":    "#A0C4FF",
}

# ─────────────────────────────────────────────────────────────────────────────
# CSS CUSTOMIZADO — dark editorial com detalhes âmbar
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {{
    background-color: {PALETTE['bg']};
    color: {PALETTE['text']};
    font-family: 'DM Sans', sans-serif;
  }}

  /* Esconde a barra lateral e header padrão */
  .block-container {{ padding: 2rem 2rem 4rem; max-width: 1400px; }}
  #MainMenu, footer, header {{ visibility: hidden; }}

  /* ─── HERO ─── */
  .hero {{
    background: linear-gradient(135deg, #0F1117 0%, #1a1020 50%, #0F1117 100%);
    border: 1px solid {PALETTE['border']};
    border-top: 3px solid {PALETTE['accent']};
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
  }}
  .hero::before {{
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(245,166,35,0.12) 0%, transparent 70%);
    border-radius: 50%;
  }}
  .hero-tag {{
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: {PALETTE['accent']};
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }}
  .hero-title {{
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1.1;
    color: {PALETTE['text']};
    margin: 0;
  }}
  .hero-sub {{
    font-size: 1rem;
    color: {PALETTE['muted']};
    margin-top: 0.6rem;
    max-width: 600px;
  }}

  /* ─── SEARCH BAR ─── */
  .stTextInput > div > div > input {{
    background: {PALETTE['card']};
    border: 1.5px solid {PALETTE['border']};
    border-radius: 10px;
    color: {PALETTE['text']};
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    padding: 0.75rem 1rem;
    transition: border-color 0.2s;
  }}
  .stTextInput > div > div > input:focus {{
    border-color: {PALETTE['accent']};
    box-shadow: 0 0 0 3px rgba(245,166,35,0.15);
  }}

  /* ─── SELECTBOX ─── */
  .stSelectbox > div > div {{
    background: {PALETTE['card']};
    border: 1.5px solid {PALETTE['border']};
    border-radius: 10px;
    color: {PALETTE['text']};
  }}

  /* ─── KPI CARDS ─── */
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
  }}
  .kpi-card {{
    background: {PALETTE['card']};
    border: 1px solid {PALETTE['border']};
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
  }}
  .kpi-card:hover {{ transform: translateY(-2px); border-color: {PALETTE['accent']}; }}
  .kpi-card.highlight {{ border-color: {PALETTE['accent']}; border-top: 3px solid {PALETTE['accent']}; }}
  .kpi-card.danger {{ border-top: 3px solid {PALETTE['bad']}; }}
  .kpi-label {{
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {PALETTE['muted']};
    margin-bottom: 0.5rem;
  }}
  .kpi-value {{
    font-family: 'Syne', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: {PALETTE['text']};
    line-height: 1.1;
  }}
  .kpi-value.amber {{ color: {PALETTE['accent']}; }}
  .kpi-value.green {{ color: {PALETTE['good']}; }}
  .kpi-value.pink  {{ color: {PALETTE['accent2']}; }}
  .kpi-sub {{
    font-size: 0.78rem;
    color: {PALETTE['muted']};
    margin-top: 0.3rem;
  }}

  /* ─── NARRATIVE BOX ─── */
  .narrative {{
    background: linear-gradient(135deg, #1A1D27 0%, #1f1525 100%);
    border: 1px solid {PALETTE['border']};
    border-left: 4px solid {PALETTE['accent']};
    border-radius: 14px;
    padding: 2rem 2.2rem;
    margin: 1.5rem 0;
    font-size: 1.08rem;
    line-height: 1.8;
    color: {PALETTE['text']};
    font-family: 'DM Sans', sans-serif;
  }}
  .narrative strong {{ color: {PALETTE['accent']}; }}
  .narrative em {{ color: {PALETTE['good']}; font-style: normal; }}

  /* ─── SECTION HEADERS ─── */
  .section-header {{
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: {PALETTE['text']};
    border-bottom: 1px solid {PALETTE['border']};
    padding-bottom: 0.5rem;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }}

  /* ─── RANK BADGE ─── */
  .rank-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(245,166,35,0.12);
    border: 1px solid rgba(245,166,35,0.3);
    color: {PALETTE['accent']};
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-weight: 500;
  }}

  /* ─── SHARE BUTTONS ─── */
  .share-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-top: 1rem;
  }}
  .share-btn {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.55rem 1.2rem;
    border-radius: 8px;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    font-weight: 500;
    text-decoration: none !important;
    transition: opacity 0.2s, transform 0.15s;
    cursor: pointer;
    border: none;
  }}
  .share-btn:hover {{ opacity: 0.85; transform: translateY(-1px); }}
  .btn-whatsapp {{ background: #25D366; color: #fff; }}
  .btn-twitter  {{ background: #000; color: #fff; border: 1px solid #333; }}
  .btn-linkedin {{ background: #0A66C2; color: #fff; }}
  .btn-insta    {{ background: linear-gradient(135deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888); color:#fff; }}

  /* ─── STBUTTON OVERRIDE ─── */
  .stButton > button {{
    background: {PALETTE['card']};
    border: 1.5px solid {PALETTE['border']};
    color: {PALETTE['text']};
    border-radius: 10px;
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    padding: 0.55rem 1.4rem;
    transition: all 0.2s;
  }}
  .stButton > button:hover {{
    border-color: {PALETTE['accent']};
    color: {PALETTE['accent']};
  }}

  /* ─── SCROLLBAR ─── */
  ::-webkit-scrollbar {{ width: 6px; }}
  ::-webkit-scrollbar-track {{ background: {PALETTE['bg']}; }}
  ::-webkit-scrollbar-thumb {{ background: {PALETTE['border']}; border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DADOS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Carregando dados da Bahia…")
def load_data():
    df = pd.read_csv("pncp_ibge_siconfi_BA_final.csv", low_memory=False)
    # Limpa quotes nas categorias
    for col in ["categoria", "subcategoria"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip("'").str.strip()
    df["municipio_nome"] = df["unidadeOrgao.municipioNome"].astype(str).str.strip()
    # Filtra contratos municipais e sem outliers
    df = df[df["flag_nao_municipal"] != True]
    df = df[df["flag_outlier"] != True]
    df["ano_compra"] = pd.to_numeric(df["anoCompra"], errors="coerce")
    df = df[df["ano_compra"].isin([2024, 2025, 2026])]
    return df


@st.cache_data(show_spinner=False)
def build_municipio_summary(df):
    """Agrega métricas por município."""
    grp = df.groupby("municipio_nome")

    total_contratos = grp["valor_final"].count().rename("total_contratos")
    total_valor = grp["valor_final"].sum().rename("total_valor")

    art = df[df["categoria"] == "artistico"]
    art_contratos = art.groupby("municipio_nome")["valor_final"].count().rename("art_contratos")
    art_valor = art.groupby("municipio_nome")["valor_final"].sum().rename("art_valor")

    # Dados demográficos/fiscais — pega primeiro registro (idênticos por município)
    meta = grp.agg(
        populacao=("ibge_populacao", "first"),
        pib=("ibge_pib", "first"),
        pib_pc=("ibge_pib_pc", "first"),
        rcl=("rcl_R$", "first"),
    )

    summary = pd.concat([total_contratos, total_valor, art_contratos, art_valor, meta], axis=1).reset_index()
    summary = summary.fillna(0)

    summary["art_per_capita"] = summary.apply(
        lambda r: r["art_valor"] / r["populacao"] if r["populacao"] > 0 else 0, axis=1
    )
    summary["art_pct_rcl"] = summary.apply(
        lambda r: (r["art_valor"] / r["rcl"] * 100) if r["rcl"] > 0 else 0, axis=1
    )
    summary["art_pct_pib"] = summary.apply(
        lambda r: (r["art_valor"] / r["pib"] * 100) if r["pib"] > 0 else 0, axis=1
    )

    # Ranking por art_pct_rcl (só quem tem shows)
    com_shows = summary[summary["art_contratos"] > 0].copy()
    com_shows["rank_ba"] = com_shows["art_pct_rcl"].rank(ascending=False).astype(int)
    summary = summary.merge(com_shows[["municipio_nome","rank_ba"]], on="municipio_nome", how="left")
    summary["rank_ba"] = summary["rank_ba"].fillna(-1).astype(int)

    summary["total_muns_com_shows"] = int((summary["art_contratos"] > 0).sum())

    return summary


def get_municipio_stats(summary_df, nome):
    row = summary_df[summary_df["municipio_nome"].str.lower() == nome.lower()]
    if row.empty:
        return None
    return row.iloc[0]


@st.cache_data(show_spinner=False)
def get_categorias_municipio(df, nome):
    mdf = df[df["municipio_nome"].str.lower() == nome.lower()]
    cats = mdf.groupby("categoria")["valor_final"].agg(["sum","count"]).reset_index()
    cats.columns = ["categoria","valor","contratos"]
    cats = cats.sort_values("valor", ascending=False)
    return cats


@st.cache_data(show_spinner=False)
def get_shows_subcategorias(df, nome):
    mdf = df[(df["municipio_nome"].str.lower() == nome.lower()) & (df["categoria"] == "artistico")]
    if mdf.empty:
        return pd.DataFrame()
    sub = mdf.groupby("subcategoria")["valor_final"].agg(["sum","count"]).reset_index()
    sub.columns = ["subcategoria","valor","contratos"]
    sub = sub.sort_values("valor", ascending=False)
    return sub


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS FORMATAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
def fmt_brl(v, decimals=0):
    if v >= 1_000_000_000:
        return f"R$ {v/1e9:.1f} bi"
    elif v >= 1_000_000:
        return f"R$ {v/1e6:.1f} mi"
    elif v >= 1_000:
        return f"R$ {v/1e3:,.0f} mil"
    return f"R$ {v:,.{decimals}f}"


def fmt_pop(v):
    if v >= 1_000_000:
        return f"{v/1e6:.2f} mi hab."
    return f"{int(v):,} hab.".replace(",", ".")


def rank_emoji(rank, total):
    pct = rank / total if total > 0 else 1
    if pct <= 0.1: return "🔴"
    if pct <= 0.25: return "🟠"
    if pct <= 0.5: return "🟡"
    return "🟢"


# ─────────────────────────────────────────────────────────────────────────────
# GERAÇÃO DE NARRATIVA
# ─────────────────────────────────────────────────────────────────────────────
def gerar_narrativa(stats, df_raw, nome):
    pop   = int(stats.get("populacao", 0) or 0)
    pib   = float(stats.get("pib", 0) or 0)
    rcl   = float(stats.get("rcl", 0) or 0)
    art_n = int(stats.get("art_contratos", 0) or 0)
    art_v = float(stats.get("art_valor", 0) or 0)
    art_pc = float(stats.get("art_per_capita", 0) or 0)
    art_pct_rcl = float(stats.get("art_pct_rcl", 0) or 0)
    total_c = int(stats.get("total_contratos", 0) or 0)
    total_v = float(stats.get("total_valor", 0) or 0)
    rank = int(stats.get("rank_ba", -1))
    total_muns = int(stats.get("total_muns_com_shows", 0))

    # Análises específicas de subcategoria
    sub = get_shows_subcategorias(df_raw, nome)
    sub_destaque = ""
    if not sub.empty:
        top_sub = sub.iloc[0]
        label = SUBCAT_LABELS.get(str(top_sub["subcategoria"]), top_sub["subcategoria"])
        pct_sub = top_sub["valor"] / art_v * 100 if art_v > 0 else 0
        sub_destaque = f" A categoria dominante foi <strong>{label}</strong>, responsável por {pct_sub:.0f}% desse total."

    # Texto de contextualização
    pop_str = fmt_pop(pop) if pop else "população não disponível"
    pib_str = fmt_brl(pib) if pib else "PIB não disponível"
    rcl_str = fmt_brl(rcl) if rcl else "RCL não disponível"
    art_v_str = fmt_brl(art_v) if art_v else "R$ 0"
    art_pc_str = f"R$ {art_pc:.2f}" if art_pc else "R$ 0,00"
    art_pct_str = f"{art_pct_rcl:.2f}%"
    total_v_str = fmt_brl(total_v)

    # Veredicto de contexto
    if art_pct_rcl > 5:
        veredicto = f"Isso representa um comprometimento <strong>muito expressivo</strong> da receita municipal — acima de 5% — sinalizando uma prioridade política clara para o setor cultural e de entretenimento."
        alert = "⚠️"
    elif art_pct_rcl > 2:
        veredicto = f"Esse volume está <strong>acima da média estadual</strong>, indicando forte investimento em eventos e cultura."
        alert = "🟠"
    elif art_pct_rcl > 0.5:
        veredicto = f"O gasto está dentro de um <strong>patamar moderado</strong> para os padrões da Bahia."
        alert = "🟡"
    elif art_pct_rcl > 0:
        veredicto = f"O investimento em shows é <strong>relativamente baixo</strong> frente à capacidade fiscal do município."
        alert = "🟢"
    else:
        veredicto = "Não foram identificados contratos artísticos no período analisado."
        alert = "ℹ️"

    rank_str = ""
    if rank > 0:
        rank_str = f"No ranking estadual de gasto artístico como proporção da receita, <strong>{nome}</strong> ocupa a {rank}ª posição entre os {total_muns} municípios baianos com shows registrados no PNCP."

    if art_n == 0:
        return f"""
<strong>{nome}</strong> possui <strong>{pop_str}</strong> e PIB estimado de <strong>{pib_str}</strong>.
No período analisado (2024–2026), o município realizou <strong>{total_c} contratos públicos</strong>,
movimentando <strong>{total_v_str}</strong> no total.

{alert} Não foram encontrados contratos artísticos ou de shows neste período.
Isso pode indicar que o município não realizou eventos públicos licitados ou que utilizou
outros mecanismos não registrados no PNCP.
"""

    return f"""
<strong>{nome}</strong> possui <strong>{pop_str}</strong> e PIB estimado de <strong>{pib_str}</strong>,
com uma Receita Corrente Líquida (RCL) de <strong>{rcl_str}</strong>.

No período analisado (2024–2026), o município realizou <strong>{art_n} contrato{'s' if art_n != 1 else ''} artístico{'s' if art_n != 1 else ''}</strong>
via PNCP, totalizando <strong>{art_v_str}</strong> em shows e eventos.{sub_destaque}

Isso representa <strong>{art_pc_str} por habitante</strong> e <strong>{art_pct_str} da receita municipal</strong>.

{veredicto}

{rank_str}

No total, o município registrou <strong>{total_c} contratos públicos</strong> ({total_v_str}),
dos quais os contratos artísticos representam
<em>{art_v/total_v*100:.1f}%</em> do volume financeiro contratado.
"""


# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICOS
# ─────────────────────────────────────────────────────────────────────────────
def fig_categorias(cats, nome):
    cats_labeled = cats.copy()
    cats_labeled["label"] = cats_labeled["categoria"].map(CAT_LABELS).fillna(cats_labeled["categoria"])
    cats_labeled["cor"] = cats_labeled["categoria"].map(CAT_COLORS).fillna("#7C7F9A")
    cats_labeled["valor_fmt"] = cats_labeled["valor"].apply(fmt_brl)

    fig = go.Figure(go.Bar(
        x=cats_labeled["label"],
        y=cats_labeled["valor"],
        marker_color=cats_labeled["cor"].tolist(),
        text=cats_labeled["valor_fmt"],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Valor: %{text}<br>Contratos: %{customdata}<extra></extra>",
        customdata=cats_labeled["contratos"],
    ))
    fig.update_layout(
        title=dict(text=f"Distribuição de Contratos — {nome}", font=dict(family="Syne", size=16, color="#E8EAF0")),
        paper_bgcolor="#1A1D27",
        plot_bgcolor="#1A1D27",
        font=dict(family="DM Sans", color="#7C7F9A"),
        xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#E8EAF0")),
        yaxis=dict(showgrid=True, gridcolor="#2A2D3E", tickfont=dict(size=11, color="#7C7F9A"),
                   title="Valor (R$)"),
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=False,
        height=380,
    )
    return fig


def fig_ranking(summary_df, nome):
    com_shows = summary_df[summary_df["art_contratos"] > 0].copy()
    com_shows = com_shows.sort_values("art_pct_rcl", ascending=False).reset_index(drop=True)
    com_shows["rank"] = range(1, len(com_shows) + 1)

    # Top 15 + município selecionado
    top15 = com_shows.head(15).copy()
    mun_row = com_shows[com_shows["municipio_nome"].str.lower() == nome.lower()]
    if not mun_row.empty and nome.lower() not in top15["municipio_nome"].str.lower().values:
        top15 = pd.concat([top15, mun_row]).drop_duplicates("municipio_nome")

    top15 = top15.sort_values("art_pct_rcl", ascending=True)
    top15["cor"] = top15["municipio_nome"].apply(
        lambda m: PALETTE["accent"] if m.lower() == nome.lower() else PALETTE["blue"]
    )
    top15["val_fmt"] = top15["art_pct_rcl"].apply(lambda v: f"{v:.2f}%")
    top15["label"] = top15["municipio_nome"].apply(
        lambda m: f"▶ {m}" if m.lower() == nome.lower() else m
    )

    fig = go.Figure(go.Bar(
        y=top15["label"],
        x=top15["art_pct_rcl"],
        orientation="h",
        marker_color=top15["cor"].tolist(),
        text=top15["val_fmt"],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>%{x:.2f}% da RCL<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Ranking: Gasto em Shows (% da RCL)", font=dict(family="Syne", size=16, color="#E8EAF0")),
        paper_bgcolor="#1A1D27",
        plot_bgcolor="#1A1D27",
        font=dict(family="DM Sans", color="#7C7F9A"),
        xaxis=dict(showgrid=True, gridcolor="#2A2D3E", ticksuffix="%", tickfont=dict(size=11, color="#7C7F9A")),
        yaxis=dict(showgrid=False, tickfont=dict(size=11, color="#E8EAF0")),
        margin=dict(l=20, r=60, t=60, b=20),
        showlegend=False,
        height=max(380, len(top15) * 32 + 80),
    )
    return fig


def fig_subcategorias_shows(sub):
    if sub.empty:
        return None
    sub_labeled = sub.copy()
    sub_labeled["label"] = sub_labeled["subcategoria"].map(SUBCAT_LABELS).fillna(sub_labeled["subcategoria"])
    sub_labeled["val_fmt"] = sub_labeled["valor"].apply(fmt_brl)

    cores = ["#F5A623", "#E84393", "#27D9A4", "#4A9EF5", "#9B7FE8"]

    fig = go.Figure(go.Pie(
        labels=sub_labeled["label"],
        values=sub_labeled["valor"],
        hole=0.55,
        marker_colors=cores[:len(sub_labeled)],
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>%{customdata}<br>%{percent}<extra></extra>",
        customdata=sub_labeled["val_fmt"],
        textfont=dict(family="DM Sans", size=12, color="#E8EAF0"),
    ))
    fig.update_layout(
        title=dict(text="Tipos de Show Contratados", font=dict(family="Syne", size=16, color="#E8EAF0")),
        paper_bgcolor="#1A1D27",
        plot_bgcolor="#1A1D27",
        font=dict(family="DM Sans", color="#7C7F9A"),
        showlegend=True,
        legend=dict(font=dict(color="#E8EAF0"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=20, r=20, t=60, b=20),
        height=340,
    )
    return fig


def fig_comparacao_media(stats, summary_df, nome):
    media_ba_pct = float(summary_df[summary_df["art_contratos"] > 0]["art_pct_rcl"].median())
    media_ba_pc = float(summary_df[summary_df["art_contratos"] > 0]["art_per_capita"].median())

    mun_pct = float(stats.get("art_pct_rcl", 0) or 0)
    mun_pc = float(stats.get("art_per_capita", 0) or 0)

    categories = ["% da RCL", "R$ per capita"]
    values_mun = [mun_pct, mun_pc]
    values_ba = [media_ba_pct, media_ba_pc]

    fig = make_subplots(rows=1, cols=2, subplot_titles=["% da Receita Municipal (RCL)", "Gasto Per Capita (R$)"])

    for i, (cat, vm, vb) in enumerate(zip(categories, values_mun, values_ba)):
        col = i + 1
        fig.add_trace(go.Bar(
            name=nome if i == 0 else "",
            x=[nome, "Mediana BA"],
            y=[vm, vb],
            marker_color=[PALETTE["accent"], PALETTE["blue"]],
            text=[f"{vm:.2f}{'%' if i==0 else ''}", f"{vb:.2f}{'%' if i==0 else ''}"],
            textposition="outside",
            showlegend=False,
            hovertemplate=f"<b>%{{x}}</b><br>{cat}: %{{y:.2f}}<extra></extra>",
        ), row=1, col=col)

    fig.update_layout(
        title=dict(text="Comparação com Mediana Estadual", font=dict(family="Syne", size=16, color="#E8EAF0")),
        paper_bgcolor="#1A1D27",
        plot_bgcolor="#1A1D27",
        font=dict(family="DM Sans", color="#7C7F9A"),
        height=340,
        margin=dict(l=20, r=20, t=80, b=20),
    )
    for ax in ["xaxis", "xaxis2"]:
        fig.update_layout(**{ax: dict(showgrid=False, tickfont=dict(color="#E8EAF0"))})
    for ax in ["yaxis", "yaxis2"]:
        fig.update_layout(**{ax: dict(showgrid=True, gridcolor="#2A2D3E", tickfont=dict(color="#7C7F9A"))})
    for ann in fig.layout.annotations:
        ann.update(font=dict(color="#7C7F9A", size=12))

    return fig


# ─────────────────────────────────────────────────────────────────────────────
# COMPARTILHAMENTO
# ─────────────────────────────────────────────────────────────────────────────
def build_share_text(stats, nome):
    art_n   = int(stats.get("art_contratos", 0) or 0)
    art_v   = float(stats.get("art_valor", 0) or 0)
    art_pc  = float(stats.get("art_per_capita", 0) or 0)
    art_pct = float(stats.get("art_pct_rcl", 0) or 0)
    pop     = int(stats.get("populacao", 0) or 0)

    if art_n == 0:
        return (
            f"🔍 {nome} (BA) não registrou contratos artísticos no PNCP entre 2024–2026.\n"
            f"Dados de transparência pública • Fiscal Storyteller BA"
        )

    art_v_str = fmt_brl(art_v)
    art_pc_str = f"R$ {art_pc:.2f}"
    return (
        f"🎭 {nome} (BA) contratou {art_n} shows entre 2024 e 2026, "
        f"totalizando {art_v_str}. "
        f"Isso representa {art_pc_str} por habitante "
        f"e {art_pct:.2f}% do orçamento municipal.\n\n"
        f"Dados: PNCP + SICONFI • Fiscal Storyteller BA"
    )


def share_buttons(texto):
    texto_enc = urllib.parse.quote(texto)
    url_app = "https://fiscal-storyteller-ba.streamlit.app"
    url_enc = urllib.parse.quote(url_app)

    whatsapp = f"https://wa.me/?text={texto_enc}%0A{url_enc}"
    twitter  = f"https://twitter.com/intent/tweet?text={texto_enc}&url={url_enc}"
    linkedin = f"https://www.linkedin.com/sharing/share-offsite/?url={url_enc}&summary={texto_enc}"
    insta    = f"data:text/plain,{texto_enc}"  # Instagram não suporta deep link, abrimos o texto

    st.markdown(f"""
    <div class="share-row">
      <a class="share-btn btn-whatsapp" href="{whatsapp}" target="_blank">
        📲 WhatsApp
      </a>
      <a class="share-btn btn-twitter" href="{twitter}" target="_blank">
        𝕏 Twitter / X
      </a>
      <a class="share-btn btn-linkedin" href="{linkedin}" target="_blank">
        🔵 LinkedIn
      </a>
      <span class="share-btn btn-insta" onclick="navigator.clipboard.writeText(document.getElementById('share-text').innerText);alert('Texto copiado! Cole no Instagram.');">
        📸 Instagram (copiar)
      </span>
    </div>
    <p id="share-text" style="display:none">{texto.replace(chr(10),' ')}</p>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# CARD IMAGEM COMPARTILHÁVEL
# ─────────────────────────────────────────────────────────────────────────────
def generate_share_image(stats, nome):
    """Gera um card PNG simples e retorna como bytes."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None

    W, H = 1080, 600
    BG        = (15, 17, 23)
    CARD_BG   = (26, 29, 39)
    AMBER     = (245, 166, 35)
    WHITE     = (232, 234, 240)
    MUTED     = (124, 127, 154)
    GREEN     = (39, 217, 164)

    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Linha accent topo
    draw.rectangle([(0, 0), (W, 5)], fill=AMBER)

    # Background card central
    draw.rounded_rectangle([(40, 30), (W-40, H-30)], radius=20, fill=CARD_BG, outline=(42,45,62), width=1)

    # Fonte padrão (PIL sem fontes externas usa bitmap)
    try:
        fnt_big   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
        fnt_med   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        fnt_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        fnt_tag   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
    except Exception:
        fnt_big = fnt_med = fnt_small = fnt_tag = ImageFont.load_default()

    art_n   = int(stats.get("art_contratos", 0) or 0)
    art_v   = float(stats.get("art_valor", 0) or 0)
    art_pc  = float(stats.get("art_per_capita", 0) or 0)
    art_pct = float(stats.get("art_pct_rcl", 0) or 0)
    pop     = int(stats.get("populacao", 0) or 0)

    # Tag
    draw.text((80, 60), "FISCAL STORYTELLER BA • DADOS PNCP + SICONFI", fill=AMBER, font=fnt_tag)

    # Nome do município
    draw.text((80, 100), nome.upper(), fill=WHITE, font=fnt_big)

    # Linha divisória
    draw.line([(80, 175), (W-80, 175)], fill=(42,45,62), width=1)

    # KPIs
    kpis = [
        ("SHOWS CONTRATADOS", str(art_n), AMBER),
        ("TOTAL INVESTIDO",   fmt_brl(art_v), WHITE),
        ("GASTO PER CAPITA",  f"R$ {art_pc:.2f}", GREEN),
        ("% DA RECEITA",      f"{art_pct:.2f}%", (232,67,147)),
    ]

    x_start = 80
    y_kpi   = 210
    col_w   = (W - 160) // 4

    for i, (lbl, val, cor) in enumerate(kpis):
        cx = x_start + i * col_w
        # Separador vertical
        if i > 0:
            draw.line([(cx, y_kpi), (cx, y_kpi + 110)], fill=(42,45,62), width=1)
        draw.text((cx + 10, y_kpi),       lbl, fill=MUTED, font=fnt_tag)
        draw.text((cx + 10, y_kpi + 28),  val, fill=cor,   font=fnt_med)

    # Linha narrativa
    if art_n > 0:
        pop_str = fmt_pop(pop)
        linha = f"{nome} contratou {art_n} shows ({fmt_brl(art_v)}), {art_pct:.2f}% do orçamento municipal."
    else:
        linha = f"{nome} não registrou contratos artísticos no PNCP (2024-2026)."

    draw.text((80, H - 120), linha, fill=MUTED, font=fnt_small)

    # Rodapé
    draw.text((80, H - 70), "Dados públicos via Portal Nacional de Contratações Públicas (PNCP)", fill=(60,63,80), font=fnt_tag)

    buf = io.BytesIO()
    img.save(buf, format="PNG", dpi=(150, 150))
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
df = load_data()
summary = build_municipio_summary(df)
municipios_lista = sorted(df["municipio_nome"].dropna().astype(str).unique().tolist())

# ─── HERO ───
st.markdown("""
<div class="hero">
  <div class="hero-tag">📊 Dados públicos · PNCP + IBGE + SICONFI · Bahia 2024–2026</div>
  <h1 class="hero-title">Fiscal Storyteller BA</h1>
  <p class="hero-sub">
    Transformando contratos públicos em histórias fiscais.
    Descubra como seu município gasta com shows, eventos e cultura.
  </p>
</div>
""", unsafe_allow_html=True)


# ─── BUSCA ───
col_search, col_sel = st.columns([2, 3])
with col_search:
    busca = st.text_input(
        "🔍  Buscar município",
        placeholder="Digite parte do nome…",
        label_visibility="collapsed",
    )

with col_sel:
    if busca.strip():
        matches = [m for m in municipios_lista if busca.strip().lower() in m.lower()]
        if not matches:
            st.warning("Nenhum município encontrado. Tente outro nome.")
            st.stop()
        nome_sel = st.selectbox(
            "Selecione o município",
            matches,
            label_visibility="collapsed",
        )
    else:
        nome_sel = st.selectbox(
            "Ou escolha na lista",
            ["— selecione —"] + municipios_lista,
            label_visibility="collapsed",
        )
        if nome_sel == "— selecione —":
            st.markdown("""
            <div style="text-align:center;padding:3rem;color:#7C7F9A;font-family:'DM Sans'">
              <div style="font-size:3rem">📍</div>
              <div style="font-size:1.1rem;margin-top:1rem">
                Digite o nome de um município baiano para explorar a sua história fiscal.
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.stop()


# ─── DADOS DO MUNICÍPIO ───
stats = get_municipio_stats(summary, nome_sel)
if stats is None:
    st.error(f"Dados não encontrados para {nome_sel}.")
    st.stop()

cats  = get_categorias_municipio(df, nome_sel)
sub   = get_shows_subcategorias(df, nome_sel)

pop       = int(stats.get("populacao", 0) or 0)
pib       = float(stats.get("pib", 0) or 0)
rcl       = float(stats.get("rcl", 0) or 0)
art_n     = int(stats.get("art_contratos", 0) or 0)
art_v     = float(stats.get("art_valor", 0) or 0)
art_pc    = float(stats.get("art_per_capita", 0) or 0)
art_pct   = float(stats.get("art_pct_rcl", 0) or 0)
total_c   = int(stats.get("total_contratos", 0) or 0)
total_v   = float(stats.get("total_valor", 0) or 0)
rank_ba   = int(stats.get("rank_ba", -1))
total_mns = int(stats.get("total_muns_com_shows", 0))


# ─── KPIs ───
st.markdown(f"""
<div class="section-header">
  📌 {nome_sel}
  {'<span class="rank-badge">' + rank_emoji(rank_ba, total_mns) + ' #' + str(rank_ba) + 'º no ranking BA</span>' if rank_ba > 0 else ''}
</div>
""", unsafe_allow_html=True)

kpi_html = f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">👥 População</div>
    <div class="kpi-value">{fmt_pop(pop) if pop else "N/D"}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">💰 PIB Municipal</div>
    <div class="kpi-value">{fmt_brl(pib) if pib else "N/D"}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">🏛️ Receita (RCL)</div>
    <div class="kpi-value">{fmt_brl(rcl) if rcl else "N/D"}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">📋 Total de Contratos</div>
    <div class="kpi-value">{total_c:,}</div>
    <div class="kpi-sub">{fmt_brl(total_v)}</div>
  </div>
  <div class="kpi-card highlight">
    <div class="kpi-label">🎭 Contratos Artísticos</div>
    <div class="kpi-value amber">{art_n:,}</div>
    <div class="kpi-sub">{fmt_brl(art_v)}</div>
  </div>
  <div class="kpi-card {'danger' if art_pct > 3 else ''}">
    <div class="kpi-label">👤 Gasto per capita</div>
    <div class="kpi-value pink">R$ {art_pc:.2f}</div>
    <div class="kpi-sub">em shows / habitante</div>
  </div>
  <div class="kpi-card {'danger' if art_pct > 3 else ''}">
    <div class="kpi-label">📊 % da Receita Municipal</div>
    <div class="kpi-value {'amber' if art_pct > 2 else 'green'}">{art_pct:.2f}%</div>
    <div class="kpi-sub">da RCL gasto em shows</div>
  </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)


# ─── NARRATIVA ───
st.markdown('<div class="section-header">📖 História Fiscal</div>', unsafe_allow_html=True)
narrativa = gerar_narrativa(stats, df, nome_sel)
st.markdown(f'<div class="narrative">{narrativa}</div>', unsafe_allow_html=True)


# ─── GRÁFICOS ───
st.markdown('<div class="section-header">📈 Visualizações</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])
with col1:
    if not cats.empty:
        st.plotly_chart(fig_categorias(cats, nome_sel), use_container_width=True, config={"displayModeBar": False})

with col2:
    if not sub.empty:
        fig_sub = fig_subcategorias_shows(sub)
        if fig_sub:
            st.plotly_chart(fig_sub, use_container_width=True, config={"displayModeBar": False})
    elif art_n == 0:
        st.markdown("""
        <div style="background:#1A1D27;border:1px solid #2A2D3E;border-radius:14px;
             padding:2rem;text-align:center;color:#7C7F9A;margin-top:1rem;">
          <div style="font-size:2rem">🎭</div>
          <div>Sem contratos artísticos neste período</div>
        </div>""", unsafe_allow_html=True)

# Ranking + Comparação
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig_ranking(summary, nome_sel), use_container_width=True, config={"displayModeBar": False})

with col4:
    st.plotly_chart(fig_comparacao_media(stats, summary, nome_sel), use_container_width=True, config={"displayModeBar": False})


# ─── COMPARTILHAMENTO ───
st.markdown('<div class="section-header">📤 Compartilhar</div>', unsafe_allow_html=True)

texto_share = build_share_text(stats, nome_sel)
st.markdown(f"""
<div style="background:#1A1D27;border:1px solid #2A2D3E;border-radius:12px;
     padding:1.2rem 1.5rem;font-family:'DM Mono',monospace;font-size:0.88rem;
     color:#E8EAF0;line-height:1.7;margin-bottom:1rem;">
{texto_share.replace(chr(10), '<br>')}
</div>
""", unsafe_allow_html=True)

share_buttons(texto_share)

# ─── BOTÃO IMAGEM ───
st.markdown("<br>", unsafe_allow_html=True)
if st.button("📸 Gerar card para compartilhar (PNG)"):
    img_bytes = generate_share_image(stats, nome_sel)
    if img_bytes:
        st.image(img_bytes, caption=f"Card — {nome_sel}")
        st.download_button(
            label="⬇️ Baixar imagem",
            data=img_bytes,
            file_name=f"fiscal_{nome_sel.lower().replace(' ','_')}.png",
            mime="image/png",
        )
    else:
        st.warning("Não foi possível gerar a imagem. Verifique se Pillow está instalado.")


# ─── RODAPÉ ───
st.markdown("""
<div style="margin-top:4rem;padding-top:2rem;border-top:1px solid #2A2D3E;
     text-align:center;color:#3A3D50;font-family:'DM Mono',monospace;font-size:0.72rem;
     line-height:2;">
  Dados: Portal Nacional de Contratações Públicas (PNCP) · IBGE · SICONFI — 2024/2026<br>
  Apenas contratos municipais válidos, excluídos outliers e contratos não-municipais.<br>
  Fiscal Storyteller BA · Dados abertos para transparência pública
</div>
""", unsafe_allow_html=True)

