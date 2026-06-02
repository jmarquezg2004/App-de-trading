import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import requests
import time
 
# ══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Arkez Invest",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# CSS — fondo oscuro SUAVIZADO, texto bien legible
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');
 
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
 
/* Fondo general — azul muy oscuro pero NO negro puro */
.stApp { background: #0f1923; color: #dce9f5; }
 
/* Sidebar — ligeramente más claro que el fondo */
section[data-testid="stSidebar"] {
    background: #162030 !important;
    border-right: 1px solid #2a3f5a;
}
section[data-testid="stSidebar"] * { color: #dce9f5 !important; }
section[data-testid="stSidebar"] label { color: #a8c4dc !important; }
 
/* Cards de métricas */
[data-testid="metric-container"] {
    background: #1a2d42;
    border: 1px solid #2a3f5a;
    border-radius: 10px;
    padding: 16px !important;
    position: relative;
    overflow: hidden;
}
[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #00c8f0, #00e880);
}
[data-testid="stMetricValue"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.4rem !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #7aabcc !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
}
 
/* Tabs */
[data-testid="stTabs"] button {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #7aabcc !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #00c8f0 !important;
    border-bottom: 2px solid #00c8f0 !important;
}
 
/* Inputs y selectboxes — fondo visible */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: #1a2d42 !important;
    border: 1px solid #2a3f5a !important;
    color: #dce9f5 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    border-radius: 6px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #00c8f0 !important;
    box-shadow: 0 0 0 1px #00c8f0 !important;
}
/* Labels de formulario — más visibles */
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stDateInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stRadio"] label {
    color: #a8c4dc !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
/* Texto dentro de selectbox */
[data-testid="stSelectbox"] span { color: #dce9f5 !important; }
 
/* DataFrames */
[data-testid="stDataFrame"] {
    border: 1px solid #2a3f5a;
    border-radius: 8px;
    overflow: hidden;
}
.stDataFrame td, .stDataFrame th {
    color: #dce9f5 !important;
    background: #1a2d42 !important;
}
 
/* Botones */
.stButton button {
    background: linear-gradient(135deg, #00c8f0, #0090b3) !important;
    color: #0a1520 !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-size: 12px !important;
}
.stButton button:hover { filter: brightness(1.1) !important; }
 
/* Alerts */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border-left-width: 3px !important;
    background: #1a2d42 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    color: #dce9f5 !important;
}
 
/* Texto general — asegurar visibilidad */
p, span, div, li { color: #dce9f5; }
h1 { font-family: 'IBM Plex Mono', monospace !important; color: #00c8f0 !important; letter-spacing: 2px; }
h2 { font-family: 'IBM Plex Mono', monospace !important; font-size: 12px !important; letter-spacing: 1.5px; text-transform: uppercase; color: #7aabcc !important; margin-bottom: 12px !important; }
h3 { font-family: 'IBM Plex Mono', monospace !important; font-size: 13px !important; color: #00c8f0 !important; }
hr { border-color: #2a3f5a !important; }
 
/* Radio buttons */
[data-testid="stRadio"] > div { gap: 12px; }
[data-testid="stRadio"] label { color: #dce9f5 !important; font-size: 13px !important; }
 
/* Form container */
[data-testid="stForm"] {
    background: #1a2d42;
    border: 1px solid #2a3f5a;
    border-radius: 10px;
    padding: 16px;
}
 
/* Expander */
[data-testid="stExpander"] {
    background: #1a2d42 !important;
    border: 1px solid #2a3f5a !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary { color: #dce9f5 !important; }
</style>
""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# CONSTANTES
# ══════════════════════════════════════════════════════════════
FIREBASE_KEY  = "AIzaSyC52gIJJRTE1B4BqeUwDmaX2fWKS3sSw10"
FIRESTORE_URL = "https://firestore.googleapis.com/v1/projects/plataforma-de-inversiones/databases/(default)/documents"
ADMIN_EMAIL   = "jmarquezg2004@gmail.com"
CMC_API_KEY   = st.secrets.get("CMC_KEY", "d67913f039804c6b900905ebad7c1aaf")
 
CATEGORIAS  = ["Acción", "ETF", "Cripto", "CDT", "Fondo", "Cuenta Remunerada", "Otro"]
ESTRATEGIAS = ["Spot", "Holding", "Futuros", "Staking", "Farming", "Arbitraje",
               "Bot/Copy Trading", "Launchpool", "ICO", "Renta Fija"]
RESULTADOS  = ["Abierta", "Ganadora", "Perdedora", "Cancelada"]
 
# ══════════════════════════════════════════════════════════════
# FIREBASE AUTH
# ══════════════════════════════════════════════════════════════
def firebase_login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_KEY}"
    try:
        r = requests.post(url, json={"email": email, "password": password,
                                      "returnSecureToken": True}, timeout=8)
        if r.status_code == 200:
            return True, r.json()
        return False, r.json().get("error", {}).get("message", "Credenciales incorrectas")
    except Exception as e:
        return False, f"Error de conexión: {e}"
 
# ══════════════════════════════════════════════════════════════
# FIRESTORE CRUD — datos persisten en la nube, nunca se pierden
# ══════════════════════════════════════════════════════════════
def fs_get(coleccion, filtro_campo=None, filtro_valor=None):
    """Lee documentos. Opcionalmente filtra por campo=valor en cliente."""
    try:
        r = requests.get(f"{FIRESTORE_URL}/{coleccion}", timeout=10)
        if r.status_code == 200 and "documents" in r.json():
            rows = []
            for doc in r.json()["documents"]:
                fields = doc.get("fields", {})
                row = {"_id": doc["name"].split("/")[-1]}
                for k, v in fields.items():
                    # Firestore devuelve el valor en la clave que corresponde al tipo
                    raw = list(v.values())[0]
                    row[k] = raw
                rows.append(row)
            df = pd.DataFrame(rows)
            if filtro_campo and filtro_valor and not df.empty and filtro_campo in df.columns:
                df = df[df[filtro_campo] == filtro_valor]
            return df
    except Exception:
        pass
    return pd.DataFrame()
 
def fs_post(coleccion, datos):
    """Crea un nuevo documento. Retorna True/False."""
    fields = {}
    for k, v in datos.items():
        if isinstance(v, (int, float)):
            fields[k] = {"doubleValue": float(v)}
        elif isinstance(v, bool):
            fields[k] = {"booleanValue": v}
        else:
            fields[k] = {"stringValue": str(v)}
    try:
        r = requests.post(f"{FIRESTORE_URL}/{coleccion}", json={"fields": fields}, timeout=8)
        return r.status_code in (200, 201)
    except Exception:
        return False
 
def fs_patch(coleccion, doc_id, datos):
    """Actualiza campos específicos de un documento."""
    fields = {}
    for k, v in datos.items():
        if isinstance(v, (int, float)):
            fields[k] = {"doubleValue": float(v)}
        else:
            fields[k] = {"stringValue": str(v)}
    mask = "&".join([f"updateMask.fieldPaths={k}" for k in datos.keys()])
    try:
        requests.patch(f"{FIRESTORE_URL}/{coleccion}/{doc_id}?{mask}",
                       json={"fields": fields}, timeout=8)
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
@st.cache_data(ttl=300)
def get_trm():
    """TRM USD/COP desde Banco de la República (fixer) o Yahoo Finance."""
    # Fuente 1: ExchangeRate-API (pública, sin key)
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=6)
        if r.status_code == 200:
            cop = r.json().get("rates", {}).get("COP")
            if cop and cop > 3000:
                return float(cop)
    except Exception:
        pass
    # Fuente 2: Frankfurter (Banco Central Europeo)
    try:
        r = requests.get("https://api.frankfurter.app/latest?from=USD&to=COP", timeout=6)
        if r.status_code == 200:
            cop = r.json().get("rates", {}).get("COP")
            if cop and cop > 3000:
                return float(cop)
    except Exception:
        pass
    # Fuente 3: Yahoo Finance via yfinance
    try:
        import yfinance as yf
        t = yf.Ticker("USDCOP=X")
        px = t.fast_info.last_price
        if px and px > 3000:
            return float(px)
    except Exception:
        pass
    return 4200.0  # fallback
 
@st.cache_data(ttl=300)
def get_cmc_prices(symbols_tuple):
    """CoinMarketCap para cripto. symbols_tuple para cache hashable."""
    symbols = list(symbols_tuple)
    if not symbols:
        return {}
    try:
        r = requests.get(
            "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest",
            params={"symbol": ",".join(symbols), "convert": "USD"},
            headers={"X-CMC_PRO_API_KEY": CMC_API_KEY, "Accept": "application/json"},
            timeout=10
        )
        if r.status_code != 200:
            return {}
        result = {}
        for sym, items in r.json().get("data", {}).items():
            item = items[0] if isinstance(items, list) else items
            q = item.get("quote", {}).get("USD", {})
            result[sym.upper()] = {
                "price": q.get("price", 0),
                "chg24": q.get("percent_change_24h", 0),
            }
        return result
    except Exception:
        return {}
 
@st.cache_data(ttl=300)
def get_stock_price(ticker):
    """Yahoo Finance para acciones y ETFs."""
    try:
        import yfinance as yf
        t = yf.Ticker(ticker.upper())
        info  = t.fast_info
        price = getattr(info, "last_price", None) or getattr(info, "previous_close", None)
        prev  = getattr(info, "previous_close", price) or price
        chg   = ((price - prev) / prev * 100) if (price and prev and prev != 0) else 0
        return float(price) if price else None, float(chg)
    except Exception:
        return None, 0
 
def get_all_prices(df_ops):
    """Obtiene precios de todos los activos variables del portafolio."""
    prices = {}
    if df_ops.empty:
        return prices
    # Cripto → CMC
    cripto = df_ops[
        df_ops["Categoria"].isin(["Cripto"]) &
        df_ops["Ticker_API"].notna() &
        (df_ops["Ticker_API"].str.strip() != "")
    ]["Ticker_API"].str.upper().unique().tolist()
    if cripto:
        prices.update(get_cmc_prices(tuple(cripto)))
    # Acciones y ETFs → Yahoo
    stocks = df_ops[
        df_ops["Categoria"].isin(["Acción", "ETF", "Fondo"]) &
        df_ops["Ticker_API"].notna() &
        (df_ops["Ticker_API"].str.strip() != "")
    ]["Ticker_API"].str.upper().unique().tolist()
    for t in stocks:
        px, chg = get_stock_price(t)
        if px:
            prices[t] = {"price": px, "chg24": chg}
    return prices
 
# ══════════════════════════════════════════════════════════════
# CARGA DE DATOS CON NORMALIZACIÓN
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=60)
def cargar_aportes():
    cols = ["_id", "Fondo", "Socio", "Cedula", "Fecha", "Tipo", "Monto", "Usuario"]
    df = fs_get("aportes")
    if df.empty:
        return pd.DataFrame(columns=cols)
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce").fillna(0.0)
    return df
 
@st.cache_data(ttl=60)
def cargar_operaciones():
    cols = ["_id", "ID", "Fondo", "Usuario", "Fecha", "Activo", "Categoria",
            "Estrategia", "Broker", "Valor_Pos", "TP_pct", "SL_pct", "TP_usd",
            "SL_usd", "Comision", "Resultado", "Ticker_API", "Precio_Entrada",
            "Cantidad", "TEA", "Notas"]
    df = fs_get("operaciones")
    if df.empty:
        return pd.DataFrame(columns=cols)
    for c in cols:
        if c not in df.columns:
            df[c] = "" if c in ["_id","Fondo","Usuario","Fecha","Activo","Categoria",
                                  "Estrategia","Broker","Resultado","Ticker_API","Notas"] else 0
    for c in ["ID","Valor_Pos","TP_pct","SL_pct","TP_usd","SL_usd",
              "Comision","Precio_Entrada","Cantidad","TEA"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
    return df
 
# ══════════════════════════════════════════════════════════════
# CÁLCULOS FINANCIEROS
# ══════════════════════════════════════════════════════════════
def calcular_pnl(row):
    if row.get("Resultado") == "Ganadora":
        return float(row.get("TP_usd", 0)) - float(row.get("Comision", 0))
    elif row.get("Resultado") == "Perdedora":
        return -float(row.get("SL_usd", 0)) - float(row.get("Comision", 0))
    return 0.0
 
def valor_posicion_abierta(row, prices):
    ticker    = str(row.get("Ticker_API", "")).strip().upper()
    cat       = str(row.get("Categoria", ""))
    p_entrada = float(row.get("Precio_Entrada", 0) or 0)
    cantidad  = float(row.get("Cantidad", 0) or 0)
    valor_pos = float(row.get("Valor_Pos", 0) or 0)
    tea       = float(row.get("TEA", 0) or 0)
 
    if cat in ["CDT", "Cuenta Remunerada"] and tea > 0 and valor_pos > 0:
        try:
            dias = max((pd.Timestamp.now() - pd.to_datetime(row.get("Fecha"))).days, 0)
            val  = valor_pos * ((1 + tea) ** (dias / 365))
            gp   = val - valor_pos
            return val, gp, (gp / valor_pos * 100)
        except Exception:
            return valor_pos, 0, 0
 
    if ticker and ticker in prices and prices[ticker]["price"] > 0:
        px = prices[ticker]["price"]
        if p_entrada > 0 and cantidad > 0:
            val = px * cantidad
            gp  = val - (p_entrada * cantidad)
            return val, gp, (gp / (p_entrada * cantidad) * 100) if p_entrada * cantidad else 0
        elif valor_pos > 0 and p_entrada > 0:
            factor = px / p_entrada
            val    = valor_pos * factor
            gp     = val - valor_pos
            return val, gp, (gp / valor_pos * 100)
 
    return valor_pos, 0.0, 0.0
 
# ══════════════════════════════════════════════════════════════
# HELPERS UI
# ══════════════════════════════════════════════════════════════
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Mono, monospace", color="#dce9f5", size=11),
    margin=dict(l=0, r=0, t=36, b=0),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#2a3f5a", borderwidth=1),
    xaxis=dict(gridcolor="#1e3350", linecolor="#2a3f5a", tickfont=dict(size=10)),
    yaxis=dict(gridcolor="#1e3350", linecolor="#2a3f5a", tickfont=dict(size=10)),
)
 
def card(label, value_str, sub=None, accent="#00c8f0"):
    sub_html = f'<div style="font-family:IBM Plex Mono;font-size:11px;color:{accent};margin-top:3px">{sub}</div>' if sub else ""
    return f"""
    <div style="background:#1a2d42;border:1px solid #2a3f5a;border-radius:10px;
                padding:16px 18px;position:relative;overflow:hidden;height:100%">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;background:{accent}"></div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc;
                  letter-spacing:1.5px;text-transform:uppercase;margin-bottom:7px">{label}</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:22px;font-weight:600;
                  color:#ffffff;line-height:1">{value_str}</div>
      {sub_html}
    </div>"""
 
def fmt_usd(v, factor=1):
    v2 = v * factor
    if abs(v2) >= 1e6:
        return f"${v2/1e6:.2f}M"
    return f"${v2:,.2f}"
 
# ══════════════════════════════════════════════════════════════
# PANTALLA DE LOGIN
# ══════════════════════════════════════════════════════════════
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
 
if not st.session_state.logged_in:
    st.markdown("""
    <div style="text-align:center;padding:50px 0 24px">
      <div style="display:inline-block;width:52px;height:52px;
                  background:linear-gradient(135deg,#00c8f0,#00e880);
                  clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
                  margin-bottom:14px"></div>
      <h1 style="font-family:'IBM Plex Mono',monospace;font-size:26px;
                 color:#00c8f0;letter-spacing:3px;margin:0">ARKEZ INVEST</h1>
      <p style="color:#7aabcc;font-family:'IBM Plex Mono',monospace;
                font-size:11px;letter-spacing:2px;margin:8px 0 0">
        PLATAFORMA DE INVERSIONES · ACCESO PRIVADO
      </p>
    </div>
    """, unsafe_allow_html=True)
 
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        with st.container():
            st.markdown('<div style="background:#1a2d42;border:1px solid #2a3f5a;border-radius:14px;padding:28px">', unsafe_allow_html=True)
            email = st.text_input("Correo electrónico", placeholder="usuario@email.com")
            pwd   = st.text_input("Contraseña", type="password")
            if st.button("ENTRAR →", use_container_width=True):
                if email and pwd:
                    with st.spinner("Verificando…"):
                        ok, result = firebase_login(email, pwd)
                    if ok:
                        rol = "admin" if email.strip().lower() == ADMIN_EMAIL.lower() else "usuario"
                        st.session_state.update({
                            "logged_in": True,
                            "usuario": email.strip().lower(),
                            "rol": rol,
                            "fondo_sel": "Arkez Invest"
                        })
                        st.rerun()
                    else:
                        st.error(f"❌ {result}")
                else:
                    st.warning("Completa los dos campos")
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()
 
# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:14px 0 10px">
      <div style="display:inline-block;width:34px;height:34px;
                  background:linear-gradient(135deg,#00c8f0,#00e880);
                  clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
                  margin-bottom:7px"></div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:13px;
                  font-weight:600;color:#00c8f0;letter-spacing:2px">ARKEZ INVEST</div>
    </div>
    """, unsafe_allow_html=True)
 
    rol     = st.session_state.rol
    usuario = st.session_state.usuario
 
    rol_color = "#00c8f0" if rol == "admin" else "#00e880"
    rol_bg    = "rgba(0,200,240,.1)" if rol == "admin" else "rgba(0,232,128,.1)"
    st.markdown(f"""
    <div style="background:#1e3350;border:1px solid #2a3f5a;border-radius:8px;
                padding:10px 12px;margin-bottom:12px">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc;
                  letter-spacing:1px;margin-bottom:3px">USUARIO</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#dce9f5;
                  word-break:break-all">{usuario}</div>
      <span style="display:inline-block;margin-top:5px;background:{rol_bg};
                   color:{rol_color};border:1px solid {rol_color};
                   padding:1px 9px;border-radius:20px;
                   font-family:'IBM Plex Mono',monospace;font-size:9px;font-weight:600">
        {'⬡ ADMIN' if rol=='admin' else '● USUARIO'}
      </span>
    </div>
    """, unsafe_allow_html=True)
 
    # Cargar fondos disponibles
    df_aportes_all = cargar_aportes()
    df_ops_all     = cargar_operaciones()
 
    fondos_list = sorted(set(
        list(df_aportes_all["Fondo"].dropna().unique()) +
        list(df_ops_all["Fondo"].dropna().unique())
    ))
    if "Arkez Invest" not in fondos_list:
        fondos_list.insert(0, "Arkez Invest")
    if not fondos_list:
        fondos_list = ["Arkez Invest"]
 
    fondo = st.selectbox("🏦 Fondo activo", fondos_list,
                         index=fondos_list.index(st.session_state.get("fondo_sel","Arkez Invest"))
                         if st.session_state.get("fondo_sel") in fondos_list else 0)
    st.session_state.fondo_sel = fondo
 
    if rol == "admin":
        with st.expander("➕ Crear nuevo fondo"):
            nuevo = st.text_input("Nombre", key="nuevo_fondo_inp")
            if st.button("Crear fondo"):
                if nuevo.strip() and nuevo not in fondos_list:
                    fs_post("aportes", {
                        "Fondo": nuevo, "Socio": usuario, "Cedula": "",
                        "Fecha": str(date.today()), "Tipo": "Aporte",
                        "Monto": 0.0, "Usuario": usuario
                    })
                    st.success(f"✓ Fondo '{nuevo}' creado")
                    st.cache_data.clear()
                    st.rerun()
 
    # TRM en tiempo real
    trm = get_trm()
    st.markdown(f"""
    <div style="background:#1e3350;border:1px solid #2a3f5a;border-radius:8px;
                padding:9px 12px;margin:10px 0">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc;
                  letter-spacing:1px">TRM USD/COP (en tiempo real)</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:16px;
                  color:#ffcc44;font-weight:600">${trm:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
 
    moneda = st.radio("Moneda de visualización", ["USD", "COP"], horizontal=True)
    factor = trm if moneda == "COP" else 1.0
 
    st.markdown("---")
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        for k in ["logged_in","usuario","rol","fondo_sel"]:
            st.session_state.pop(k, None)
        st.rerun()
 
# ══════════════════════════════════════════════════════════════
# FILTRAR DATOS POR FONDO
# ══════════════════════════════════════════════════════════════
df_ap  = df_aportes_all[df_aportes_all["Fondo"] == fondo].copy() if not df_aportes_all.empty else pd.DataFrame()
df_ops = df_ops_all[df_ops_all["Fondo"] == fondo].copy() if not df_ops_all.empty else pd.DataFrame()
 
# Precios en tiempo real
prices = get_all_prices(df_ops) if not df_ops.empty else {}
 
# Métricas globales
capital_neto = df_ap["Monto"].sum() if not df_ap.empty else 0
 
ops_cerradas = df_ops[df_ops["Resultado"].isin(["Ganadora","Perdedora"])].copy() if not df_ops.empty else pd.DataFrame()
ops_abiertas = df_ops[df_ops["Resultado"] == "Abierta"].copy() if not df_ops.empty else pd.DataFrame()
 
if not ops_cerradas.empty:
    ops_cerradas["PnL"] = ops_cerradas.apply(calcular_pnl, axis=1)
    pnl_cerradas = ops_cerradas["PnL"].sum()
else:
    pnl_cerradas = 0
 
filas_abiertas, valor_abierto, pnl_abierto = [], 0, 0
if not ops_abiertas.empty:
    for _, row in ops_abiertas.iterrows():
        val, gp, gp_pct = valor_posicion_abierta(row, prices)
        valor_abierto += val
        pnl_abierto   += gp
        filas_abiertas.append({
            "Activo":        str(row.get("Activo","—")),
            "Categoria":     str(row.get("Categoria","—")),
            "Ticker":        str(row.get("Ticker_API","—")),
            "Valor_Entrada": float(row.get("Valor_Pos",0) or 0),
            "Valor_Actual":  val,
            "GP_usd":        gp,
            "GP_pct":        gp_pct,
            "Fecha":         str(row.get("Fecha","—")),
            "_id":           str(row.get("_id","")),
            "Usuario":       str(row.get("Usuario","—")),
        })
 
total_gp  = pnl_cerradas + pnl_abierto
patrimonio= capital_neto + total_gp
rend_pct  = (total_gp / capital_neto * 100) if capital_neto > 0 else 0
 
win_rate  = 0
if not ops_cerradas.empty:
    ganadoras = (ops_cerradas["Resultado"] == "Ganadora").sum()
    win_rate  = ganadoras / len(ops_cerradas) * 100
 
# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="display:flex;align-items:center;gap:14px;margin-bottom:4px;flex-wrap:wrap">
  <div style="width:38px;height:38px;background:linear-gradient(135deg,#00c8f0,#00e880);
              clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);flex-shrink:0"></div>
  <div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:19px;font-weight:600;
                color:#00c8f0;letter-spacing:2px">{fondo.upper()}</div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#7aabcc;
                letter-spacing:1px">PORTAFOLIO DE INVERSIONES · PRECIOS EN TIEMPO REAL</div>
  </div>
  <div style="margin-left:auto;font-family:'IBM Plex Mono',monospace;font-size:10px;color:#7aabcc">
    {datetime.now().strftime('%d/%m/%Y %H:%M')}
  </div>
</div>
<hr style="border-color:#2a3f5a;margin:12px 0 18px">
""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# KPIs
# ══════════════════════════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)
gp_color = "#00e880" if total_gp >= 0 else "#ff5566"
gp_sign  = "+" if total_gp >= 0 else ""
 
with k1:
    st.markdown(card("Patrimonio total", fmt_usd(patrimonio, factor)), unsafe_allow_html=True)
with k2:
    st.markdown(card("Capital aportado", fmt_usd(capital_neto, factor), accent="#7aabcc"), unsafe_allow_html=True)
with k3:
    st.markdown(card("Ganancia / Pérdida",
        f"{gp_sign}{fmt_usd(total_gp, factor)}",
        f"{'▲' if rend_pct>=0 else '▼'} {abs(rend_pct):.2f}%",
        accent=gp_color), unsafe_allow_html=True)
with k4:
    st.markdown(card("Posiciones abiertas", fmt_usd(valor_abierto, factor),
        f"{len(filas_abiertas)} posiciones", accent="#ffcc44"), unsafe_allow_html=True)
with k5:
    st.markdown(card("Win rate", f"{win_rate:.1f}%",
        f"{len(ops_cerradas)} ops cerradas", accent="#c084fc"), unsafe_allow_html=True)
 
st.markdown("<br>", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# TABS — todos los usuarios pueden registrar y ver sus ops
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    tab_dash, tab_pos, tab_reg, tab_soc, tab_anal, tab_adm = st.tabs([
        "⬡ Dashboard", "◈ Posiciones", "📌 Registrar operación",
        "💰 Socios / Capital", "📊 Análisis", "⚙ Administración"
    ])
else:
    tab_dash, tab_pos, tab_reg, tab_anal = st.tabs([
        "⬡ Dashboard", "◈ Mis posiciones",
        "📌 Registrar operación", "📊 Análisis"
    ])
 
# ══════════════════════════════════════════════════════════════
# TAB DASHBOARD
# ══════════════════════════════════════════════════════════════
with tab_dash:
    col_l, col_r = st.columns([3, 2])
 
    with col_l:
        # Evolución capital
        if not df_ap.empty:
            df_ev = df_ap.copy()
            df_ev["Fecha"] = pd.to_datetime(df_ev["Fecha"], errors="coerce")
            df_ev = df_ev.dropna(subset=["Fecha"]).sort_values("Fecha")
            df_ev["Monto_s"] = df_ev.apply(lambda r: r["Monto"] if r["Tipo"]=="Aporte" else -r["Monto"], axis=1)
            df_ev["Capital"] = df_ev["Monto_s"].cumsum() * factor
            fig = go.Figure(go.Scatter(
                x=df_ev["Fecha"], y=df_ev["Capital"],
                mode="lines+markers",
                line=dict(color="#00c8f0", width=2),
                fill="tozeroy", fillcolor="rgba(0,200,240,0.07)",
                marker=dict(color="#00c8f0", size=5),
                hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:$,.0f}<extra></extra>"
            ))
            fig.update_layout(**PLOTLY_LAYOUT,
                title=dict(text="Evolución del capital", font=dict(size=11,color="#7aabcc"), x=0.5))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        else:
            st.info("Sin movimientos de capital registrados aún.")
 
    with col_r:
        # Distribución por categoría
        if not df_ops.empty and "Categoria" in df_ops.columns:
            dist = df_ops.groupby("Categoria")["Valor_Pos"].sum().reset_index()
            dist = dist[dist["Valor_Pos"] > 0]
            if not dist.empty:
                CCOLORS = {"Acción":"#00c8f0","ETF":"#00e880","Cripto":"#ff7744",
                           "CDT":"#ffcc44","Fondo":"#c084fc","Cuenta Remunerada":"#f59e0b","Otro":"#7aabcc"}
                fig2 = go.Figure(go.Pie(
                    labels=dist["Categoria"], values=dist["Valor_Pos"] * factor,
                    hole=0.6,
                    marker=dict(colors=[CCOLORS.get(c,"#7aabcc") for c in dist["Categoria"]],
                                line=dict(color="#0f1923", width=2)),
                    textfont=dict(family="IBM Plex Mono", size=11),
                    hovertemplate="<b>%{label}</b><br>%{value:$,.0f}<br>%{percent}<extra></extra>"
                ))
                fig2.update_layout(**PLOTLY_LAYOUT,
                    title=dict(text="Distribución por tipo", font=dict(size=11,color="#7aabcc"), x=0.5))
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        else:
            st.info("Sin operaciones registradas.")
 
    # Precios en tiempo real
    if prices:
        st.markdown("## Precios en tiempo real")
        cols_px = st.columns(min(len(prices), 5))
        for i, (ticker, data) in enumerate(list(prices.items())[:10]):
            chg = data.get("chg24", 0)
            clr = "#00e880" if chg >= 0 else "#ff5566"
            sgn = "▲" if chg >= 0 else "▼"
            px  = data["price"]
            px_str = f"${px:,.4f}" if px < 10 else f"${px:,.2f}"
            with cols_px[i % min(len(prices), 5)]:
                st.markdown(f"""
                <div style="background:#1a2d42;border:1px solid #2a3f5a;border-radius:8px;
                            padding:12px;text-align:center;margin-bottom:8px">
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;
                              font-weight:600;color:#00c8f0">{ticker}</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:15px;
                              font-weight:600;color:#ffffff;margin:4px 0">{px_str}</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:{clr}">
                    {sgn} {abs(chg):.2f}%
                  </div>
                </div>""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# TAB POSICIONES
# ══════════════════════════════════════════════════════════════
with tab_pos:
    # Filtrar por usuario si no es admin
    mis_abiertas = filas_abiertas if rol == "admin" else [f for f in filas_abiertas if f["Usuario"] == usuario]
    mis_ops      = df_ops if rol == "admin" else (df_ops[df_ops["Usuario"] == usuario] if not df_ops.empty and "Usuario" in df_ops.columns else pd.DataFrame())
 
    if mis_abiertas:
        st.markdown("## Posiciones abiertas — valorización actual")
        for row in mis_abiertas:
            gp_clr  = "#00e880" if row["GP_usd"] >= 0 else "#ff5566"
            gp_sign = "+" if row["GP_usd"] >= 0 else ""
            px_info = prices.get(row["Ticker"].upper(), {})
            px_str  = f"${px_info.get('price',0):,.4f}" if px_info and px_info.get('price',0) < 10 else (f"${px_info.get('price',0):,.2f}" if px_info else "—")
 
            st.markdown(f"""
            <div style="background:#1a2d42;border:1px solid #2a3f5a;border-radius:10px;
                        padding:14px 18px;margin-bottom:10px;display:flex;
                        align-items:center;gap:18px;flex-wrap:wrap">
              <div style="min-width:120px">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:14px;
                            font-weight:600;color:#00c8f0">{row['Activo']}</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;
                            color:#7aabcc">{row['Ticker']} · {row['Categoria']}</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;
                            color:#4a6f8a">{row['Fecha']}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc;letter-spacing:1px">PRECIO ACTUAL</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:13px;color:#dce9f5">{px_str}</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc;letter-spacing:1px">ENTRADA</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:13px;color:#dce9f5">{fmt_usd(row['Valor_Entrada'],factor)}</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc;letter-spacing:1px">VALOR ACTUAL</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:14px;font-weight:600;color:#ffffff">{fmt_usd(row['Valor_Actual'],factor)}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc;letter-spacing:1px">G/P</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:600;color:{gp_clr}">{gp_sign}{fmt_usd(row['GP_usd'],factor)}</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:{gp_clr}">{gp_sign}{row['GP_pct']:.2f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("Sin posiciones abiertas." if rol == "admin" else "No tienes posiciones abiertas registradas.")
 
    # Historial
    if not mis_ops.empty:
        st.markdown("## Historial de operaciones")
        cols_show = [c for c in ["Fecha","Activo","Categoria","Estrategia","Broker",
                                   "Valor_Pos","Resultado","Ticker_API","Usuario"]
                     if c in mis_ops.columns]
        df_show = mis_ops[cols_show].sort_values("Fecha", ascending=False) if "Fecha" in cols_show else mis_ops[cols_show]
        df_show = df_show.copy()
        if "Valor_Pos" in df_show.columns:
            df_show["Valor_Pos"] = df_show["Valor_Pos"] * factor
 
        def color_res(val):
            if val == "Ganadora":  return "color:#00e880;font-weight:600"
            if val == "Perdedora": return "color:#ff5566;font-weight:600"
            if val == "Abierta":   return "color:#00c8f0"
            return ""
 
        styled = df_show.style
        if "Resultado" in df_show.columns:
            styled = styled.applymap(color_res, subset=["Resultado"])
        if "Valor_Pos" in df_show.columns:
            styled = styled.format({"Valor_Pos": "${:,.2f}"})
        st.dataframe(styled, use_container_width=True, hide_index=True)
 
# ══════════════════════════════════════════════════════════════
# TAB REGISTRAR OPERACIÓN — disponible para TODOS los usuarios
# ══════════════════════════════════════════════════════════════
with tab_reg:
    st.markdown("## Registrar nueva operación")
    st.markdown(f'<div style="font-family:IBM Plex Mono;font-size:11px;color:#7aabcc;margin-bottom:12px">Registrando como: <strong style="color:#00c8f0">{usuario}</strong> · Fondo: <strong style="color:#00c8f0">{fondo}</strong></div>', unsafe_allow_html=True)
 
    with st.form("form_operacion", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        fecha_op   = c1.date_input("Fecha", value=date.today())
        activo     = c2.text_input("Nombre del activo", placeholder="Bitcoin, Nubank, VTI…")
        categoria  = c3.selectbox("Categoría", CATEGORIAS)
        estrategia = c4.selectbox("Estrategia", ESTRATEGIAS)
 
        c5, c6, c7 = st.columns(3)
        broker     = c5.text_input("Broker / Exchange")
        valor_pos  = c6.number_input("Valor posición USD", min_value=0.0, step=0.01)
        comision   = c7.number_input("Comisión USD", min_value=0.0, step=0.01)
 
        c8, c9, c10, c11 = st.columns(4)
        precio_entrada = c8.number_input("Precio de entrada", min_value=0.0, step=0.0001, format="%.4f")
        cantidad       = c9.number_input("Cantidad / Unidades", min_value=0.0, step=0.000001, format="%.6f")
        tp_pct         = c10.number_input("TP %", min_value=0.0, step=0.1)
        sl_pct         = c11.number_input("SL %", min_value=0.0, step=0.1)
 
        c12, c13, c14 = st.columns(3)
        resultado  = c12.selectbox("Resultado actual", RESULTADOS)
        ticker_api = c13.text_input("Ticker para precios",
            placeholder="BTC (CMC) · AAPL · VTI (Yahoo)")
        tea_pct    = c14.number_input("TEA % anual (solo CDT/Rem.)", min_value=0.0,
            max_value=100.0, step=0.01,
            help="Solo para CDT o Cuenta Remunerada. Ej: 12.85 para 12.85% anual")
 
        notas = st.text_area("Notas", height=60, placeholder="Observaciones opcionales…")
 
        tp_usd = valor_pos * tp_pct / 100
        sl_usd = valor_pos * sl_pct / 100
 
        submitted = st.form_submit_button("💾 Guardar operación", use_container_width=True)
        if submitted:
            if not activo.strip():
                st.error("❌ El nombre del activo es obligatorio")
            else:
                nuevo_id = float(df_ops_all["ID"].max() + 1) if not df_ops_all.empty and df_ops_all["ID"].max() > 0 else 1.0
                ok = fs_post("operaciones", {
                    "ID":            nuevo_id,
                    "Fondo":         fondo,
                    "Usuario":       usuario,          # quién registra
                    "Fecha":         str(fecha_op),
                    "Activo":        activo.strip(),
                    "Categoria":     categoria,
                    "Estrategia":    estrategia,
                    "Broker":        broker.strip(),
                    "Valor_Pos":     float(valor_pos),
                    "TP_pct":        float(tp_pct),
                    "SL_pct":        float(sl_pct),
                    "TP_usd":        float(tp_usd),
                    "SL_usd":        float(sl_usd),
                    "Comision":      float(comision),
                    "Resultado":     resultado,
                    "Ticker_API":    ticker_api.strip().upper(),
                    "Precio_Entrada":float(precio_entrada),
                    "Cantidad":      float(cantidad),
                    "TEA":           float(tea_pct / 100) if tea_pct > 0 else 0.0,
                    "Notas":         notas.strip(),
                })
                if ok:
                    st.success("✓ Operación guardada en Firestore correctamente")
                    st.cache_data.clear()
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Error guardando. Verifica tu conexión.")
 
    # Editar resultado de operaciones propias
    mis_ops_e = df_ops if rol == "admin" else (
        df_ops[df_ops["Usuario"] == usuario] if not df_ops.empty and "Usuario" in df_ops.columns
        else pd.DataFrame()
    )
 
    if not mis_ops_e.empty:
        st.markdown("---")
        st.markdown("## Editar / eliminar operaciones")
        op_labels = [
            f"{row.get('Fecha','?')} — {row.get('Activo','?')} ({row.get('Resultado','?')})"
            for _, row in mis_ops_e.iterrows()
        ]
        sel = st.selectbox("Selecciona operación", range(len(op_labels)),
                           format_func=lambda i: op_labels[i])
        if sel is not None:
            sel_row = mis_ops_e.iloc[sel]
            ce1, ce2, ce3 = st.columns(3)
            with ce1:
                nuevo_res = st.selectbox("Nuevo resultado", RESULTADOS,
                    index=RESULTADOS.index(sel_row.get("Resultado","Abierta"))
                    if sel_row.get("Resultado") in RESULTADOS else 0,
                    key="edit_res")
                if st.button("✏️ Actualizar resultado"):
                    fs_patch("operaciones", sel_row["_id"], {"Resultado": nuevo_res})
                    st.success("✓ Resultado actualizado")
                    st.cache_data.clear()
                    st.rerun()
            with ce2:
                nueva_fecha = st.date_input("Cambiar fecha", key="edit_fecha")
                if st.button("📅 Actualizar fecha"):
                    fs_patch("operaciones", sel_row["_id"], {"Fecha": str(nueva_fecha)})
                    st.success("✓ Fecha actualizada")
                    st.cache_data.clear()
                    st.rerun()
            with ce3:
                st.markdown("<br>", unsafe_allow_html=True)
                # Admin puede borrar cualquiera; usuario solo las suyas
                puede_borrar = (rol == "admin") or (sel_row.get("Usuario","") == usuario)
                if puede_borrar:
                    if st.button("🗑 Eliminar operación"):
                        fs_delete("operaciones", sel_row["_id"])
                        st.success("✓ Eliminada")
                        st.cache_data.clear()
                        st.rerun()
 
# ══════════════════════════════════════════════════════════════
# TAB SOCIOS (solo admin)
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    with tab_soc:
        st.markdown("## Movimientos de capital — Socios")
 
        with st.form("form_aporte", clear_on_submit=True):
            c1, c2, c3, c4 = st.columns(4)
            socio  = c1.text_input("Nombre del socio")
            cedula = c2.text_input("Cédula / ID")
            tipo   = c3.selectbox("Tipo", ["Aporte", "Retiro"])
            monto  = c4.number_input("Monto (USD)", min_value=0.0, step=0.01)
            fecha_a = st.date_input("Fecha del movimiento", value=date.today())
 
            if st.form_submit_button("💾 Guardar movimiento", use_container_width=True):
                if not socio.strip():
                    st.error("❌ El nombre del socio es obligatorio")
                else:
                    ok = fs_post("aportes", {
                        "Fondo": fondo, "Socio": socio, "Cedula": cedula,
                        "Fecha": str(fecha_a), "Tipo": tipo,
                        "Monto": float(monto), "Usuario": usuario
                    })
                    if ok:
                        st.success("✓ Movimiento guardado")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("❌ Error guardando")
 
        if not df_ap.empty and df_ap["Socio"].dropna().str.strip().any():
            st.markdown("---")
            st.markdown("## Resumen por socio")
 
            resumen = df_ap.groupby(["Socio","Cedula"]).apply(
                lambda g: pd.Series({
                    "Total Aportes": g[g["Tipo"]=="Aporte"]["Monto"].sum() * factor,
                    "Total Retiros": g[g["Tipo"]=="Retiro"]["Monto"].sum() * factor,
                    "Neto":          g.apply(lambda r: r["Monto"] if r["Tipo"]=="Aporte"
                                             else -r["Monto"], axis=1).sum() * factor,
                })
            ).reset_index()
            tot_neto = resumen["Neto"].sum()
            resumen["% del Fondo"] = (resumen["Neto"] / tot_neto * 100).round(2) if tot_neto else 0
 
            st.dataframe(resumen.style.format({
                "Total Aportes":"${:,.2f}", "Total Retiros":"${:,.2f}",
                "Neto":"${:,.2f}", "% del Fondo":"{:.2f}%"
            }), use_container_width=True, hide_index=True)
 
            st.markdown("## Historial de movimientos")
            df_hist = df_ap.sort_values("Fecha", ascending=False)
            show_cols = [c for c in ["Fecha","Socio","Cedula","Tipo","Monto"] if c in df_hist.columns]
            df_hist_show = df_hist[show_cols].copy()
            if "Monto" in df_hist_show.columns:
                df_hist_show["Monto"] = df_hist_show["Monto"] * factor
            st.dataframe(
                df_hist_show.style
                    .applymap(lambda v: "color:#00e880;font-weight:600" if v=="Aporte" else
                               "color:#ff5566;font-weight:600" if v=="Retiro" else "",
                               subset=["Tipo"] if "Tipo" in df_hist_show.columns else [])
                    .format({"Monto":"${:,.2f}"} if "Monto" in df_hist_show.columns else {}),
                use_container_width=True, hide_index=True
            )
            if st.button("🗑 Eliminar último movimiento"):
                last_id = df_ap.sort_values("Fecha").iloc[-1]["_id"]
                fs_delete("aportes", last_id)
                st.cache_data.clear()
                st.rerun()
 
# ══════════════════════════════════════════════════════════════
# TAB ANÁLISIS
# ══════════════════════════════════════════════════════════════
with tab_anal:
    st.markdown("## Análisis de rendimiento")
 
    ops_anal = ops_cerradas if rol == "admin" else (
        ops_cerradas[ops_cerradas["Usuario"] == usuario]
        if not ops_cerradas.empty and "Usuario" in ops_cerradas.columns
        else pd.DataFrame()
    )
 
    if not ops_anal.empty:
        c_a1, c_a2 = st.columns([3, 2])
 
        with c_a1:
            fig_pnl = go.Figure(go.Bar(
                x=ops_anal.apply(lambda r: f"{r.get('Activo','?')} ({r.get('Fecha','?')})", axis=1),
                y=ops_anal["PnL"],
                marker_color=ops_anal["PnL"].apply(lambda x: "#00e880" if x >= 0 else "#ff5566"),
                text=ops_anal["PnL"].apply(lambda x: f"${x:,.0f}"),
                textposition="outside",
                textfont=dict(size=10),
                hovertemplate="<b>%{x}</b><br>P&L: $%{y:,.2f}<extra></extra>"
            ))
            fig_pnl.update_layout(**PLOTLY_LAYOUT,
                title=dict(text="P&L por operación cerrada", font=dict(size=11,color="#7aabcc"), x=0.5))
            st.plotly_chart(fig_pnl, use_container_width=True, config={"displayModeBar":False})
 
        with c_a2:
            pnl_vals  = ops_anal["PnL"]
            mejor     = ops_anal.loc[pnl_vals.idxmax()]
            peor      = ops_anal.loc[pnl_vals.idxmin()]
            avg_g     = pnl_vals[pnl_vals>0].mean() if (pnl_vals>0).any() else 0
            avg_p     = pnl_vals[pnl_vals<0].mean() if (pnl_vals<0).any() else 0
            pf        = abs(pnl_vals[pnl_vals>0].sum() / pnl_vals[pnl_vals<0].sum()) if (pnl_vals<0).any() else 9.99
            wr        = (pnl_vals>0).sum() / len(pnl_vals) * 100
 
            st.markdown(f"""
            <div style="background:#1a2d42;border:1px solid #2a3f5a;border-radius:10px;padding:16px">
              <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc;
                          letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px">Estadísticas</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
                <div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc">WIN RATE</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:18px;color:#c084fc;font-weight:600">{wr:.1f}%</div>
                </div>
                <div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc">PROFIT FACTOR</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:18px;color:#00c8f0;font-weight:600">{min(pf,9.99):.2f}x</div>
                </div>
                <div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc">AVG GANADORA</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:14px;color:#00e880;font-weight:600">+${avg_g:,.2f}</div>
                </div>
                <div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc">AVG PERDEDORA</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:14px;color:#ff5566;font-weight:600">${avg_p:,.2f}</div>
                </div>
                <div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc">MEJOR OP.</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#00e880">{mejor.get('Activo','?')}</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#00e880">+${mejor['PnL']:,.2f}</div>
                </div>
                <div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#7aabcc">PEOR OP.</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#ff5566">{peor.get('Activo','?')}</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#ff5566">${peor['PnL']:,.2f}</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("Aún no hay operaciones cerradas para analizar.")
 
# ══════════════════════════════════════════════════════════════
# TAB ADMINISTRACIÓN (solo admin)
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    with tab_adm:
        st.markdown("## Panel de administración")
 
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Resumen por fondo")
            if fondos_list:
                res = []
                for f in fondos_list:
                    cap = df_aportes_all[df_aportes_all["Fondo"]==f]["Monto"].sum() if not df_aportes_all.empty else 0
                    nop = len(df_ops_all[df_ops_all["Fondo"]==f]) if not df_ops_all.empty else 0
                    res.append({"Fondo":f, "Capital USD":cap*factor, "# Operaciones":nop})
                st.dataframe(pd.DataFrame(res).style.format({"Capital USD":"${:,.2f}"}),
                             use_container_width=True, hide_index=True)
 
        with col2:
            st.markdown("### Estado de APIs")
            st.markdown(f"""
            <div style="background:#1a2d42;border:1px solid #2a3f5a;border-radius:8px;
                        padding:14px;font-family:'IBM Plex Mono',monospace;font-size:11px">
              <div style="color:#7aabcc;font-size:9px;letter-spacing:1px;margin-bottom:10px">FUENTES ACTIVAS</div>
              <div style="color:#ffcc44;margin-bottom:6px">● CoinMarketCap API — Cripto</div>
              <div style="color:#00c8f0;margin-bottom:6px">● Yahoo Finance (yfinance) — Acciones / ETF</div>
              <div style="color:#00e880;margin-bottom:6px">● ExchangeRate-API / Frankfurter — TRM</div>
              <div style="color:#7aabcc;font-size:9px;margin-top:10px">TRM actual: ${trm:,.2f} COP/USD</div>
              <div style="color:#7aabcc;font-size:9px">CMC key: …{CMC_API_KEY[-6:]}</div>
              <div style="color:#7aabcc;font-size:9px">Caché precios: 5 min</div>
            </div>""", unsafe_allow_html=True)
 
            if st.button("🔄 Forzar actualización de precios"):
                st.cache_data.clear()
                st.success("✓ Caché limpiado — próxima carga trae precios frescos")
 
        st.markdown("---")
        st.markdown("### Todas las operaciones")
        if not df_ops_all.empty:
            cols_adm = [c for c in ["Fondo","Usuario","Fecha","Activo","Categoria","Valor_Pos","Resultado"] if c in df_ops_all.columns]
            df_adm = df_ops_all[cols_adm].sort_values("Fecha", ascending=False) if "Fecha" in cols_adm else df_ops_all[cols_adm]
            if "Valor_Pos" in df_adm.columns:
                df_adm = df_adm.copy()
                df_adm["Valor_Pos"] = df_adm["Valor_Pos"] * factor
            st.dataframe(df_adm.style.format({"Valor_Pos":"${:,.2f}"} if "Valor_Pos" in df_adm.columns else {}),
                         use_container_width=True, hide_index=True)
 
