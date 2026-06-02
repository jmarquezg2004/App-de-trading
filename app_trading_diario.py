import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, date
import requests
import time
 
# ══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Arkez Invest — Plataforma",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# CSS Premium
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');
 
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}
.stApp {
    background: #060a0f;
    color: #e8f4fd;
}
section[data-testid="stSidebar"] {
    background: #0d1520 !important;
    border-right: 1px solid #1e3048;
}
section[data-testid="stSidebar"] * { color: #e8f4fd !important; }
 
/* Metric cards */
[data-testid="metric-container"] {
    background: #0d1520;
    border: 1px solid #1e3048;
    border-radius: 10px;
    padding: 16px !important;
    position: relative;
    overflow: hidden;
}
[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00d4ff, #00ff88);
}
[data-testid="stMetricValue"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.5rem !important;
    color: #e8f4fd !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #4a6fa5 !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'IBM Plex Mono', monospace !important;
}
 
/* Tabs */
[data-testid="stTabs"] button {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #4a6fa5 !important;
    border-bottom: 2px solid transparent !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #00d4ff !important;
    border-bottom: 2px solid #00d4ff !important;
}
 
/* DataFrames */
[data-testid="stDataFrame"] {
    border: 1px solid #1e3048;
    border-radius: 8px;
    overflow: hidden;
}
 
/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] select {
    background: #0d1520 !important;
    border: 1px solid #1e3048 !important;
    color: #e8f4fd !important;
    font-family: 'IBM Plex Mono', monospace !important;
    border-radius: 6px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 1px #00d4ff !important;
}
 
/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #00d4ff, #008fb3) !important;
    color: #060a0f !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
.stButton button:hover {
    filter: brightness(1.1) !important;
    transform: translateY(-1px) !important;
}
 
/* Success/Error */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border-left-width: 3px !important;
    background: #0d1520 !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
 
