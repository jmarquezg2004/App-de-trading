import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date
import requests
import time
 
# ══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Arkez Invest",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# ── CSS: fix dropdowns, inputs, labels, todo legible ──────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');
 
/* ── BASE ─────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    color: #DCE5F0;
}
.stApp { background: #111827; }
p, span, div { color: #DCE5F0; }
h1 { font-family:'IBM Plex Mono',monospace!important; color:#C8A84B!important; letter-spacing:2px; }
h2 { font-family:'IBM Plex Mono',monospace!important; font-size:12px!important;
     letter-spacing:1.5px; text-transform:uppercase; color:#8BA5C8!important; }
h3 { font-family:'IBM Plex Mono',monospace!important; font-size:13px!important; color:#C8A84B!important; }
hr { border-color:#2a3f5a!important; }
 
/* ── SIDEBAR ──────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #0D1929 !important;
    border-right: 1px solid #1E3354;
}
section[data-testid="stSidebar"] * { color: #DCE5F0 !important; }
section[data-testid="stSidebar"] label { color: #B0C4DC !important; font-size:12px!important; }
 
/* ── INPUTS — fondo oscuro, texto claro ───────────── */
input, textarea {
    background: #162236 !important;
    color: #DCE5F0 !important;
    border: 1px solid #1E3354 !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}
input:focus, textarea:focus {
    border-color: #C8A84B !important;
    box-shadow: 0 0 0 1px #C8A84B !important;
}
 
/* ── SELECTBOX — el más problemático ─────────────── */
/* Contenedor visible del selectbox */
[data-testid="stSelectbox"] > div > div {
    background: #162236 !important;
    border: 1px solid #1E3354 !important;
    border-radius: 6px !important;
    color: #DCE5F0 !important;
}
/* Texto seleccionado */
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] p {
    color: #DCE5F0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}
/* Dropdown abierto — lista de opciones */
[data-baseweb="select"] [role="listbox"],
[data-baseweb="popover"] ul,
[data-baseweb="menu"],
[data-baseweb="select"] ul {
    background: #162236 !important;
    border: 1px solid #1E3354 !important;
}
/* Cada opción de la lista */
[data-baseweb="select"] [role="option"],
[data-baseweb="menu"] li,
[data-baseweb="select"] li {
    background: #162236 !important;
    color: #DCE5F0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}
[data-baseweb="select"] [role="option"]:hover,
[data-baseweb="menu"] li:hover {
    background: #1A3050 !important;
    color: #C8A84B !important;
}
/* Flecha del selectbox */
[data-baseweb="select"] svg { fill: #8BA5C8 !important; }
 
/* ── LABELS ───────────────────────────────────────── */
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stDateInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stRadio"] > label,
[data-testid="stCheckbox"] label {
    color: #B0C4DC !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}
 
/* ── DATE INPUT ───────────────────────────────────── */
[data-testid="stDateInput"] input {
    background: #162236 !important;
    color: #DCE5F0 !important;
}
 
/* ── NUMBER INPUT ─────────────────────────────────── */
[data-testid="stNumberInput"] button {
    background: #1A3050 !important;
    color: #DCE5F0 !important;
    border-color: #1E3354 !important;
}
 
/* ── BUTTONS ──────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #C8A84B, #A07830) !important;
    color: #0a1520 !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-size: 12px !important;
    padding: 8px 20px !important;
}
.stButton > button:hover { filter: brightness(1.1) !important; }
.stButton > button[kind="secondary"] {
    background: #162236 !important;
    color: #DCE5F0 !important;
    border: 1px solid #1E3354 !important;
}
 
/* ── TABS ─────────────────────────────────────────── */
[data-testid="stTabs"] button {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #8BA5C8 !important;
    background: transparent !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #C8A84B !important;
    border-bottom: 2px solid #C8A84B !important;
}
[data-testid="stTabs"] { border-bottom: 1px solid #2a3f5a; }
 
/* ── METRICS ──────────────────────────────────────── */
[data-testid="metric-container"] {
    background: #162236;
    border: 1px solid #1E3354;
    border-radius: 10px;
    padding: 16px !important;
    position: relative;
    overflow: hidden;
}
[data-testid="metric-container"]::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, #C8A84B, #2ECC87);
}
[data-testid="stMetricValue"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.4rem !important;
    color: #F0EAD6 !important;
    font-weight: 600 !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #8BA5C8 !important;
}
 
/* ── DATAFRAME ────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid #1E3354;
    border-radius: 8px;
    overflow: hidden;
}
.stDataFrame th { background:#0F1A2B!important; color:#8BA5C8!important; }
.stDataFrame td { color:#DCE5F0!important; }
 
/* ── ALERTS ───────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border-left-width: 3px !important;
    background: #162236 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    color: #DCE5F0 !important;
}
.stSuccess { border-left-color: #2ECC87 !important; }
.stError   { border-left-color: #E85555 !important; }
.stWarning { border-left-color: #F0C040 !important; }
.stInfo    { border-left-color: #C8A84B !important; }
 
/* ── FORM ─────────────────────────────────────────── */
[data-testid="stForm"] {
    background: #0F1A2B !important;
    border: 1px solid #1E3354 !important;
    border-radius: 10px !important;
    padding: 20px !important;
}
 
/* ── EXPANDER ─────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #162236 !important;
    border: 1px solid #1E3354 !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p { color: #DCE5F0 !important; }
 
/* ── RADIO ────────────────────────────────────────── */
[data-testid="stRadio"] label span { color: #DCE5F0 !important; }
 
/* ── SPINNER ──────────────────────────────────────── */
.stSpinner > div { border-top-color: #C8A84B !important; }
</style>
""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# CONSTANTES
# ══════════════════════════════════════════════════════════════
FIREBASE_KEY  = "AIzaSyC52gIJJRTE1B4BqeUwDmaX2fWKS3sSw10"
FS_URL        = "https://firestore.googleapis.com/v1/projects/plataforma-de-inversiones/databases/(default)/documents"
ADMIN_EMAIL   = "jmarquezg2004@gmail.com"
CMC_KEY       = st.secrets.get("CMC_KEY", "d67913f039804c6b900905ebad7c1aaf")
 
CATEGORIAS  = ["Acción", "ETF", "Cripto", "CDT", "Fondo", "Cuenta Remunerada", "Otro"]
ESTRATEGIAS = ["Spot", "Holding", "Futuros", "Staking", "Farming",
               "Arbitraje", "Bot/Copy Trading", "Launchpool", "ICO", "Renta Fija"]
RESULTADOS  = ["Abierta", "Ganadora", "Perdedora", "Cancelada"]
TIPO_CUENTA = ["Fondo Grupal", "Portafolio Individual"]
 
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
        msg = r.json().get("error", {}).get("message", "Error")
        return False, msg
    except Exception as e:
        return False, f"Error de conexión: {e}"
 
def firebase_crear_usuario(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_KEY}"
    try:
        r = requests.post(url, json={"email": email, "password": password,
                                      "returnSecureToken": True}, timeout=8)
        if r.status_code == 200:
            return True, "OK"
        msg = r.json().get("error", {}).get("message", "Error")
        return False, msg
    except Exception as e:
        return False, str(e)
 
# ══════════════════════════════════════════════════════════════
# FIRESTORE CRUD — Bug fix: tipos correctos para cada campo
# ══════════════════════════════════════════════════════════════
def _to_field(v):
    """Convierte un valor Python al formato de campo Firestore."""
    if isinstance(v, bool):
        return {"booleanValue": v}
    if isinstance(v, int):
        return {"integerValue": str(v)}
    if isinstance(v, float):
        return {"doubleValue": v}
    return {"stringValue": str(v)}
 
def fs_get(col):
    try:
        r = requests.get(f"{FS_URL}/{col}", timeout=10)
        if r.status_code == 200:
            docs = r.json().get("documents", [])
            rows = []
            for doc in docs:
                row = {"_id": doc["name"].split("/")[-1]}
                for k, v in doc.get("fields", {}).items():
                    # Tomar el valor independientemente del tipo Firestore
                    val = list(v.values())[0]
                    row[k] = val
                rows.append(row)
            return pd.DataFrame(rows) if rows else pd.DataFrame()
    except Exception:
        pass
    return pd.DataFrame()
 
def fs_post(col, datos: dict):
    fields = {k: _to_field(v) for k, v in datos.items()}
    try:
        r = requests.post(f"{FS_URL}/{col}", json={"fields": fields}, timeout=10)
        return r.status_code in (200, 201)
    except Exception:
        return False
 
def fs_patch(col, doc_id, datos: dict):
    fields = {k: _to_field(v) for k, v in datos.items()}
    mask   = "&".join(f"updateMask.fieldPaths={k}" for k in datos)
    try:
        requests.patch(f"{FS_URL}/{col}/{doc_id}?{mask}",
                       json={"fields": fields}, timeout=10)
        return True
    except Exception:
        return False
 
def fs_delete(col, doc_id):
    try:
        requests.delete(f"{FS_URL}/{col}/{doc_id}", timeout=10)
        return True
    except Exception:
        return False
 
# ══════════════════════════════════════════════════════════════
# PRECIOS EN TIEMPO REAL
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def get_trm():
    for url in ["https://open.er-api.com/v6/latest/USD",
                "https://api.frankfurter.app/latest?from=USD&to=COP"]:
        try:
            r = requests.get(url, timeout=6)
            if r.status_code == 200:
                data = r.json()
                cop  = data.get("rates", {}).get("COP") or data.get("rates", {}).get("COP")
                if cop and float(cop) > 3000:
                    return float(cop)
        except Exception:
            pass
    try:
        import yfinance as yf
        px = yf.Ticker("USDCOP=X").fast_info.last_price
        if px and px > 3000:
            return float(px)
    except Exception:
        pass
    return 4200.0
 
@st.cache_data(ttl=300)
def get_cmc(symbols_tuple):
    if not symbols_tuple:
        return {}
    try:
        r = requests.get(
            "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest",
            params={"symbol": ",".join(symbols_tuple), "convert": "USD"},
            headers={"X-CMC_PRO_API_KEY": CMC_KEY, "Accept": "application/json"},
            timeout=10
        )
        if r.status_code != 200:
            return {}
        out = {}
        for sym, items in r.json().get("data", {}).items():
            item = items[0] if isinstance(items, list) else items
            q    = item.get("quote", {}).get("USD", {})
            out[sym.upper()] = {"price": q.get("price", 0), "chg24": q.get("percent_change_24h", 0)}
        return out
    except Exception:
        return {}
 
@st.cache_data(ttl=300)
def get_stock(ticker):
    try:
        import yfinance as yf
        info  = yf.Ticker(ticker).fast_info
        price = getattr(info, "last_price", None) or getattr(info, "previous_close", None)
        prev  = getattr(info, "previous_close", price) or price
        chg   = ((price - prev) / prev * 100) if price and prev else 0
        return float(price) if price else None, float(chg)
    except Exception:
        return None, 0
 
def get_prices(df_ops):
    out = {}
    if df_ops.empty:
        return out
    criptos = df_ops[df_ops["Categoria"] == "Cripto"]["Ticker_API"].dropna()
    criptos = [x.strip().upper() for x in criptos if x.strip()]
    if criptos:
        out.update(get_cmc(tuple(set(criptos))))
    stocks = df_ops[df_ops["Categoria"].isin(["Acción","ETF","Fondo"])]["Ticker_API"].dropna()
    for t in set(x.strip().upper() for x in stocks if x.strip()):
        px, chg = get_stock(t)
        if px:
            out[t] = {"price": px, "chg24": chg}
    return out
 
# ══════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=60)
def load_aportes():
    df = fs_get("aportes")
    if df.empty:
        return pd.DataFrame(columns=["_id","Fondo","Socio","Cedula","Fecha",
                                      "Tipo","Monto","Usuario","TipoCuenta"])
    for c in ["Monto"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
    for c in ["_id","Fondo","Socio","Cedula","Fecha","Tipo","Usuario","TipoCuenta"]:
        if c not in df.columns:
            df[c] = ""
    return df
 
@st.cache_data(ttl=60)
def load_ops():
    df = fs_get("operaciones")
    if df.empty:
        return pd.DataFrame(columns=["_id","ID","Fondo","Usuario","Fecha","Activo",
            "Categoria","Estrategia","Broker","Valor_Pos","TP_pct","SL_pct",
            "TP_usd","SL_usd","Comision","Resultado","Ticker_API",
            "Precio_Entrada","Cantidad","TEA","Notas"])
    num_cols = ["Valor_Pos","TP_pct","SL_pct","TP_usd","SL_usd",
                "Comision","Precio_Entrada","Cantidad","TEA","ID"]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
        else:
            df[c] = 0.0
    for c in ["_id","Fondo","Usuario","Fecha","Activo","Categoria",
              "Estrategia","Broker","Resultado","Ticker_API","Notas"]:
        if c not in df.columns:
            df[c] = ""
    return df
 
@st.cache_data(ttl=60)
def load_usuarios():
    df = fs_get("usuarios")
    if df.empty:
        return pd.DataFrame(columns=["_id","Email","Nombre","Fondo","TipoCuenta","Activo"])
    for c in ["_id","Email","Nombre","Fondo","TipoCuenta","Activo"]:
        if c not in df.columns:
            df[c] = ""
    return df
 
# ══════════════════════════════════════════════════════════════
# CÁLCULOS
# ══════════════════════════════════════════════════════════════
def calcular_pnl(row):
    if row.get("Resultado") == "Ganadora":
        return float(row.get("TP_usd", 0) or 0) - float(row.get("Comision", 0) or 0)
    if row.get("Resultado") == "Perdedora":
        return -float(row.get("SL_usd", 0) or 0) - float(row.get("Comision", 0) or 0)
    return 0.0
 
def valor_abierta(row, prices):
    ticker   = str(row.get("Ticker_API","")).strip().upper()
    cat      = str(row.get("Categoria",""))
    entrada  = float(row.get("Precio_Entrada", 0) or 0)
    cantidad = float(row.get("Cantidad", 0) or 0)
    v_pos    = float(row.get("Valor_Pos", 0) or 0)
    tea      = float(row.get("TEA", 0) or 0)
 
    if cat in ["CDT","Cuenta Remunerada"] and tea > 0 and v_pos > 0:
        try:
            dias = max((pd.Timestamp.now() - pd.to_datetime(row.get("Fecha"))).days, 0)
            val  = v_pos * ((1 + tea) ** (dias / 365))
            gp   = val - v_pos
            return val, gp, gp / v_pos * 100
        except Exception:
            return v_pos, 0, 0
 
    if ticker and ticker in prices and prices[ticker].get("price", 0) > 0:
        px = prices[ticker]["price"]
        if entrada > 0 and cantidad > 0:
            val = px * cantidad
            gp  = val - entrada * cantidad
            pct = gp / (entrada * cantidad) * 100
            return val, gp, pct
        if v_pos > 0 and entrada > 0:
            val = v_pos * px / entrada
            gp  = val - v_pos
            return val, gp, gp / v_pos * 100
 
    return v_pos, 0.0, 0.0
 
# ══════════════════════════════════════════════════════════════
# UI HELPERS
# ══════════════════════════════════════════════════════════════
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Mono", color="#DCE5F0", size=11),
    margin=dict(l=0, r=0, t=36, b=0),
    xaxis=dict(gridcolor="#152034", linecolor="#1E3354"),
    yaxis=dict(gridcolor="#152034", linecolor="#1E3354"),
)
CAT_COLORS = {"Acción":"#C8A84B","ETF":"#2ECC87","Cripto":"#E87844",
              "CDT":"#F0C040","Fondo":"#9B8EC4","Cuenta Remunerada":"#f59e0b","Otro":"#8BA5C8"}
 
def card(label, val, sub=None, color="#C8A84B"):
    sub_h = f'<div style="font:500 11px/1.3 IBM Plex Mono,mono;color:{color};margin-top:3px">{sub}</div>' if sub else ""
    return f"""<div style="background:#1a2d42;border:1px solid #2a3f5a;border-radius:10px;
        padding:16px 18px;position:relative;overflow:hidden;height:100%">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;background:{color}"></div>
      <div style="font:400 9px/1 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1.5px;
                  text-transform:uppercase;margin-bottom:8px">{label}</div>
      <div style="font:600 22px/1 IBM Plex Mono,mono;color:#F0EAD6">{val}</div>{sub_h}</div>"""
 
def money(v, f=1):
    v2 = v * f
    if abs(v2) >= 1e6: return f"${v2/1e6:.2f}M"
    return f"${v2:,.2f}"
 
def section(title):
    st.markdown(f'<h2 style="margin:20px 0 10px">{title}</h2>', unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
 
if not st.session_state.logged_in:
    st.markdown("""<div style="text-align:center;padding:50px 0 24px">
      <div style="display:inline-block;width:52px;height:52px;margin-bottom:14px;
                  background:linear-gradient(135deg,#C8A84B,#2ECC87);
                  clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%)"></div>
      <div style="font:600 26px/1 IBM Plex Mono,mono;color:#C8A84B;letter-spacing:3px">
        ARKEZ</div>
      <div style="font:400 11px/1 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:2px;margin-top:8px">
        PLATAFORMA DE INVERSIONES · ACCESO PRIVADO</div></div>""", unsafe_allow_html=True)
 
    _, col, _ = st.columns([1,1.2,1])
    with col:
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
    st.stop()
 
# ══════════════════════════════════════════════════════════════
# CARGAR TODOS LOS DATOS
# ══════════════════════════════════════════════════════════════
rol     = st.session_state.rol
usuario = st.session_state.usuario
 
df_ap_all   = load_aportes()
df_ops_all  = load_ops()
df_usuarios = load_usuarios()
 
# Fondos disponibles
fondos_set = set(df_ap_all["Fondo"].dropna().tolist()) | set(df_ops_all["Fondo"].dropna().tolist())
fondos_set.discard("")
fondos_list = sorted(fondos_set) or ["Arkez Invest"]
if "Arkez Invest" not in fondos_list:
    fondos_list.insert(0, "Arkez Invest")
 
# Si el usuario no es admin, lo limitamos a su fondo asignado
if rol == "usuario" and not df_usuarios.empty and "Email" in df_usuarios.columns:
    mi_fila = df_usuarios[df_usuarios["Email"].str.lower() == usuario]
    if not mi_fila.empty and mi_fila.iloc[0].get("Fondo"):
        fondo_usuario = mi_fila.iloc[0]["Fondo"]
        if fondo_usuario not in fondos_list:
            fondos_list.append(fondo_usuario)
        fondos_list_usuario = [fondo_usuario]
    else:
        fondos_list_usuario = fondos_list
else:
    fondos_list_usuario = fondos_list
 
# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""<div style="text-align:center;padding:14px 0 10px">
      <div style="display:inline-block;width:34px;height:34px;margin-bottom:7px;
                  background:linear-gradient(135deg,#C8A84B,#2ECC87);
                  clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%)"></div>
      <div style="font:600 13px/1 IBM Plex Mono,mono;color:#C8A84B;letter-spacing:2px">
        ARKEZ</div></div>""", unsafe_allow_html=True)
 
    col_r = "#C8A84B" if rol == "admin" else "#2ECC87"
    col_b = "rgba(200,168,75,.12)" if rol == "admin" else "rgba(0,232,128,.12)"
    st.markdown(f"""<div style="background:#152034;border:1px solid #2a3f5a;border-radius:8px;
        padding:10px 12px;margin-bottom:12px">
      <div style="font:400 9px/1 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px;
                  margin-bottom:3px">USUARIO</div>
      <div style="font:400 11px/1.4 IBM Plex Mono,mono;color:#DCE5F0;word-break:break-all">{usuario}</div>
      <span style="display:inline-block;margin-top:5px;background:{col_b};color:{col_r};
                   border:1px solid {col_r};padding:1px 9px;border-radius:20px;
                   font:600 9px/1.8 IBM Plex Mono,mono">
        {'⬡ ADMIN' if rol=='admin' else '● USUARIO'}</span></div>""", unsafe_allow_html=True)
 
    # Selección de fondo
    lista_f = fondos_list if rol == "admin" else fondos_list_usuario
    idx_f   = lista_f.index(st.session_state.get("fondo_sel","Arkez Invest")) \
              if st.session_state.get("fondo_sel") in lista_f else 0
    fondo   = st.selectbox("🏦 Fondo activo", lista_f, index=idx_f)
    st.session_state.fondo_sel = fondo
 
    # TRM
    trm = get_trm()
    st.markdown(f"""<div style="background:#152034;border:1px solid #2a3f5a;border-radius:8px;
        padding:9px 12px;margin:10px 0">
      <div style="font:400 9px/1 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">
        TRM USD/COP (tiempo real)</div>
      <div style="font:600 16px/1.5 IBM Plex Mono,mono;color:#F0C040">${trm:,.2f}</div>
    </div>""", unsafe_allow_html=True)
 
    moneda = st.radio("Moneda", ["USD", "COP"], horizontal=True)
    factor = trm if moneda == "COP" else 1.0
 
    st.markdown("---")
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
 
# ══════════════════════════════════════════════════════════════
# DATOS DEL FONDO SELECCIONADO
# ══════════════════════════════════════════════════════════════
df_ap  = df_ap_all[df_ap_all["Fondo"] == fondo].copy()  if not df_ap_all.empty  else pd.DataFrame()
df_ops = df_ops_all[df_ops_all["Fondo"] == fondo].copy() if not df_ops_all.empty else pd.DataFrame()
 
prices = get_prices(df_ops)
capital= df_ap["Monto"].sum() if not df_ap.empty else 0
 
ops_c = df_ops[df_ops["Resultado"].isin(["Ganadora","Perdedora"])].copy() if not df_ops.empty else pd.DataFrame()
ops_a = df_ops[df_ops["Resultado"] == "Abierta"].copy()                   if not df_ops.empty else pd.DataFrame()
 
if not ops_c.empty:
    ops_c["PnL"] = ops_c.apply(calcular_pnl, axis=1)
    pnl_c = ops_c["PnL"].sum()
else:
    pnl_c = 0.0
 
abiertas, val_ab, pnl_ab = [], 0.0, 0.0
if not ops_a.empty:
    for _, row in ops_a.iterrows():
        val, gp, pct = valor_abierta(row, prices)
        val_ab += val; pnl_ab += gp
        abiertas.append({
            "Activo":   row.get("Activo","—"),   "Categoria": row.get("Categoria","—"),
            "Ticker":   row.get("Ticker_API","—"),"Val_ent":   float(row.get("Valor_Pos",0) or 0),
            "Val_act":  val,                      "GP_usd":    gp,
            "GP_pct":   pct,                      "Fecha":     row.get("Fecha","—"),
            "_id":      row.get("_id",""),         "Usuario":   row.get("Usuario","—"),
        })
 
total_gp  = pnl_c + pnl_ab
patrimonio= capital + total_gp
rend      = total_gp / capital * 100 if capital > 0 else 0
wr        = ((ops_c["Resultado"] == "Ganadora").sum() / len(ops_c) * 100) if not ops_c.empty else 0
 
# ══════════════════════════════════════════════════════════════
# HEADER + KPIs
# ══════════════════════════════════════════════════════════════
st.markdown(f"""<div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:4px">
  <div style="width:38px;height:38px;flex-shrink:0;
              background:linear-gradient(135deg,#C8A84B,#2ECC87);
              clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%)"></div>
  <div>
    <div style="font:600 18px/1 IBM Plex Mono,mono;color:#C8A84B;letter-spacing:2px">
      {fondo.upper()}</div>
    <div style="font:400 10px/1.5 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">
      PORTAFOLIO DE INVERSIONES · PRECIOS EN TIEMPO REAL</div>
  </div>
  <div style="margin-left:auto;font:400 10px/1 IBM Plex Mono,mono;color:#8BA5C8">
    {datetime.now().strftime('%d/%m/%Y %H:%M')}</div></div>
<hr style="margin:12px 0 18px">""", unsafe_allow_html=True)
 
gp_col = "#2ECC87" if total_gp >= 0 else "#E85555"
k1,k2,k3,k4,k5 = st.columns(5)
with k1: st.markdown(card("Patrimonio total",  money(patrimonio,factor)), unsafe_allow_html=True)
with k2: st.markdown(card("Capital aportado",  money(capital,factor), color="#8BA5C8"), unsafe_allow_html=True)
with k3: st.markdown(card("Ganancia / Pérdida",
    f"{'+'if total_gp>=0 else ''}{money(total_gp,factor)}",
    f"{'▲' if rend>=0 else '▼'} {abs(rend):.2f}%", color=gp_col), unsafe_allow_html=True)
with k4: st.markdown(card("Posiciones abiertas", money(val_ab,factor),
    f"{len(abiertas)} posiciones", color="#F0C040"), unsafe_allow_html=True)
with k5: st.markdown(card("Win rate", f"{wr:.1f}%",
    f"{len(ops_c)} ops cerradas", color="#9B8EC4"), unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    tabs = st.tabs(["⬡ Dashboard","◈ Posiciones","📌 Registrar Op.",
                    "💰 Socios / Capital","📊 Análisis",
                    "👥 Usuarios","⚙ Administración"])
    t_dash,t_pos,t_reg,t_soc,t_anal,t_usr,t_adm = tabs
else:
    tabs = st.tabs(["⬡ Dashboard","◈ Mis posiciones","📌 Registrar Op.","📊 Análisis"])
    t_dash,t_pos,t_reg,t_anal = tabs
 
# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
with t_dash:
    cl, cr = st.columns([3,2])
    with cl:
        if not df_ap.empty:
            dfe = df_ap.copy()
            dfe["Fecha"] = pd.to_datetime(dfe["Fecha"], errors="coerce")
            dfe = dfe.dropna(subset=["Fecha"]).sort_values("Fecha")
            dfe["cap"] = dfe.apply(lambda r: r["Monto"] if r["Tipo"]=="Aporte" else -r["Monto"], axis=1).cumsum() * factor
            fig = go.Figure(go.Scatter(x=dfe["Fecha"], y=dfe["cap"], mode="lines+markers",
                line=dict(color="#C8A84B",width=2), fill="tozeroy",
                fillcolor="rgba(200,168,75,.07)", marker=dict(color="#C8A84B",size=5),
                hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:$,.0f}<extra></extra>"))
            fig.update_layout(**PLOTLY_THEME,
                title=dict(text="Evolución del capital",font=dict(size=11,color="#8BA5C8"),x=.5))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        else:
            st.info("Sin movimientos de capital registrados.")
    with cr:
        if not df_ops.empty:
            dist = df_ops.groupby("Categoria")["Valor_Pos"].sum().reset_index()
            dist = dist[dist["Valor_Pos"] > 0]
            if not dist.empty:
                fig2 = go.Figure(go.Pie(
                    labels=dist["Categoria"], values=dist["Valor_Pos"]*factor, hole=.6,
                    marker=dict(colors=[CAT_COLORS.get(c,"#8BA5C8") for c in dist["Categoria"]],
                                line=dict(color="#0f1923",width=2)),
                    hovertemplate="<b>%{label}</b><br>%{value:$,.0f}<br>%{percent}<extra></extra>"))
                fig2.update_layout(**PLOTLY_THEME,
                    title=dict(text="Distribución por tipo",font=dict(size=11,color="#8BA5C8"),x=.5))
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        else:
            st.info("Sin operaciones registradas.")
 
    if prices:
        section("Precios en tiempo real")
        cols_p = st.columns(min(len(prices),5))
        for i,(tk,d) in enumerate(list(prices.items())[:10]):
            chg = d.get("chg24",0); px = d.get("price",0)
            clr = "#2ECC87" if chg>=0 else "#E85555"
            px_s= f"${px:,.4f}" if px<10 else f"${px:,.2f}"
            with cols_p[i % min(len(prices),5)]:
                st.markdown(f"""<div style="background:#1a2d42;border:1px solid #2a3f5a;
                    border-radius:8px;padding:12px;text-align:center;margin-bottom:8px">
                  <div style="font:600 11px/1.5 IBM Plex Mono,mono;color:#C8A84B">{tk}</div>
                  <div style="font:600 15px/1.4 IBM Plex Mono,mono;color:#F0EAD6">{px_s}</div>
                  <div style="font:400 10px/1.3 IBM Plex Mono,mono;color:{clr}">
                    {'▲' if chg>=0 else '▼'} {abs(chg):.2f}%</div></div>""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
# POSICIONES
# ══════════════════════════════════════════════════════════════
with t_pos:
    mis_ab = abiertas if rol=="admin" else [a for a in abiertas if a["Usuario"]==usuario]
    mis_op = df_ops if rol=="admin" else (
        df_ops[df_ops["Usuario"]==usuario] if "Usuario" in df_ops.columns else pd.DataFrame())
 
    if mis_ab:
        section("Posiciones abiertas — valorización actual")
        for a in mis_ab:
            gc = "#2ECC87" if a["GP_usd"]>=0 else "#E85555"
            sg = "+" if a["GP_usd"]>=0 else ""
            pxd= prices.get(a["Ticker"].upper(),{})
            pxs= (f"${pxd['price']:,.4f}" if pxd.get("price",0)<10 else f"${pxd['price']:,.2f}") if pxd else "—"
            st.markdown(f"""<div style="background:#1a2d42;border:1px solid #2a3f5a;
                border-radius:10px;padding:14px 18px;margin-bottom:10px;
                display:flex;align-items:center;gap:18px;flex-wrap:wrap">
              <div style="min-width:130px">
                <div style="font:600 14px/1.3 IBM Plex Mono,mono;color:#C8A84B">{a['Activo']}</div>
                <div style="font:400 10px/1.4 IBM Plex Mono,mono;color:#8BA5C8">
                  {a['Ticker']} · {a['Categoria']}</div>
                <div style="font:400 9px/1.4 IBM Plex Mono,mono;color:#4a6f8a">{a['Fecha']}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px/1 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">PRECIO HOY</div>
                <div style="font:500 13px/1.5 IBM Plex Mono,mono;color:#DCE5F0">{pxs}</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font:400 9px/1 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">ENTRADA</div>
                <div style="font:500 13px/1.5 IBM Plex Mono,mono;color:#DCE5F0">{money(a['Val_ent'],factor)}</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font:400 9px/1 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">VALOR ACTUAL</div>
                <div style="font:600 14px/1.5 IBM Plex Mono,mono;color:#F0EAD6">{money(a['Val_act'],factor)}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px/1 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">G/P</div>
                <div style="font:600 15px/1.3 IBM Plex Mono,mono;color:{gc}">{sg}{money(a['GP_usd'],factor)}</div>
                <div style="font:500 10px/1.3 IBM Plex Mono,mono;color:{gc}">{sg}{a['GP_pct']:.2f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("Sin posiciones abiertas.")
 
    if not mis_op.empty:
        section("Historial de operaciones")
        cols_s = [c for c in ["Fecha","Activo","Categoria","Estrategia","Broker",
                               "Valor_Pos","Resultado","Ticker_API","Usuario"] if c in mis_op.columns]
        dfs = mis_op[cols_s].sort_values("Fecha",ascending=False).copy()
        if "Valor_Pos" in dfs.columns:
            dfs["Valor_Pos"] = dfs["Valor_Pos"] * factor
        def cr_res(v):
            if v=="Ganadora":  return "color:#2ECC87;font-weight:600"
            if v=="Perdedora": return "color:#E85555;font-weight:600"
            if v=="Abierta":   return "color:#C8A84B"
            return ""
        styled = dfs.style
        if "Resultado" in dfs.columns:
            styled = styled.applymap(cr_res, subset=["Resultado"])
        if "Valor_Pos" in dfs.columns:
            styled = styled.format({"Valor_Pos":"${:,.2f}"})
        st.dataframe(styled, use_container_width=True, hide_index=True)
 
# ══════════════════════════════════════════════════════════════
# REGISTRAR OPERACIÓN — todos los usuarios
# ══════════════════════════════════════════════════════════════
with t_reg:
    section("Registrar nueva operación")
    st.markdown(f'<div style="font:400 11px/1.5 IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:12px">'
                f'Registrando como: <strong style="color:#C8A84B">{usuario}</strong> · '
                f'Fondo: <strong style="color:#C8A84B">{fondo}</strong></div>', unsafe_allow_html=True)
 
    with st.form("form_op", clear_on_submit=True):
        c1,c2,c3,c4 = st.columns(4)
        fecha_op   = c1.date_input("Fecha", value=date.today())
        activo     = c2.text_input("Nombre del activo", placeholder="Bitcoin, Nubank, VTI…")
        categoria  = c3.selectbox("Categoría", CATEGORIAS, index=0)
        estrategia = c4.selectbox("Estrategia", ESTRATEGIAS, index=0)
 
        c5,c6,c7 = st.columns(3)
        broker    = c5.text_input("Broker / Exchange")
        valor_pos = c6.number_input("Valor posición USD", min_value=0.0, step=0.01, format="%.2f")
        comision  = c7.number_input("Comisión USD", min_value=0.0, step=0.01, format="%.2f")
 
        c8,c9,c10,c11 = st.columns(4)
        precio_ent = c8.number_input("Precio de entrada", min_value=0.0, step=0.0001, format="%.4f")
        cantidad   = c9.number_input("Cantidad / Unidades", min_value=0.0, step=0.000001, format="%.6f")
        tp_pct     = c10.number_input("TP %", min_value=0.0, step=0.1, format="%.2f")
        sl_pct     = c11.number_input("SL %", min_value=0.0, step=0.1, format="%.2f")
 
        c12,c13,c14 = st.columns(3)
        resultado   = c12.selectbox("Resultado actual", RESULTADOS, index=0)
        ticker_api  = c13.text_input("Ticker para precios",
                        placeholder="BTC · AAPL · VTI · ETH")
        tea_pct     = c14.number_input("TEA % anual (CDT/Remunerada)",
                        min_value=0.0, max_value=100.0, step=0.01, format="%.2f",
                        help="Solo para CDT o Cuenta Remunerada. Ej: 12.85")
 
        notas = st.text_area("Notas", height=60, placeholder="Observaciones opcionales…")
 
        if st.form_submit_button("💾 GUARDAR OPERACIÓN", use_container_width=True):
            if not activo.strip():
                st.error("❌ El nombre del activo es obligatorio")
            else:
                # Calcular ID siguiente
                if not df_ops_all.empty and "ID" in df_ops_all.columns:
                    max_id = pd.to_numeric(df_ops_all["ID"], errors="coerce").max()
                    nuevo_id = float(max_id + 1) if not pd.isna(max_id) else 1.0
                else:
                    nuevo_id = 1.0
 
                datos = {
                    "ID":             nuevo_id,
                    "Fondo":          fondo,
                    "Usuario":        usuario,
                    "Fecha":          str(fecha_op),
                    "Activo":         activo.strip(),
                    "Categoria":      categoria,
                    "Estrategia":     estrategia,
                    "Broker":         broker.strip(),
                    "Valor_Pos":      float(valor_pos),
                    "TP_pct":         float(tp_pct),
                    "SL_pct":         float(sl_pct),
                    "TP_usd":         float(valor_pos * tp_pct / 100),
                    "SL_usd":         float(valor_pos * sl_pct / 100),
                    "Comision":       float(comision),
                    "Resultado":      resultado,
                    "Ticker_API":     ticker_api.strip().upper(),
                    "Precio_Entrada": float(precio_ent),
                    "Cantidad":       float(cantidad),
                    "TEA":            float(tea_pct / 100) if tea_pct > 0 else 0.0,
                    "Notas":          notas.strip(),
                }
                with st.spinner("Guardando en Firestore…"):
                    ok = fs_post("operaciones", datos)
                if ok:
                    st.success("✓ Operación guardada correctamente en Firestore")
                    st.cache_data.clear()
                    time.sleep(0.8)
                    st.rerun()
                else:
                    st.error("❌ Error guardando. Verifica tu conexión a internet.")
 
    # Editar / eliminar
    mis_ops_e = df_ops if rol=="admin" else (
        df_ops[df_ops["Usuario"]==usuario] if not df_ops.empty and "Usuario" in df_ops.columns
        else pd.DataFrame())
    if not mis_ops_e.empty:
        st.markdown("---")
        section("Editar / eliminar operación")
        labels_e = [f"{r.get('Fecha','?')} — {r.get('Activo','?')} ({r.get('Resultado','?')})"
                    for _,r in mis_ops_e.iterrows()]
        sel = st.selectbox("Selecciona operación", range(len(labels_e)),
                           format_func=lambda i: labels_e[i], key="sel_edit")
        if sel is not None:
            sr   = mis_ops_e.iloc[sel]
            ce1,ce2,ce3 = st.columns(3)
            with ce1:
                cur_res = sr.get("Resultado","Abierta")
                ri = RESULTADOS.index(cur_res) if cur_res in RESULTADOS else 0
                nr = st.selectbox("Cambiar resultado", RESULTADOS, index=ri, key="nr")
                if st.button("✏️ Actualizar resultado"):
                    fs_patch("operaciones", sr["_id"], {"Resultado": nr})
                    st.success("✓ Actualizado"); st.cache_data.clear(); st.rerun()
            with ce2:
                nf = st.date_input("Cambiar fecha", key="nf")
                if st.button("📅 Actualizar fecha"):
                    fs_patch("operaciones", sr["_id"], {"Fecha": str(nf)})
                    st.success("✓ Actualizado"); st.cache_data.clear(); st.rerun()
            with ce3:
                puede = (rol=="admin") or (str(sr.get("Usuario",""))==usuario)
                if puede:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🗑 Eliminar esta operación"):
                        fs_delete("operaciones", sr["_id"])
                        st.success("✓ Eliminada"); st.cache_data.clear(); st.rerun()
 
# ══════════════════════════════════════════════════════════════
# SOCIOS / CAPITAL (admin)
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    with t_soc:
        section("Movimientos de capital — Socios")
 
        with st.form("form_ap", clear_on_submit=True):
            c1,c2,c3,c4 = st.columns(4)
            socio      = c1.text_input("Nombre del socio")
            cedula     = c2.text_input("Cédula / ID")
            tipo_mov   = c3.selectbox("Tipo de movimiento", ["Aporte","Retiro"])
            monto      = c4.number_input("Monto (USD)", min_value=0.0, step=0.01, format="%.2f")
 
            c5,c6 = st.columns(2)
            tipo_cta = c5.selectbox("Tipo de cuenta",
                ["Fondo Grupal", "Portafolio Individual"],
                help="Fondo Grupal: el dinero va al fondo colectivo.\n"
                     "Portafolio Individual: cada persona gestiona su propio portafolio.")
            fecha_a  = c6.date_input("Fecha del movimiento", value=date.today())
 
            if st.form_submit_button("💾 GUARDAR MOVIMIENTO", use_container_width=True):
                if not socio.strip():
                    st.error("❌ Nombre del socio obligatorio")
                else:
                    ok = fs_post("aportes", {
                        "Fondo": fondo, "Socio": socio.strip(),
                        "Cedula": cedula.strip(), "Fecha": str(fecha_a),
                        "Tipo": tipo_mov, "Monto": float(monto),
                        "TipoCuenta": tipo_cta, "Usuario": usuario,
                    })
                    if ok:
                        st.success(f"✓ Movimiento guardado — {tipo_cta}")
                        st.cache_data.clear(); st.rerun()
                    else:
                        st.error("❌ Error guardando")
 
        if not df_ap.empty and "Socio" in df_ap.columns:
            st.markdown("---"); section("Resumen por socio")
            df_soc = df_ap.copy()
            df_soc["Monto_s"] = df_soc.apply(
                lambda r: r["Monto"] if r["Tipo"]=="Aporte" else -r["Monto"], axis=1)
            res = df_soc.groupby(["Socio","Cedula","TipoCuenta"] if "TipoCuenta" in df_soc.columns else ["Socio","Cedula"]).agg(
                Aportes=("Monto_s", lambda x: x[x>0].sum()),
                Retiros=("Monto_s", lambda x: abs(x[x<0].sum())),
                Neto=("Monto_s","sum")
            ).reset_index()
            res["Neto_d"]     = res["Neto"] * factor
            res["Aportes_d"]  = res["Aportes"] * factor
            res["Retiros_d"]  = res["Retiros"] * factor
            total_n = res["Neto"].sum()
            res["% del Fondo"]= (res["Neto"]/total_n*100).round(2) if total_n else 0
            st.dataframe(
                res[["Socio","Cedula","TipoCuenta","Aportes_d","Retiros_d","Neto_d","% del Fondo"]
                    if "TipoCuenta" in res.columns else
                    ["Socio","Cedula","Aportes_d","Retiros_d","Neto_d","% del Fondo"]].rename(columns={
                    "Aportes_d":"Aportes","Retiros_d":"Retiros","Neto_d":"Neto"})
                .style.format({"Aportes":"${:,.2f}","Retiros":"${:,.2f}",
                               "Neto":"${:,.2f}","% del Fondo":"{:.2f}%"}),
                use_container_width=True, hide_index=True)
 
            section("Historial de movimientos")
            cols_h = [c for c in ["Fecha","Socio","Cedula","Tipo","TipoCuenta","Monto"] if c in df_ap.columns]
            dfh = df_ap[cols_h].sort_values("Fecha",ascending=False).copy()
            if "Monto" in dfh.columns: dfh["Monto"] = dfh["Monto"]*factor
            def cr_tipo(v):
                if v=="Aporte":  return "color:#2ECC87;font-weight:600"
                if v=="Retiro":  return "color:#E85555;font-weight:600"
                return ""
            styled_h = dfh.style.format({"Monto":"${:,.2f}"})
            if "Tipo" in dfh.columns:
                styled_h = styled_h.applymap(cr_tipo, subset=["Tipo"])
            st.dataframe(styled_h, use_container_width=True, hide_index=True)
 
            if st.button("🗑 Eliminar último movimiento"):
                lid = df_ap.sort_values("Fecha").iloc[-1]["_id"]
                fs_delete("aportes", lid); st.cache_data.clear(); st.rerun()
 
# ══════════════════════════════════════════════════════════════
# ANÁLISIS
# ══════════════════════════════════════════════════════════════
with t_anal:
    section("Análisis de rendimiento")
    anal_ops = ops_c if rol=="admin" else (
        ops_c[ops_c["Usuario"]==usuario] if not ops_c.empty and "Usuario" in ops_c.columns
        else pd.DataFrame())
 
    if not anal_ops.empty:
        c_a1,c_a2 = st.columns([3,2])
        with c_a1:
            fig_b = go.Figure(go.Bar(
                x=anal_ops.apply(lambda r:f"{r.get('Activo','?')} ({r.get('Fecha','?')})",axis=1),
                y=anal_ops["PnL"],
                marker_color=anal_ops["PnL"].apply(lambda x:"#2ECC87" if x>=0 else "#E85555"),
                text=anal_ops["PnL"].apply(lambda x:f"${x:,.0f}"),
                textposition="outside", textfont=dict(size=10),
                hovertemplate="<b>%{x}</b><br>P&L: $%{y:,.2f}<extra></extra>"))
            fig_b.update_layout(**PLOTLY_THEME,
                title=dict(text="P&L por operación cerrada",font=dict(size=11,color="#8BA5C8"),x=.5))
            st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar":False})
        with c_a2:
            pv = anal_ops["PnL"]
            mejor = anal_ops.loc[pv.idxmax()]
            peor  = anal_ops.loc[pv.idxmin()]
            avg_g = pv[pv>0].mean() if (pv>0).any() else 0
            avg_p = pv[pv<0].mean() if (pv<0).any() else 0
            pf    = abs(pv[pv>0].sum()/pv[pv<0].sum()) if (pv<0).any() else 9.99
            wr2   = (pv>0).sum()/len(pv)*100
            st.markdown(f"""<div style="background:#1a2d42;border:1px solid #2a3f5a;
                border-radius:10px;padding:16px">
              <div style="font:400 9px/2 IBM Plex Mono,mono;color:#8BA5C8;
                          letter-spacing:1.5px;text-transform:uppercase">Estadísticas</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
                <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8">WIN RATE</div>
                  <div style="font:600 18px IBM Plex Mono,mono;color:#9B8EC4">{wr2:.1f}%</div></div>
                <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8">PROFIT FACTOR</div>
                  <div style="font:600 18px IBM Plex Mono,mono;color:#C8A84B">{min(pf,9.99):.2f}x</div></div>
                <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8">AVG GANADORA</div>
                  <div style="font:600 14px IBM Plex Mono,mono;color:#2ECC87">+${avg_g:,.2f}</div></div>
                <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8">AVG PERDEDORA</div>
                  <div style="font:600 14px IBM Plex Mono,mono;color:#E85555">${avg_p:,.2f}</div></div>
                <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8">MEJOR OP.</div>
                  <div style="font:600 12px IBM Plex Mono,mono;color:#2ECC87">{mejor.get('Activo','?')}</div>
                  <div style="font:500 11px IBM Plex Mono,mono;color:#2ECC87">+${mejor['PnL']:,.2f}</div></div>
                <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8">PEOR OP.</div>
                  <div style="font:600 12px IBM Plex Mono,mono;color:#E85555">{peor.get('Activo','?')}</div>
                  <div style="font:500 11px IBM Plex Mono,mono;color:#E85555">${peor['PnL']:,.2f}</div></div>
              </div></div>""", unsafe_allow_html=True)
    else:
        st.info("Aún no hay operaciones cerradas para analizar.")
 
# ══════════════════════════════════════════════════════════════
# GESTIÓN DE USUARIOS (admin)
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    with t_usr:
        section("Gestión de usuarios")
        st.markdown("""<div style="background:#0F1A2B;border:1px solid #2a3f5a;border-left:3px solid #C8A84B;
            border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:16px;
            font:400 12px/1.7 IBM Plex Mono,mono;color:#B0C4DC">
          Aquí creas los accesos para tus clientes. Cada usuario verá solo su fondo.<br>
          La contraseña que pongas aquí es la que ellos usarán para ingresar a la plataforma.
        </div>""", unsafe_allow_html=True)
 
        with st.form("form_user", clear_on_submit=True):
            cu1,cu2 = st.columns(2)
            u_email  = cu1.text_input("Email del usuario (será su login)")
            u_nombre = cu2.text_input("Nombre / Empresa")
 
            cu3,cu4,cu5 = st.columns(3)
            u_pwd      = cu3.text_input("Contraseña inicial", type="password",
                           help="Mínimo 6 caracteres. El usuario puede cambiarla después.")
            u_fondo    = cu4.selectbox("Fondo que puede ver", fondos_list)
            u_tipocta  = cu5.selectbox("Tipo de cuenta",
                ["Fondo Grupal","Portafolio Individual"],
                help="Fondo Grupal: ve el fondo completo compartido.\n"
                     "Portafolio Individual: solo ve sus propias operaciones.")
 
            if st.form_submit_button("👤 CREAR USUARIO Y DAR ACCESO", use_container_width=True):
                if not u_email.strip() or not u_pwd.strip() or not u_nombre.strip():
                    st.error("❌ Email, nombre y contraseña son obligatorios")
                elif len(u_pwd) < 6:
                    st.error("❌ La contraseña debe tener al menos 6 caracteres")
                else:
                    with st.spinner("Creando cuenta en Firebase Auth…"):
                        ok_fb, msg_fb = firebase_crear_usuario(u_email.strip(), u_pwd.strip())
                    if ok_fb:
                        # Guardar perfil en Firestore
                        fs_post("usuarios", {
                            "Email":      u_email.strip().lower(),
                            "Nombre":     u_nombre.strip(),
                            "Fondo":      u_fondo,
                            "TipoCuenta": u_tipocta,
                            "Activo":     "Si",
                            "CreadoPor":  usuario,
                            "Fecha":      str(date.today()),
                        })
                        st.success(f"✓ Usuario creado: **{u_email}** → Fondo: **{u_fondo}** ({u_tipocta})")
                        st.cache_data.clear()
                    else:
                        if "EMAIL_EXISTS" in str(msg_fb):
                            st.warning(f"⚠ El email {u_email} ya tiene cuenta. Se actualizó su perfil de fondo.")
                            fs_post("usuarios", {
                                "Email": u_email.strip().lower(), "Nombre": u_nombre.strip(),
                                "Fondo": u_fondo, "TipoCuenta": u_tipocta,
                                "Activo":"Si","CreadoPor":usuario,"Fecha":str(date.today()),
                            })
                            st.cache_data.clear()
                        else:
                            st.error(f"❌ Error Firebase: {msg_fb}")
 
        # Lista de usuarios registrados
        st.markdown("---"); section("Usuarios con acceso")
        df_us2 = load_usuarios()
        if not df_us2.empty:
            cols_u = [c for c in ["Email","Nombre","Fondo","TipoCuenta","Activo","Fecha"] if c in df_us2.columns]
            st.dataframe(df_us2[cols_u], use_container_width=True, hide_index=True)
 
            section("Desactivar / eliminar usuario")
            us_labels = [f"{r.get('Email','?')} — {r.get('Nombre','?')}" for _,r in df_us2.iterrows()]
            sel_u = st.selectbox("Selecciona usuario", range(len(us_labels)),
                                 format_func=lambda i: us_labels[i], key="sel_usr")
            if sel_u is not None:
                sur = df_us2.iloc[sel_u]
                if st.button("🗑 Eliminar acceso de este usuario"):
                    fs_delete("usuarios", sur["_id"])
                    st.success(f"✓ Acceso eliminado para {sur.get('Email','?')}")
                    st.cache_data.clear(); st.rerun()
        else:
            st.info("Aún no has creado usuarios. Usa el formulario de arriba.")
 
# ══════════════════════════════════════════════════════════════
# ADMINISTRACIÓN (admin)
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    with t_adm:
        section("Panel de administración")
        ca1,ca2 = st.columns(2)
        with ca1:
            section("Resumen por fondo")
            rows_r = []
            for f in fondos_list:
                cap = df_ap_all[df_ap_all["Fondo"]==f]["Monto"].sum() if not df_ap_all.empty else 0
                nop = len(df_ops_all[df_ops_all["Fondo"]==f]) if not df_ops_all.empty else 0
                rows_r.append({"Fondo":f,"Capital USD":cap*factor,"# Ops":nop})
            st.dataframe(pd.DataFrame(rows_r).style.format({"Capital USD":"${:,.2f}"}),
                         use_container_width=True, hide_index=True)
 
            section("Crear nuevo fondo")
            nf_inp = st.text_input("Nombre del nuevo fondo", key="nf_adm")
            if st.button("➕ Crear fondo"):
                if nf_inp.strip() and nf_inp not in fondos_list:
                    fs_post("aportes",{"Fondo":nf_inp.strip(),"Socio":"","Cedula":"",
                                       "Fecha":str(date.today()),"Tipo":"Aporte",
                                       "Monto":0.0,"Usuario":usuario,"TipoCuenta":"Fondo Grupal"})
                    st.success(f"✓ Fondo '{nf_inp}' creado")
                    st.cache_data.clear(); st.rerun()
 
        with ca2:
            section("Estado de APIs")
            st.markdown(f"""<div style="background:#1a2d42;border:1px solid #2a3f5a;
                border-radius:8px;padding:14px;font:400 11px/1.9 IBM Plex Mono,mono">
              <div style="color:#8BA5C8;font-size:9px;letter-spacing:1px;margin-bottom:8px">
                FUENTES ACTIVAS</div>
              <div style="color:#F0C040">● CoinMarketCap API — Cripto</div>
              <div style="color:#C8A84B">● Yahoo Finance (yfinance) — Acciones / ETF</div>
              <div style="color:#2ECC87">● ExchangeRate-API / Frankfurter — TRM</div>
              <div style="color:#8BA5C8;font-size:9px;margin-top:10px">
                TRM actual: ${trm:,.2f} · CMC key: …{CMC_KEY[-6:]}<br>
                Caché precios: 5 min · Caché TRM: 1 hora</div></div>""",
                unsafe_allow_html=True)
 
            if st.button("🔄 Limpiar caché de precios"):
                st.cache_data.clear()
                st.success("✓ Próxima carga trae precios frescos")
 
        st.markdown("---"); section("Todas las operaciones")
        if not df_ops_all.empty:
            cols_a = [c for c in ["Fondo","Usuario","Fecha","Activo","Categoria",
                                   "Valor_Pos","Resultado"] if c in df_ops_all.columns]
            dfa = df_ops_all[cols_a].sort_values("Fecha",ascending=False).copy()
            if "Valor_Pos" in dfa.columns: dfa["Valor_Pos"] = dfa["Valor_Pos"]*factor
            st.dataframe(dfa.style.format({"Valor_Pos":"${:,.2f}"}),
                         use_container_width=True, hide_index=True)
        else:
            st.info("Sin operaciones registradas aún.")