/* Divider */
hr { border-color: #1e3048 !important; }
 
/* Headers */
h1, h2, h3 { color: #e8f4fd !important; }
h1 { font-family: 'IBM Plex Mono', monospace !important; color: #00d4ff !important; letter-spacing: 2px; }
h2 { font-family: 'IBM Plex Mono', monospace !important; font-size: 14px !important; letter-spacing: 1.5px; text-transform: uppercase; color: #4a6fa5 !important; }
h3 { font-family: 'IBM Plex Mono', monospace !important; font-size: 13px !important; color: #00d4ff !important; }
 
/* Badge styles via HTML */
.badge-accion   { background: rgba(0,212,255,.12); color: #00d4ff; border: 1px solid rgba(0,212,255,.25); padding: 2px 10px; border-radius: 20px; font-size: 10px; font-weight: 600; font-family: 'IBM Plex Mono', monospace; }
.badge-etf      { background: rgba(0,255,136,.12); color: #00ff88; border: 1px solid rgba(0,255,136,.25); padding: 2px 10px; border-radius: 20px; font-size: 10px; font-weight: 600; font-family: 'IBM Plex Mono', monospace; }
.badge-cripto   { background: rgba(255,107,53,.12); color: #ff6b35; border: 1px solid rgba(255,107,53,.25); padding: 2px 10px; border-radius: 20px; font-size: 10px; font-weight: 600; font-family: 'IBM Plex Mono', monospace; }
.badge-cdt      { background: rgba(255,204,0,.12);  color: #ffcc00; border: 1px solid rgba(255,204,0,.25);  padding: 2px 10px; border-radius: 20px; font-size: 10px; font-weight: 600; font-family: 'IBM Plex Mono', monospace; }
.kpi-label      { font-family: 'IBM Plex Mono', monospace; font-size: 9px; color: #4a6fa5; letter-spacing: 1.5px; text-transform: uppercase; }
 
/* Grid bg */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: linear-gradient(rgba(0,212,255,.02) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(0,212,255,.02) 1px, transparent 1px);
    background-size: 44px 44px;
    pointer-events: none;
    z-index: 0;
}
</style>
""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# CONSTANTES
# ══════════════════════════════════════════════════════════════
FIREBASE_KEY      = "AIzaSyC52gIJJRTE1B4BqeUwDmaX2fWKS3sSw10"
FIRESTORE_URL     = "https://firestore.googleapis.com/v1/projects/plataforma-de-inversiones/databases/(default)/documents"
ADMIN_EMAIL       = "jmarquezg2004@gmail.com"
CMC_API_KEY       = st.secrets.get("CMC_KEY", "d67913f039804c6b900905ebad7c1aaf")
 
CATEGORIAS        = ["Acción", "ETF", "Cripto", "CDT", "Fondo", "Cuenta Remunerada", "Otro"]
ESTRATEGIAS       = ["Spot", "Holding", "Futuros", "Staking", "Farming", "Arbitraje", "Bot/Copy Trading", "Launchpool", "ICO", "Renta Fija"]
RESULTADOS        = ["Abierta", "Ganadora", "Perdedora", "Cancelada"]
 
COLORS = {
    "accent":  "#00d4ff",
    "green":   "#00ff88",
    "orange":  "#ff6b35",
    "yellow":  "#ffcc00",
    "red":     "#ff4757",
    "muted":   "#4a6fa5",
    "bg":      "#060a0f",
    "surface": "#0d1520",
    "border":  "#1e3048",
}
 
# ══════════════════════════════════════════════════════════════
# FIREBASE AUTH
# ══════════════════════════════════════════════════════════════
def firebase_login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_KEY}"
    try:
        r = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True}, timeout=8)
        if r.status_code == 200:
            return True, r.json()
        return False, r.json().get("error", {}).get("message", "Error desconocido")
    except Exception as e:
        return False, f"Error de conexión: {e}"
 
# ══════════════════════════════════════════════════════════════
# FIRESTORE CRUD
# ══════════════════════════════════════════════════════════════
def fs_get(coleccion):
    try:
        r = requests.get(f"{FIRESTORE_URL}/{coleccion}", timeout=8)
        if r.status_code == 200 and "documents" in r.json():
            rows = []
            for doc in r.json()["documents"]:
                fields = doc.get("fields", {})
                row = {"_id": doc["name"].split("/")[-1]}
                for k, v in fields.items():
                    row[k] = list(v.values())[0]
                rows.append(row)
            return pd.DataFrame(rows)
    except Exception:
        pass
    return pd.DataFrame()
 
def fs_post(coleccion, datos):
    fields = {}
    for k, v in datos.items():
        if isinstance(v, (int, float)):
            fields[k] = {"doubleValue": float(v)}
        elif isinstance(v, bool):
            fields[k] = {"booleanValue": v}
        else:
            fields[k] = {"stringValue": str(v)}
    try:
        requests.post(f"{FIRESTORE_URL}/{coleccion}", json={"fields": fields}, timeout=8)
        return True
    except Exception:
        return False
 
def fs_patch(coleccion, doc_id, datos):
    fields = {}
    for k, v in datos.items():
        if isinstance(v, (int, float)):
            fields[k] = {"doubleValue": float(v)}
        else:
            fields[k] = {"stringValue": str(v)}
    mask = "&".join([f"updateMask.fieldPaths={k}" for k in datos.keys()])
    try:
        requests.patch(f"{FIRESTORE_URL}/{coleccion}/{doc_id}?{mask}", json={"fields": fields}, timeout=8)
        return True
    except Exception:
        return False
 
def fs_delete(coleccion, doc_id):
    try:
        requests.delete(f"{FIRESTORE_URL}/{coleccion}/{doc_id}", timeout=8)
        return True
    except Exception:
        return False
 
# ══════════════════════════════════════════════════════════════
# PRECIOS EN TIEMPO REAL
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=300)   # cache 5 minutos
def get_cmc_prices(symbols_tuple):
    """CoinMarketCap API — cripto. symbols_tuple para hashabilidad."""
    symbols = list(symbols_tuple)
    if not symbols:
        return {}
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    params = {"symbol": ",".join(symbols), "convert": "USD"}
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY, "Accept": "application/json"}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        if r.status_code != 200:
            return {}
        data = r.json().get("data", {})
        result = {}
        for sym, items in data.items():
            item = items[0] if isinstance(items, list) else items
            q = item.get("quote", {}).get("USD", {})
            result[sym.upper()] = {
                "price":  q.get("price", 0),
                "chg24":  q.get("percent_change_24h", 0),
                "chg7d":  q.get("percent_change_7d", 0),
                "mcap":   q.get("market_cap", 0),
                "name":   item.get("name", sym),
            }
        return result
    except Exception:
        return {}
 
@st.cache_data(ttl=300)
def get_stock_price(ticker):
    """Yahoo Finance para acciones y ETFs."""
    if not ticker:
        return None, 0
    try:
        import yfinance as yf
        t = yf.Ticker(ticker.upper())
        info = t.fast_info
        price = getattr(info, "last_price", None) or getattr(info, "previous_close", None)
        prev  = getattr(info, "previous_close", price) or price
        chg   = ((price - prev) / prev * 100) if (price and prev and prev != 0) else 0
        return float(price) if price else None, float(chg)
    except Exception:
        return None, 0
 
@st.cache_data(ttl=3600)
def get_trm():
    """TRM USD/COP via Yahoo Finance."""
    try:
        import yfinance as yf
        t = yf.Ticker("USDCOP=X")
        price = t.fast_info.last_price
        return float(price) if price else 4200.0
    except Exception:
        return 4200.0
 
def get_all_prices(df_ops):
    """Obtiene todos los precios necesarios de una vez."""
    prices = {}
    if df_ops.empty:
        return prices
 
    # Cripto via CMC
    cripto_tickers = df_ops[
        df_ops["Categoria"].isin(["Cripto"]) &
        df_ops["Ticker_API"].notna() &
        (df_ops["Ticker_API"].str.strip() != "")
    ]["Ticker_API"].str.upper().unique().tolist()
 
    if cripto_tickers:
        cmc = get_cmc_prices(tuple(cripto_tickers))
        prices.update(cmc)
 
    # Acciones y ETFs via Yahoo
    stock_rows = df_ops[
        df_ops["Categoria"].isin(["Acción", "ETF", "Fondo"]) &
        df_ops["Ticker_API"].notna() &
        (df_ops["Ticker_API"].str.strip() != "")
    ]
    for ticker in stock_rows["Ticker_API"].str.upper().unique():
        px, chg = get_stock_price(ticker)
        if px:
            prices[ticker] = {"price": px, "chg24": chg}
 
    return prices
 
# ══════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════════════
def cargar_datos():
    """Carga y normaliza aportes y operaciones desde Firestore."""
    # Aportes
    cols_a = ["_id", "Fondo", "Socio", "Cedula", "Fecha", "Tipo", "Monto"]
    df_a = fs_get("aportes")
    if df_a.empty:
        df_a = pd.DataFrame(columns=cols_a)
    else:
        for c in cols_a:
            if c not in df_a.columns:
                df_a[c] = None
        df_a["Monto"] = pd.to_numeric(df_a["Monto"], errors="coerce").fillna(0.0)
 
    # Operaciones
    cols_o = ["_id", "ID", "Fondo", "Fecha", "Activo", "Categoria", "Estrategia",
              "Broker", "Valor_Pos", "TP_pct", "SL_pct", "TP_usd", "SL_usd",
              "Comision", "Resultado", "Ticker_API", "Precio_Entrada", "Cantidad",
              "TEA", "Notas"]
    df_o = fs_get("operaciones")
    if df_o.empty:
        df_o = pd.DataFrame(columns=cols_o)
    else:
        for c in cols_o:
            if c not in df_o.columns:
                df_o[c] = None
        for col in ["ID", "Valor_Pos", "TP_pct", "SL_pct", "TP_usd", "SL_usd",
                    "Comision", "Precio_Entrada", "Cantidad", "TEA"]:
            df_o[col] = pd.to_numeric(df_o[col], errors="coerce").fillna(0.0)
 
    return df_a, df_o
 
# ══════════════════════════════════════════════════════════════
# CÁLCULOS FINANCIEROS
# ══════════════════════════════════════════════════════════════
def calcular_pnl_op(row):
    """P&L de una operación cerrada."""
    if row.get("Resultado") == "Ganadora":
        return float(row.get("TP_usd", 0)) - float(row.get("Comision", 0))
    elif row.get("Resultado") == "Perdedora":
        return -float(row.get("SL_usd", 0)) - float(row.get("Comision", 0))
    return 0.0
 
def valor_actual_posicion(row, prices):
    """Valor actual de una posición abierta usando precios en tiempo real."""
    ticker = str(row.get("Ticker_API", "")).strip().upper()
    cat    = str(row.get("Categoria", ""))
    p_entrada = float(row.get("Precio_Entrada", 0) or 0)
    cantidad  = float(row.get("Cantidad", 0) or 0)
    valor_pos = float(row.get("Valor_Pos", 0) or 0)
    tea       = float(row.get("TEA", 0) or 0)
 
    if cat in ["CDT", "Cuenta Remunerada"] and tea > 0:
        # TEA compuesta desde fecha de entrada
        try:
            fecha_entrada = pd.to_datetime(row.get("Fecha"))
            dias = (pd.Timestamp.now() - fecha_entrada).days
            valor_actual = valor_pos * ((1 + tea) ** (dias / 365))
            return valor_actual, valor_actual - valor_pos, (valor_actual - valor_pos) / valor_pos * 100 if valor_pos else 0
        except Exception:
            return valor_pos, 0, 0
 
    if ticker and ticker in prices:
        px_actual = prices[ticker]["price"]
        if p_entrada > 0 and cantidad > 0:
            valor_actual = px_actual * cantidad
            gp           = valor_actual - (p_entrada * cantidad)
            gp_pct       = gp / (p_entrada * cantidad) * 100
            return valor_actual, gp, gp_pct
        elif valor_pos > 0 and p_entrada > 0:
            factor      = px_actual / p_entrada
            valor_actual = valor_pos * factor
            gp           = valor_actual - valor_pos
            gp_pct       = gp / valor_pos * 100
            return valor_actual, gp, gp_pct
 
    return valor_pos, 0.0, 0.0
 
# ══════════════════════════════════════════════════════════════
# CHARTS PLOTLY
# ══════════════════════════════════════════════════════════════
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Mono, monospace", color="#e8f4fd", size=11),
    margin=dict(l=0, r=0, t=30, b=0),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1e3048", borderwidth=1),
    xaxis=dict(gridcolor="#1e3048", linecolor="#1e3048", tickfont=dict(size=10)),
    yaxis=dict(gridcolor="#1e3048", linecolor="#1e3048", tickfont=dict(size=10)),
)
 
def chart_distribucion(df_ops_fondo):
    """Donut de distribución por categoría."""
    if df_ops_fondo.empty:
        return None
    dist = df_ops_fondo.groupby("Categoria")["Valor_Pos"].sum().reset_index()
    dist = dist[dist["Valor_Pos"] > 0]
    if dist.empty:
        return None
    colors = {"Acción":"#00d4ff","ETF":"#00ff88","Cripto":"#ff6b35",
              "CDT":"#ffcc00","Fondo":"#a855f7","Cuenta Remunerada":"#f59e0b","Otro":"#4a6fa5"}
    fig = go.Figure(go.Pie(
        labels=dist["Categoria"], values=dist["Valor_Pos"],
        hole=0.6,
        marker=dict(colors=[colors.get(c,"#4a6fa5") for c in dist["Categoria"]],
                    line=dict(color="#060a0f", width=2)),
        textfont=dict(family="IBM Plex Mono", size=11),
        hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>"
    ))
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text="Distribución por tipo", font=dict(size=11, color="#4a6fa5"), x=0.5))
    return fig
 
def chart_evolucion_capital(df_aportes_fondo):
    """Línea de evolución del capital aportado."""
    if df_aportes_fondo.empty:
        return None
    df = df_aportes_fondo.copy()
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    df = df.dropna(subset=["Fecha"]).sort_values("Fecha")
    df["Monto_signed"] = df.apply(lambda r: r["Monto"] if r["Tipo"]=="Aporte" else -r["Monto"], axis=1)
    df["Capital_acum"] = df["Monto_signed"].cumsum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Fecha"], y=df["Capital_acum"],
        mode="lines+markers",
        line=dict(color="#00d4ff", width=2),
        fill="tozeroy", fillcolor="rgba(0,212,255,0.07)",
        marker=dict(color="#00d4ff", size=5),
        name="Capital",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>$%{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text="Evolución capital aportado", font=dict(size=11, color="#4a6fa5"), x=0.5))
    return fig
 
def chart_pnl_barras(df_ops_cerradas):
    """Barras de P&L por operación."""
    if df_ops_cerradas.empty:
        return None
    df = df_ops_cerradas.copy()
    df["PnL"] = df.apply(calcular_pnl_op, axis=1)
    df["Color"] = df["PnL"].apply(lambda x: "#00ff88" if x >= 0 else "#ff4757")
    df["Label"] = df.apply(lambda r: f"{r.get('Activo','?')} ({r.get('Fecha','?')})", axis=1)
    fig = go.Figure(go.Bar(
        x=df["Label"], y=df["PnL"],
        marker_color=df["Color"],
        hovertemplate="<b>%{x}</b><br>P&L: $%{y:,.2f}<extra></extra>",
        text=df["PnL"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside",
        textfont=dict(size=10)
    ))
    fig.update_layout(**PLOTLY_LAYOUT,
        title=dict(text="P&L por operación cerrada", font=dict(size=11, color="#4a6fa5"), x=0.5),
        yaxis_title="USD")
    return fig
 
def chart_posiciones_abiertas(filas_abiertas):
    """Barras horizontales de valor actual de posiciones abiertas."""
    if not filas_abiertas:
        return None
    labels = [r["Activo"] for r in filas_abiertas]
    vals   = [r["Valor_Actual"] for r in filas_abiertas]
    gps    = [r["GP_pct"] for r in filas_abiertas]
    colors = ["#00ff88" if g >= 0 else "#ff4757" for g in gps]
    fig = go.Figure(go.Bar(
        y=labels, x=vals, orientation="h",
        marker_color=["#00d4ff"] * len(labels),
        hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(**PLOTLY_LAYOUT,
        title=dict(text="Valor actual posiciones abiertas", font=dict(size=11, color="#4a6fa5"), x=0.5),
        xaxis_title="USD", height=max(200, len(labels)*40))
    return fig
 
# ══════════════════════════════════════════════════════════════
# HELPERS UI
# ══════════════════════════════════════════════════════════════
def metric_card(label, value, delta=None, prefix="$"):
    val_str = f"{prefix}{value:,.2f}" if isinstance(value, (int, float)) else str(value)
    delta_html = ""
    if delta is not None:
        clr = "#00ff88" if delta >= 0 else "#ff4757"
        sign = "▲" if delta >= 0 else "▼"
        delta_html = f'<div style="font-family:IBM Plex Mono;font-size:11px;color:{clr}">{sign} {abs(delta):.2f}%</div>'
    return f"""
    <div style="background:#0d1520;border:1px solid #1e3048;border-radius:10px;padding:16px;position:relative;overflow:hidden">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#00d4ff,#00ff88)"></div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px">{label}</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:22px;font-weight:600;color:#e8f4fd;line-height:1">{val_str}</div>
      {delta_html}
    </div>"""
 
def price_badge(price, chg):
    clr = "#00ff88" if chg >= 0 else "#ff4757"
    sign = "+" if chg >= 0 else ""
    return f'<span style="font-family:IBM Plex Mono;font-size:12px;color:#e8f4fd">${price:,.4f}</span> <span style="font-size:10px;color:{clr}">{sign}{chg:.2f}%</span>'
 
# ══════════════════════════════════════════════════════════════
# LOGIN SCREEN
# ══════════════════════════════════════════════════════════════
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
 
if not st.session_state.logged_in:
    st.markdown("""
    <div style="text-align:center;padding:40px 0 20px">
      <div style="display:inline-block;width:48px;height:48px;background:linear-gradient(135deg,#00d4ff,#00ff88);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);margin-bottom:16px"></div>
      <h1 style="font-family:'IBM Plex Mono',monospace;font-size:24px;color:#00d4ff;letter-spacing:3px;margin:0">ARKEZ INVEST</h1>
      <p style="color:#4a6fa5;font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:2px;margin:8px 0 0">PLATAFORMA DE INVERSIONES · ACCESO PRIVADO</p>
    </div>
    """, unsafe_allow_html=True)
 
    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown('<div style="background:#0d1520;border:1px solid #1e3048;border-radius:14px;padding:28px">', unsafe_allow_html=True)
        email = st.text_input("📧 Correo electrónico", key="login_email", placeholder="usuario@email.com")
        pwd   = st.text_input("🔒 Contraseña", type="password", key="login_pwd")
 
        if st.button("ENTRAR →", use_container_width=True):
            if email and pwd:
                with st.spinner("Verificando credenciales…"):
                    ok, result = firebase_login(email, pwd)
                if ok:
                    rol = "admin" if email.strip().lower() == ADMIN_EMAIL.lower() else "cliente"
                    st.session_state.update({
                        "logged_in": True, "usuario": email.strip().lower(),
                        "rol": rol, "fondo_sel": "Arkez Invest"
                    })
                    st.success(f"Bienvenido — Rol: {rol.upper()}")
                    time.sleep(0.8)
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
            else:
                st.warning("Completa todos los campos")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()
 
# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:16px 0 12px">
      <div style="display:inline-block;width:32px;height:32px;background:linear-gradient(135deg,#00d4ff,#00ff88);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);margin-bottom:8px"></div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:13px;font-weight:600;color:#00d4ff;letter-spacing:2px">ARKEZ INVEST</div>
    </div>
    """, unsafe_allow_html=True)
 
    rol     = st.session_state.rol
    usuario = st.session_state.usuario
 
    st.markdown(f"""
    <div style="background:#111d2e;border:1px solid #1e3048;border-radius:8px;padding:10px 12px;margin-bottom:12px">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5;letter-spacing:1px">USUARIO</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#e8f4fd;overflow:hidden;text-overflow:ellipsis">{usuario}</div>
      <div style="margin-top:4px">
        <span style="background:{'rgba(0,212,255,.12)' if rol=='admin' else 'rgba(0,255,136,.12)'};
                     color:{'#00d4ff' if rol=='admin' else '#00ff88'};
                     border:1px solid {'rgba(0,212,255,.25)' if rol=='admin' else 'rgba(0,255,136,.25)'};
                     padding:1px 8px;border-radius:20px;font-family:'IBM Plex Mono',monospace;font-size:9px;font-weight:600">
          {'⬡ ADMIN' if rol=='admin' else '● CLIENTE'}
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)
 
    # Cargar datos
    df_aportes, df_ops = cargar_datos()
 
    # Selección de fondo
    fondos_list = sorted(set(
        list(df_aportes["Fondo"].dropna().unique()) +
        list(df_ops["Fondo"].dropna().unique())
    )) or ["Arkez Invest"]
    if "Arkez Invest" not in fondos_list:
        fondos_list.insert(0, "Arkez Invest")
 
    if rol == "admin":
        fondo = st.selectbox("🏦 Fondo activo", fondos_list,
                             index=fondos_list.index(st.session_state.get("fondo_sel","Arkez Invest"))
                             if st.session_state.get("fondo_sel","Arkez Invest") in fondos_list else 0)
        st.session_state.fondo_sel = fondo
 
        with st.expander("➕ Crear fondo"):
            nuevo = st.text_input("Nombre del fondo", key="nuevo_fondo")
            if st.button("Crear", key="btn_crear_fondo"):
                if nuevo.strip() and nuevo not in fondos_list:
                    fs_post("aportes", {"Fondo": nuevo, "Socio": usuario, "Cedula": "",
                                        "Fecha": str(date.today()), "Tipo": "Aporte", "Monto": 0.0})
                    st.success(f"✓ Fondo '{nuevo}' creado")
                    st.rerun()
    else:
        # Cliente: solo ve su fondo (asignado por email)
        fondo = st.session_state.get("fondo_sel", fondos_list[0])
        st.markdown(f'<div style="font-family:IBM Plex Mono;font-size:11px;color:#4a6fa5">Fondo: <span style="color:#e8f4fd">{fondo}</span></div>', unsafe_allow_html=True)
 
    # TRM
    trm = get_trm()
    st.markdown(f"""
    <div style="background:#111d2e;border:1px solid #1e3048;border-radius:8px;padding:8px 12px;margin-top:12px">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5;letter-spacing:1px">TRM USD/COP</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:14px;color:#ffcc00;font-weight:600">${trm:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
 
    moneda_display = st.radio("Moneda", ["USD", "COP"], horizontal=True)
    factor_moneda  = trm if moneda_display == "COP" else 1.0
    sfx            = " COP" if moneda_display == "COP" else " USD"
 
    st.markdown("---")
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        for k in ["logged_in","usuario","rol","fondo_sel"]:
            st.session_state.pop(k, None)
        st.rerun()
 
# ══════════════════════════════════════════════════════════════
# FILTRAR POR FONDO
# ══════════════════════════════════════════════════════════════
df_ap_f  = df_aportes[df_aportes["Fondo"] == fondo].copy() if not df_aportes.empty else pd.DataFrame()
df_ops_f = df_ops[df_ops["Fondo"] == fondo].copy() if not df_ops.empty else pd.DataFrame()
 
# Precios en tiempo real
prices = get_all_prices(df_ops_f) if not df_ops_f.empty else {}
 
# Calcular métricas globales
capital_neto = df_ap_f["Monto"].sum() if not df_ap_f.empty else 0
 
ops_cerradas = df_ops_f[df_ops_f["Resultado"].isin(["Ganadora","Perdedora"])].copy() if not df_ops_f.empty else pd.DataFrame()
ops_abiertas = df_ops_f[df_ops_f["Resultado"] == "Abierta"].copy() if not df_ops_f.empty else pd.DataFrame()
 
pnl_cerradas = 0
if not ops_cerradas.empty:
    ops_cerradas["PnL"] = ops_cerradas.apply(calcular_pnl_op, axis=1)
    pnl_cerradas = ops_cerradas["PnL"].sum()
 
# Posiciones abiertas con valorización actual
filas_abiertas = []
valor_abierto  = 0
pnl_abierto    = 0
 
if not ops_abiertas.empty:
    for _, row in ops_abiertas.iterrows():
        val, gp, gp_pct = valor_actual_posicion(row, prices)
        valor_abierto += val
        pnl_abierto   += gp
        filas_abiertas.append({
            "Activo":       row.get("Activo","—"),
            "Categoria":    row.get("Categoria","—"),
            "Ticker":       row.get("Ticker_API","—"),
            "Valor_Entrada":float(row.get("Valor_Pos",0)),
            "Valor_Actual": val,
            "GP_usd":       gp,
            "GP_pct":       gp_pct,
            "Fecha":        row.get("Fecha","—"),
            "_id":          row.get("_id",""),
        })
 
total_gp  = pnl_cerradas + pnl_abierto
patrimonio= capital_neto + total_gp
rend_pct  = (total_gp / capital_neto * 100) if capital_neto > 0 else 0
 
win_rate  = 0
if not ops_cerradas.empty:
    ganadoras = (ops_cerradas["Resultado"] == "Ganadora").sum()
    total_c   = len(ops_cerradas)
    win_rate  = ganadoras / total_c * 100 if total_c else 0
 
# ══════════════════════════════════════════════════════════════
# HEADER PRINCIPAL
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="display:flex;align-items:center;gap:16px;margin-bottom:4px">
  <div style="width:36px;height:36px;background:linear-gradient(135deg,#00d4ff,#00ff88);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%)"></div>
  <div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:18px;font-weight:600;color:#00d4ff;letter-spacing:2px">{fondo.upper()}</div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#4a6fa5;letter-spacing:1px">PORTAFOLIO DE INVERSIONES · TIEMPO REAL</div>
  </div>
  <div style="margin-left:auto;font-family:'IBM Plex Mono',monospace;font-size:10px;color:#4a6fa5">
    Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}
  </div>
</div>
<hr style="border-color:#1e3048;margin:12px 0 20px">
""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# KPI ROW
# ══════════════════════════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)
 
with k1:
    st.markdown(metric_card("Patrimonio Total",
        patrimonio * factor_moneda, prefix="$"), unsafe_allow_html=True)
with k2:
    st.markdown(metric_card("Capital Aportado",
        capital_neto * factor_moneda, prefix="$"), unsafe_allow_html=True)
with k3:
    gp_color = "#00ff88" if total_gp >= 0 else "#ff4757"
    st.markdown(f"""
    <div style="background:#0d1520;border:1px solid #1e3048;border-radius:10px;padding:16px;position:relative;overflow:hidden">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;background:{'#00ff88' if total_gp>=0 else '#ff4757'}"></div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px">Ganancia / Pérdida</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:22px;font-weight:600;color:{gp_color};line-height:1">
        {'+'if total_gp>=0 else ''}${total_gp*factor_moneda:,.2f}
      </div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:{gp_color}">
        {'▲' if rend_pct>=0 else '▼'} {abs(rend_pct):.2f}%
      </div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(metric_card("Posiciones Abiertas",
        valor_abierto * factor_moneda, prefix="$"), unsafe_allow_html=True)
with k5:
    st.markdown(f"""
    <div style="background:#0d1520;border:1px solid #1e3048;border-radius:10px;padding:16px;position:relative;overflow:hidden">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;background:#a855f7"></div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px">Win Rate</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:22px;font-weight:600;color:#a855f7;line-height:1">{win_rate:.1f}%</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#4a6fa5">{len(ops_cerradas)} ops cerradas</div>
    </div>""", unsafe_allow_html=True)
 
st.markdown("<br>", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# TABS PRINCIPALES
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    tabs = st.tabs(["⬡ Dashboard", "◈ Posiciones", "📌 Registrar Op.", "💰 Socios", "📊 Análisis", "⚙ Admin"])
    tab_dash, tab_pos, tab_reg, tab_soc, tab_anal, tab_adm = tabs
else:
    tabs = st.tabs(["⬡ Dashboard", "◈ Posiciones", "📊 Análisis"])
    tab_dash, tab_pos, tab_anal = tabs
 
# ══════════════════════════════════════════════════════════════
# TAB 1: DASHBOARD
# ══════════════════════════════════════════════════════════════
with tab_dash:
    c_left, c_right = st.columns([3, 2])
 
    with c_left:
        fig_ev = chart_evolucion_capital(df_ap_f)
        if fig_ev:
            st.plotly_chart(fig_ev, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Sin movimientos de capital registrados aún.")
 
    with c_right:
        fig_dist = chart_distribucion(df_ops_f)
        if fig_dist:
            st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Sin operaciones registradas aún.")
 
    # Precios en tiempo real
    if prices:
        st.markdown("## Precios en tiempo real")
        cols_px = st.columns(min(len(prices), 5))
        for i, (ticker, data) in enumerate(list(prices.items())[:10]):
            col = cols_px[i % min(len(prices), 5)]
            with col:
                chg  = data.get("chg24", 0)
                clr  = "#00ff88" if chg >= 0 else "#ff4757"
                sign = "▲" if chg >= 0 else "▼"
                st.markdown(f"""
                <div style="background:#0d1520;border:1px solid #1e3048;border-radius:8px;padding:12px;text-align:center">
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;color:#00d4ff">{ticker}</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:600;color:#e8f4fd;margin:4px 0">${data['price']:,.4f if data['price']<10 else data['price']:,.2f}</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:{clr}">{sign} {abs(chg):.2f}%</div>
                </div>""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# TAB 2: POSICIONES
# ══════════════════════════════════════════════════════════════
with tab_pos:
    # Posiciones abiertas valoradas
    if filas_abiertas:
        st.markdown("## Posiciones abiertas")
        for row in filas_abiertas:
            gp_clr  = "#00ff88" if row["GP_usd"] >= 0 else "#ff4757"
            gp_sign = "+" if row["GP_usd"] >= 0 else ""
            px_info = prices.get(row["Ticker"].upper(), {})
            px_str  = f"${px_info.get('price',0):,.4f}" if px_info else "—"
 
            st.markdown(f"""
            <div style="background:#0d1520;border:1px solid #1e3048;border-radius:10px;padding:16px;margin-bottom:10px;display:flex;align-items:center;gap:20px;flex-wrap:wrap">
              <div style="min-width:120px">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:14px;font-weight:600;color:#00d4ff">{row['Activo']}</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#4a6fa5">{row['Ticker']} · {row['Categoria']}</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5;letter-spacing:1px">PRECIO ACTUAL</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:13px;color:#e8f4fd">{px_str}</div>
              </div>
              <div style="text-align:center;min-width:110px">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5;letter-spacing:1px">VALOR ENTRADA</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:13px;color:#e8f4fd">${row['Valor_Entrada']*factor_moneda:,.2f}</div>
              </div>
              <div style="text-align:center;min-width:110px">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5;letter-spacing:1px">VALOR ACTUAL</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:13px;font-weight:600;color:#e8f4fd">${row['Valor_Actual']*factor_moneda:,.2f}</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5;letter-spacing:1px">G/P</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:14px;font-weight:600;color:{gp_clr}">{gp_sign}${row['GP_usd']*factor_moneda:,.2f}</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:{gp_clr}">{gp_sign}{row['GP_pct']:.2f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)
 
        fig_pos = chart_posiciones_abiertas(filas_abiertas)
        if fig_pos:
            st.plotly_chart(fig_pos, use_container_width=True, config={"displayModeBar":False})
    else:
        st.info("Sin posiciones abiertas actualmente.")
 
    # Historial de operaciones
    if not df_ops_f.empty:
        st.markdown("## Historial de operaciones")
        df_show = df_ops_f[["Fecha","Activo","Categoria","Estrategia","Broker",
                              "Valor_Pos","TP_pct","SL_pct","Resultado","Ticker_API"]].copy()
        df_show["Valor_Pos"] = df_show["Valor_Pos"] * factor_moneda
 
        def color_resultado(val):
            if val == "Ganadora":  return "color: #00ff88; font-weight: 600"
            if val == "Perdedora": return "color: #ff4757; font-weight: 600"
            if val == "Abierta":   return "color: #00d4ff"
            return ""
 
        st.dataframe(
            df_show.sort_values("Fecha", ascending=False).style
                .applymap(color_resultado, subset=["Resultado"])
                .format({"Valor_Pos": "${:,.2f}", "TP_pct": "{:.1f}%", "SL_pct": "{:.1f}%"}),
            use_container_width=True, hide_index=True
        )
 
# ══════════════════════════════════════════════════════════════
# TAB 3: REGISTRAR OPERACIÓN (solo admin)
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    with tab_reg:
        st.markdown("## Registrar nueva operación")
 
        with st.form("form_op", clear_on_submit=True):
            r1c1, r1c2, r1c3, r1c4 = st.columns(4)
            fecha_op  = r1c1.date_input("Fecha", value=date.today())
            activo    = r1c2.text_input("Nombre del activo", placeholder="Bitcoin, Nubank, VTI…")
            categoria = r1c3.selectbox("Categoría", CATEGORIAS)
            estrategia= r1c4.selectbox("Estrategia", ESTRATEGIAS)
 
            r2c1, r2c2, r2c3 = st.columns(3)
            broker    = r2c1.text_input("Broker / Exchange")
            valor_pos = r2c2.number_input("Valor posición USD", min_value=0.0, step=0.01)
            comision  = r2c3.number_input("Comisión USD", min_value=0.0, step=0.01)
 
            r3c1, r3c2, r3c3, r3c4 = st.columns(4)
            precio_entrada = r3c1.number_input("Precio entrada", min_value=0.0, step=0.0001, format="%.4f")
            cantidad       = r3c2.number_input("Cantidad / Unidades", min_value=0.0, step=0.000001, format="%.6f")
            tp_pct         = r3c3.number_input("TP %", min_value=0.0, step=0.1)
            sl_pct         = r3c4.number_input("SL %", min_value=0.0, step=0.1)
 
            r4c1, r4c2, r4c3 = st.columns(3)
            resultado  = r4c1.selectbox("Resultado", RESULTADOS)
            ticker_api = r4c2.text_input("Ticker API", placeholder="BTC (CMC) · AAPL (Yahoo) · VTI")
            tea_pct    = r4c3.number_input("TEA % anual (CDT/Rem.)", min_value=0.0, max_value=100.0, step=0.01,
                                            help="Solo para CDT o Cuenta Remunerada. Ej: 12.85")
            notas = st.text_area("Notas", height=60)
 
            tp_usd = valor_pos * tp_pct / 100
            sl_usd = valor_pos * sl_pct / 100
 
            if st.form_submit_button("💾 Guardar operación", use_container_width=True):
                if not activo.strip():
                    st.error("El nombre del activo es obligatorio")
                else:
                    new_id = float(df_ops["ID"].max() + 1) if not df_ops.empty and df_ops["ID"].max() > 0 else 1.0
                    ok = fs_post("operaciones", {
                        "ID": new_id, "Fondo": fondo, "Fecha": str(fecha_op),
                        "Activo": activo, "Categoria": categoria, "Estrategia": estrategia,
                        "Broker": broker, "Valor_Pos": valor_pos, "TP_pct": tp_pct,
                        "SL_pct": sl_pct, "TP_usd": tp_usd, "SL_usd": sl_usd,
                        "Comision": comision, "Resultado": resultado,
                        "Ticker_API": ticker_api.strip().upper(),
                        "Precio_Entrada": precio_entrada, "Cantidad": cantidad,
                        "TEA": tea_pct / 100 if tea_pct > 0 else 0.0,
                        "Notas": notas
                    })
                    if ok:
                        st.success("✓ Operación guardada correctamente")
                        st.cache_data.clear()
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Error guardando en Firestore")
 
        # Editar / Eliminar operaciones
        if not df_ops_f.empty:
            st.markdown("---")
            st.markdown("## Gestionar operaciones existentes")
 
            op_ids = df_ops_f["_id"].tolist()
            op_labels = [f"{r['Fecha']} — {r['Activo']} ({r['Resultado']})" for _, r in df_ops_f.iterrows()]
            sel_idx = st.selectbox("Selecciona operación", range(len(op_labels)), format_func=lambda i: op_labels[i])
 
            if sel_idx is not None:
                sel_row = df_ops_f.iloc[sel_idx]
                c_edit1, c_edit2 = st.columns(2)
 
                with c_edit1:
                    nuevo_resultado = st.selectbox("Cambiar resultado", RESULTADOS,
                                                    index=RESULTADOS.index(sel_row.get("Resultado","Abierta"))
                                                    if sel_row.get("Resultado") in RESULTADOS else 0)
                    if st.button("✏️ Actualizar resultado"):
                        fs_patch("operaciones", sel_row["_id"], {"Resultado": nuevo_resultado})
                        st.success("✓ Resultado actualizado")
                        st.cache_data.clear()
                        st.rerun()
 
                with c_edit2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🗑 Eliminar operación", type="secondary"):
                        fs_delete("operaciones", sel_row["_id"])
                        st.success("✓ Operación eliminada")
                        st.cache_data.clear()
                        st.rerun()
 
# ══════════════════════════════════════════════════════════════
# TAB 4: SOCIOS (solo admin)
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    with tab_soc:
        st.markdown("## Movimientos de capital — Socios")
 
        with st.form("form_aporte", clear_on_submit=True):
            c1, c2, c3, c4 = st.columns(4)
            socio  = c1.text_input("Nombre del socio")
            cedula = c2.text_input("Cédula / ID")
            tipo   = c3.selectbox("Tipo", ["Aporte", "Retiro"])
            monto  = c4.number_input("Monto (USD)", min_value=0.01, step=0.01)
            fecha_a= st.date_input("Fecha movimiento", value=date.today())
 
            if st.form_submit_button("💾 Guardar movimiento", use_container_width=True):
                if not socio.strip():
                    st.error("El nombre del socio es obligatorio")
                else:
                    ok = fs_post("aportes", {
                        "Fondo": fondo, "Socio": socio, "Cedula": cedula,
                        "Fecha": str(fecha_a), "Tipo": tipo, "Monto": monto
                    })
                    if ok:
                        st.success("✓ Movimiento guardado")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Error guardando")
 
        if not df_ap_f.empty:
            # Tabla de socios
            st.markdown("---")
            st.markdown("## Resumen por socio")
            if "Socio" in df_ap_f.columns:
                resumen = df_ap_f.groupby(["Socio","Cedula"]).apply(
                    lambda g: pd.Series({
                        "Total Aportes": g[g["Tipo"]=="Aporte"]["Monto"].sum(),
                        "Total Retiros": g[g["Tipo"]=="Retiro"]["Monto"].sum(),
                        "Neto":          g.apply(lambda r: r["Monto"] if r["Tipo"]=="Aporte" else -r["Monto"], axis=1).sum(),
                    })
                ).reset_index()
                resumen["% del Fondo"] = (resumen["Neto"] / resumen["Neto"].sum() * 100).round(2)
                st.dataframe(resumen.style.format({
                    "Total Aportes":"${:,.2f}","Total Retiros":"${:,.2f}",
                    "Neto":"${:,.2f}","% del Fondo":"{:.2f}%"
                }), use_container_width=True, hide_index=True)
 
            st.markdown("## Historial completo")
            df_hist = df_ap_f.sort_values("Fecha", ascending=False)
            st.dataframe(
                df_hist[["Fecha","Socio","Cedula","Tipo","Monto"]].style
                    .applymap(lambda v: "color:#00ff88;font-weight:600" if v=="Aporte" else
                               "color:#ff4757;font-weight:600" if v=="Retiro" else "", subset=["Tipo"])
                    .format({"Monto":"${:,.2f}"}),
                use_container_width=True, hide_index=True
            )
 
            if st.button("🗑 Eliminar último movimiento"):
                last_id = df_ap_f.sort_values("Fecha").iloc[-1]["_id"]
                fs_delete("aportes", last_id)
                st.cache_data.clear()
                st.rerun()
 
# ══════════════════════════════════════════════════════════════
# TAB 5: ANÁLISIS
# ══════════════════════════════════════════════════════════════
with tab_anal:
    st.markdown("## Análisis de rendimiento")
 
    if not ops_cerradas.empty:
        c_anal1, c_anal2 = st.columns([3,2])
 
        with c_anal1:
            fig_pnl = chart_pnl_barras(ops_cerradas)
            if fig_pnl:
                st.plotly_chart(fig_pnl, use_container_width=True, config={"displayModeBar":False})
 
        with c_anal2:
            # Estadísticas
            pnl_vals      = ops_cerradas["PnL"]
            mejor_op      = ops_cerradas.loc[pnl_vals.idxmax()]
            peor_op       = ops_cerradas.loc[pnl_vals.idxmin()]
            avg_ganadora  = pnl_vals[pnl_vals > 0].mean() if (pnl_vals > 0).any() else 0
            avg_perdedora = pnl_vals[pnl_vals < 0].mean() if (pnl_vals < 0).any() else 0
            profit_factor = abs(pnl_vals[pnl_vals>0].sum() / pnl_vals[pnl_vals<0].sum()) if (pnl_vals<0).any() else float('inf')
 
            st.markdown(f"""
            <div style="background:#0d1520;border:1px solid #1e3048;border-radius:10px;padding:16px;margin-bottom:10px">
              <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px">Estadísticas</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
                <div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5">WIN RATE</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:16px;color:#a855f7;font-weight:600">{win_rate:.1f}%</div>
                </div>
                <div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5">PROFIT FACTOR</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:16px;color:#00d4ff;font-weight:600">{profit_factor:.2f}x</div>
                </div>
                <div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5">AVG GANADORA</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:14px;color:#00ff88;font-weight:600">+${avg_ganadora:,.2f}</div>
                </div>
                <div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5">AVG PERDEDORA</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:14px;color:#ff4757;font-weight:600">${avg_perdedora:,.2f}</div>
                </div>
                <div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5">MEJOR OP</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#00ff88">{mejor_op.get('Activo','?')}</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#00ff88">+${mejor_op['PnL']:,.2f}</div>
                </div>
                <div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#4a6fa5">PEOR OP</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#ff4757">{peor_op.get('Activo','?')}</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#ff4757">${peor_op['PnL']:,.2f}</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)
 
        # PnL por categoría
        st.markdown("## P&L por categoría")
        cat_pnl = ops_cerradas.groupby("Categoria")["PnL"].agg(["sum","count","mean"]).reset_index()
        cat_pnl.columns = ["Categoría","P&L Total","# Ops","P&L Promedio"]
        fig_cat = px.bar(cat_pnl, x="Categoría", y="P&L Total",
            color="P&L Total",
            color_continuous_scale=[[0,"#ff4757"],[0.5,"#ffcc00"],[1,"#00ff88"]],
            text="P&L Total",
            template="plotly_dark")
        fig_cat.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig_cat.update_layout(**PLOTLY_LAYOUT,
            title=dict(text="P&L por categoría", font=dict(size=11,color="#4a6fa5"),x=0.5),
            coloraxis_showscale=False)
        st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar":False})
 
    else:
        st.info("Aún no hay operaciones cerradas para analizar.")
 
    # Distribución de capital actual
    if not df_ops_f.empty:
        st.markdown("## Distribución actual del portafolio")
        c_d1, c_d2 = st.columns(2)
        with c_d1:
            fig_d = chart_distribucion(df_ops_f)
            if fig_d:
                st.plotly_chart(fig_d, use_container_width=True, config={"displayModeBar":False})
        with c_d2:
            fig_est = px.pie(
                df_ops_f.groupby("Estrategia")["Valor_Pos"].sum().reset_index(),
                names="Estrategia", values="Valor_Pos",
                hole=0.55, template="plotly_dark",
                color_discrete_sequence=["#00d4ff","#00ff88","#ff6b35","#ffcc00","#a855f7","#ff4757","#4a6fa5"]
            )
            fig_est.update_layout(**PLOTLY_LAYOUT,
                title=dict(text="Distribución por estrategia", font=dict(size=11,color="#4a6fa5"),x=0.5))
            st.plotly_chart(fig_est, use_container_width=True, config={"displayModeBar":False})
 
# ══════════════════════════════════════════════════════════════
# TAB 6: ADMIN
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    with tab_adm:
        st.markdown("## Panel de administración")
 
        col_a1, col_a2 = st.columns(2)
 
        with col_a1:
            st.markdown("### Resumen global de fondos")
            if not df_aportes.empty or not df_ops.empty:
                fondos_res = {}
                for f in fondos_list:
                    ap_f  = df_aportes[df_aportes["Fondo"]==f]["Monto"].sum() if not df_aportes.empty else 0
                    ops_f2= df_ops[df_ops["Fondo"]==f] if not df_ops.empty else pd.DataFrame()
                    n_ops = len(ops_f2)
                    fondos_res[f] = {"Capital": ap_f, "# Ops": n_ops}
 
                df_res = pd.DataFrame(fondos_res).T.reset_index()
                df_res.columns = ["Fondo","Capital Aportado","# Operaciones"]
                st.dataframe(df_res.style.format({"Capital Aportado":"${:,.2f}"}),
                             use_container_width=True, hide_index=True)
 
        with col_a2:
            st.markdown("### Configuración de precios")
            st.markdown(f"""
            <div style="background:#0d1520;border:1px solid #1e3048;border-radius:8px;padding:14px;font-family:'IBM Plex Mono',monospace;font-size:11px">
              <div style="color:#4a6fa5;font-size:9px;letter-spacing:1px;margin-bottom:8px">FUENTES ACTIVAS</div>
              <div style="color:#f0b90b;margin-bottom:4px">● CoinMarketCap API — Cripto</div>
              <div style="color:#00d4ff;margin-bottom:4px">● Yahoo Finance (yfinance) — Acciones / ETF</div>
              <div style="color:#00ff88;margin-bottom:4px">● Yahoo Finance — TRM USD/COP</div>
              <div style="margin-top:8px;color:#4a6fa5;font-size:9px">CMC KEY: ...{CMC_API_KEY[-6:]}</div>
              <div style="color:#4a6fa5;font-size:9px">Caché: 5 min · TRM: 1h</div>
            </div>
            """, unsafe_allow_html=True)
 
            if st.button("🔄 Limpiar caché de precios"):
                st.cache_data.clear()
                st.success("✓ Caché limpiado — próxima consulta trae precios frescos")
 
        st.markdown("---")
        st.markdown("### Todas las operaciones (global)")
        if not df_ops.empty:
            st.dataframe(
                df_ops[["Fondo","Fecha","Activo","Categoria","Valor_Pos","Resultado","Ticker_API"]]
                    .sort_values("Fecha", ascending=False)
                    .style.format({"Valor_Pos":"${:,.2f}"}),
                use_container_width=True, hide_index=True
            )
