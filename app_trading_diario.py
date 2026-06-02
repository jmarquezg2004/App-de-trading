import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date
import requests
import time

st.set_page_config(page_title="Arkez — Plataforma", page_icon="⬡", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

html, body { font-family: 'IBM Plex Sans', sans-serif; }
.stApp { background: #111827; color: #ffffff; }
h1 { font-family:'IBM Plex Mono',monospace!important; color:#C8A84B!important; letter-spacing:2px; }
h2 { font-family:'IBM Plex Mono',monospace!important; font-size:11px!important; letter-spacing:1.5px; text-transform:uppercase; color:#8BA5C8!important; }
h3 { font-family:'IBM Plex Mono',monospace!important; font-size:13px!important; color:#C8A84B!important; }
hr { border-color:#1E3354!important; }

section[data-testid="stSidebar"] { background:#0D1929!important; border-right:1px solid #1E3354; }
section[data-testid="stSidebar"] label { color:#B0C4DC!important; font-size:12px!important; }

/* TODOS los inputs — texto blanco */
input, textarea {
    background:#162236!important; color:#ffffff!important;
    -webkit-text-fill-color:#ffffff!important;
    border:1px solid #2a4060!important; border-radius:6px!important;
    font-family:'IBM Plex Mono',monospace!important; font-size:13px!important;
    opacity:1!important;
}
input::placeholder, textarea::placeholder {
    color:#8BA5C8!important; -webkit-text-fill-color:#8BA5C8!important; opacity:1!important;
}
input:focus, textarea:focus { border-color:#C8A84B!important; }
input:disabled {
    color:#C8A84B!important; -webkit-text-fill-color:#C8A84B!important; opacity:1!important;
}

/* Selectbox */
[data-testid="stSelectbox"]>div>div {
    background:#162236!important; border:1px solid #2a4060!important;
    border-radius:6px!important; color:#ffffff!important;
}
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] p { color:#ffffff!important; font-size:13px!important; }

/* Dropdown abierto */
[data-baseweb="popover"], [data-baseweb="popover"] *,
[data-baseweb="menu"], [data-baseweb="menu"] *,
[role="listbox"], [role="listbox"] * {
    background:#1a2d42!important; color:#ffffff!important;
    font-family:'IBM Plex Mono',monospace!important; font-size:13px!important;
    border-color:#2a4060!important;
}
[role="option"]:hover { background:#243b55!important; color:#C8A84B!important; }
[aria-selected="true"] { background:#1e3a5a!important; color:#C8A84B!important; }
[data-baseweb="select"] svg { fill:#8BA5C8!important; }

/* Labels */
[data-testid="stTextInput"] label, [data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label, [data-testid="stDateInput"] label,
[data-testid="stTextArea"] label, [data-testid="stRadio"]>label {
    color:#B0C4DC!important; font-size:13px!important; font-weight:500!important;
}

/* Number input buttons */
[data-testid="stNumberInput"] button {
    background:#1a3050!important; color:#ffffff!important; border-color:#2a4060!important;
}

/* Botones */
.stButton>button {
    background:linear-gradient(135deg,#C8A84B,#A07830)!important;
    color:#0D1929!important; border:none!important; border-radius:6px!important;
    font-family:'IBM Plex Mono',monospace!important; font-weight:600!important;
    letter-spacing:1px!important; text-transform:uppercase!important; font-size:12px!important;
}
.stButton>button:hover { filter:brightness(1.1)!important; }

/* Tabs */
[data-testid="stTabs"] button {
    font-family:'IBM Plex Mono',monospace!important; font-size:11px!important;
    letter-spacing:1px; text-transform:uppercase; color:#8BA5C8!important; background:transparent!important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color:#C8A84B!important; border-bottom:2px solid #C8A84B!important;
}

/* Métricas */
[data-testid="metric-container"] {
    background:#162236; border:1px solid #1E3354; border-radius:10px;
    padding:16px!important; position:relative; overflow:hidden;
}
[data-testid="metric-container"]::before {
    content:''; position:absolute; top:0;left:0;right:0; height:2px;
    background:linear-gradient(90deg,#C8A84B,#A07830);
}
[data-testid="stMetricValue"] {
    font-family:'IBM Plex Mono',monospace!important; font-size:1.4rem!important;
    color:#ffffff!important; font-weight:600!important;
}
[data-testid="stMetricLabel"] {
    font-family:'IBM Plex Mono',monospace!important; font-size:0.68rem!important;
    letter-spacing:1.2px; text-transform:uppercase; color:#8BA5C8!important;
}

/* DataFrames */
[data-testid="stDataFrame"] { border:1px solid #1E3354; border-radius:8px; overflow:hidden; }

/* Alerts */
[data-testid="stAlert"] {
    border-radius:8px!important; border-left-width:3px!important;
    background:#162236!important; font-family:'IBM Plex Mono',monospace!important; color:#ffffff!important;
}

/* Form */
[data-testid="stForm"] {
    background:#0F1A2B!important; border:1px solid #1E3354!important;
    border-radius:10px!important; padding:20px!important;
}

/* Radio */
[data-testid="stRadio"] label span { color:#ffffff!important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# CONSTANTES
# ══════════════════════════════════════════════════════
FIREBASE_KEY = "AIzaSyC52gIJJRTE1B4BqeUwDmaX2fWKS3sSw10"
FS_URL       = "https://firestore.googleapis.com/v1/projects/plataforma-de-inversiones/databases/(default)/documents"
ADMIN_EMAIL  = "jmarquezg2004@gmail.com"
CMC_KEY      = st.secrets.get("CMC_KEY", "d67913f039804c6b900905ebad7c1aaf")

CATEGORIAS = ["Acción", "ETF", "Cripto", "CDT", "Fondo", "Cuenta Remunerada", "Otro"]
MODO_IND   = "Portafolio Individual"
MODO_OBS   = "Observador de Fondo"

# ══════════════════════════════════════════════════════
# FIREBASE AUTH
# ══════════════════════════════════════════════════════
def firebase_login(email, pwd):
    try:
        r = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_KEY}",
            json={"email": email, "password": pwd, "returnSecureToken": True}, timeout=8)
        if r.status_code == 200: return True, r.json()
        return False, r.json().get("error", {}).get("message", "Error")
    except Exception as e: return False, str(e)

def firebase_crear(email, pwd):
    try:
        r = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_KEY}",
            json={"email": email, "password": pwd, "returnSecureToken": True}, timeout=8)
        if r.status_code == 200: return True, "OK"
        return False, r.json().get("error", {}).get("message", "Error")
    except Exception as e: return False, str(e)

# ══════════════════════════════════════════════════════
# FIRESTORE
# ══════════════════════════════════════════════════════
def _f(v):
    if isinstance(v, bool):  return {"booleanValue": v}
    if isinstance(v, int):   return {"integerValue": str(v)}
    if isinstance(v, float): return {"doubleValue": v}
    return {"stringValue": str(v)}

def fs_get(col):
    try:
        r = requests.get(f"{FS_URL}/{col}", timeout=10)
        if r.status_code == 200:
            docs = r.json().get("documents", [])
            rows = [{"_id": d["name"].split("/")[-1],
                     **{k: list(v.values())[0] for k, v in d.get("fields", {}).items()}}
                    for d in docs]
            return pd.DataFrame(rows) if rows else pd.DataFrame()
    except Exception: pass
    return pd.DataFrame()

def fs_post(col, datos):
    try:
        r = requests.post(f"{FS_URL}/{col}",
                          json={"fields": {k: _f(v) for k, v in datos.items()}}, timeout=10)
        if r.status_code in (200, 201): return True, ""
        return False, f"Error {r.status_code}: {r.text[:300]}"
    except Exception as e: return False, str(e)

def fs_patch(col, doc_id, datos):
    mask = "&".join(f"updateMask.fieldPaths={k}" for k in datos)
    try:
        requests.patch(f"{FS_URL}/{col}/{doc_id}?{mask}",
                       json={"fields": {k: _f(v) for k, v in datos.items()}}, timeout=10)
        return True
    except Exception: return False

def fs_delete(col, doc_id):
    try:
        requests.delete(f"{FS_URL}/{col}/{doc_id}", timeout=10)
        return True
    except Exception: return False

# ══════════════════════════════════════════════════════
# PRECIOS
# ══════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def get_trm():
    for url in ["https://open.er-api.com/v6/latest/USD",
                "https://api.frankfurter.app/latest?from=USD&to=COP"]:
        try:
            r = requests.get(url, timeout=6)
            cop = r.json().get("rates", {}).get("COP") if r.status_code == 200 else None
            if cop and float(cop) > 3000: return float(cop)
        except: pass
    try:
        import yfinance as yf
        px = yf.Ticker("USDCOP=X").fast_info.last_price
        if px and px > 3000: return float(px)
    except: pass
    return 4200.0

@st.cache_data(ttl=300)
def get_cmc(syms):
    if not syms: return {}
    try:
        r = requests.get(
            "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest",
            params={"symbol": ",".join(syms), "convert": "USD"},
            headers={"X-CMC_PRO_API_KEY": CMC_KEY, "Accept": "application/json"}, timeout=10)
        if r.status_code != 200: return {}
        out = {}
        for sym, items in r.json().get("data", {}).items():
            item = items[0] if isinstance(items, list) else items
            q = item.get("quote", {}).get("USD", {})
            out[sym.upper()] = {"price": q.get("price", 0), "chg24": q.get("percent_change_24h", 0)}
        return out
    except: return {}

@st.cache_data(ttl=300)
def get_stock(ticker):
    try:
        import yfinance as yf
        info  = yf.Ticker(ticker).fast_info
        price = getattr(info, "last_price", None) or getattr(info, "previous_close", None)
        prev  = getattr(info, "previous_close", price) or price
        chg   = ((price - prev) / prev * 100) if price and prev else 0
        return float(price) if price else None, float(chg)
    except: return None, 0

def get_prices(df):
    out = {}
    if df.empty: return out
    criptos = [x.strip().upper() for x in df[df["Categoria"]=="Cripto"]["Ticker_API"].dropna() if x.strip()]
    if criptos: out.update(get_cmc(tuple(set(criptos))))
    stocks = [x.strip().upper() for x in df[df["Categoria"].isin(["Acción","ETF","Fondo"])]["Ticker_API"].dropna() if x.strip()]
    for t in set(stocks):
        px, chg = get_stock(t)
        if px: out[t] = {"price": px, "chg24": chg}
    return out

# ══════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════
# Estructura de inversión simplificada:
# Fecha_Compra, Activo, Categoria, Cantidad, Precio_Compra, Broker, Ticker_API
# Fecha_Venta (vacío si abierta), Precio_Venta (vacío si abierta)
# Estado: "Abierta" | "Cerrada"

@st.cache_data(ttl=60)
def load_inv():
    df = fs_get("inversiones")
    if df.empty:
        return pd.DataFrame(columns=["_id","Fondo","Usuario","Fecha_Compra","Activo",
                                     "Categoria","Cantidad","Precio_Compra","Broker",
                                     "Ticker_API","Fecha_Venta","Precio_Venta","Estado","Notas"])
    num = ["Cantidad","Precio_Compra","Precio_Venta"]
    for c in num:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
        else: df[c] = 0.0
    for c in ["_id","Fondo","Usuario","Fecha_Compra","Activo","Categoria","Broker",
              "Ticker_API","Fecha_Venta","Estado","Notas"]:
        if c not in df.columns: df[c] = ""
    return df

@st.cache_data(ttl=60)
def load_aportes():
    df = fs_get("aportes")
    if df.empty:
        return pd.DataFrame(columns=["_id","Fondo","Socio","Fecha","Tipo","Monto","Usuario"])
    if "Monto" in df.columns: df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce").fillna(0.0)
    return df

@st.cache_data(ttl=60)
def load_usuarios():
    df = fs_get("usuarios")
    if df.empty:
        return pd.DataFrame(columns=["_id","Email","Nombre","Modo","Fondo","Activo"])
    return df

# ══════════════════════════════════════════════════════
# CÁLCULOS P&L
# ══════════════════════════════════════════════════════
def calcular_posicion(row, prices):
    """Calcula el estado actual de una inversión."""
    ticker  = str(row.get("Ticker_API", "")).strip().upper()
    cat     = str(row.get("Categoria", ""))
    cant    = float(row.get("Cantidad", 0) or 0)
    pc      = float(row.get("Precio_Compra", 0) or 0)
    pv      = float(row.get("Precio_Venta", 0) or 0)
    estado  = str(row.get("Estado", "Abierta"))
    tea_val = 0.0  # para CDT/Remunerada

    costo_total = cant * pc

    if estado == "Cerrada" and pv > 0:
        valor_actual  = cant * pv
        gp_usd        = valor_actual - costo_total
        gp_pct        = gp_usd / costo_total * 100 if costo_total else 0
        px_actual     = pv
        chg24         = 0
        return costo_total, valor_actual, gp_usd, gp_pct, px_actual, chg24

    # Posición abierta
    if cat in ["CDT", "Cuenta Remunerada"]:
        # TEA almacenada como porcentaje anual en Notas o en Precio_Compra
        # Convención: Precio_Compra = TEA decimal (ej: 0.1285)
        tea_val = pc  # en este caso Precio_Compra es la TEA
        try:
            dias = max((pd.Timestamp.now() - pd.to_datetime(row.get("Fecha_Compra"))).days, 0)
            valor_actual = costo_total * ((1 + tea_val) ** (dias / 365))
            gp_usd = valor_actual - costo_total
            gp_pct = gp_usd / costo_total * 100 if costo_total else 0
            return costo_total, valor_actual, gp_usd, gp_pct, tea_val, 0
        except:
            return costo_total, costo_total, 0, 0, tea_val, 0

    if ticker and ticker in prices and prices[ticker].get("price", 0) > 0:
        px  = prices[ticker]["price"]
        chg = prices[ticker].get("chg24", 0)
        valor_actual = cant * px
        gp_usd = valor_actual - costo_total
        gp_pct = gp_usd / costo_total * 100 if costo_total else 0
        return costo_total, valor_actual, gp_usd, gp_pct, px, chg

    return costo_total, costo_total, 0, 0, pc, 0

# ══════════════════════════════════════════════════════
# HELPERS UI
# ══════════════════════════════════════════════════════
PT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Mono", color="#ffffff", size=11),
    margin=dict(l=10, r=10, t=36, b=10),
    xaxis=dict(gridcolor="#1e3350", linecolor="#2a4060", tickfont=dict(color="#8BA5C8")),
    yaxis=dict(gridcolor="#1e3350", linecolor="#2a4060", tickfont=dict(color="#8BA5C8")),
)
CAT_CLR = {"Acción":"#C8A84B","ETF":"#2ECC87","Cripto":"#E87844",
           "CDT":"#6BA3BE","Fondo":"#9B8EC4","Cuenta Remunerada":"#F0C040","Otro":"#8BA5C8"}

def money(v, f=1):
    v2 = v * f
    if abs(v2) >= 1e6: return f"${v2/1e6:.2f}M"
    return f"${v2:,.2f}"

def card(label, val, sub=None, color="#C8A84B"):
    s = f'<div style="font:500 11px/1.4 IBM Plex Mono,mono;color:{color};margin-top:3px">{sub}</div>' if sub else ""
    return f"""<div style="background:#162236;border:1px solid #1E3354;border-radius:10px;
        padding:16px 18px;position:relative;overflow:hidden;height:100%">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;background:{color}"></div>
      <div style="font:400 9px/1 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1.5px;
                  text-transform:uppercase;margin-bottom:8px">{label}</div>
      <div style="font:600 22px/1 IBM Plex Mono,mono;color:#ffffff">{val}</div>{s}</div>"""

def sec(t):
    st.markdown(f'<h2 style="margin:18px 0 10px">{t}</h2>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("""<div style="text-align:center;padding:50px 0 24px">
      <div style="display:inline-block;width:52px;height:52px;margin-bottom:14px;
                  background:linear-gradient(135deg,#C8A84B,#A07830);
                  clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%)"></div>
      <div style="font:600 28px/1 IBM Plex Mono,mono;color:#C8A84B;letter-spacing:3px">ARKEZ</div>
      <div style="font:400 11px/1.5 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:2px;margin-top:6px">
        PLATAFORMA · ACCESO PRIVADO</div></div>""", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1.2,1])
    with col:
        email = st.text_input("Correo electrónico", placeholder="usuario@email.com")
        pwd   = st.text_input("Contraseña", type="password")
        if st.button("ENTRAR →", use_container_width=True):
            if email and pwd:
                with st.spinner("Verificando…"):
                    ok, result = firebase_login(email, pwd)
                if ok:
                    em  = email.strip().lower()
                    rol = "admin" if em == ADMIN_EMAIL.lower() else "usuario"
                    df_u = load_usuarios()
                    modo_u = MODO_IND; fondo_u = None
                    if not df_u.empty and "Email" in df_u.columns:
                        fila = df_u[df_u["Email"].str.lower() == em]
                        if not fila.empty:
                            modo_u  = fila.iloc[0].get("Modo", MODO_IND)
                            fondo_u = fila.iloc[0].get("Fondo") or None
                    st.session_state.update({"logged_in":True,"usuario":em,"rol":rol,
                                             "modo":modo_u,"fondo_asignado":fondo_u,
                                             "fondo_sel":"Arkez Invest"})
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
            else:
                st.warning("Completa los dos campos")
    st.stop()

# ══════════════════════════════════════════════════════
# SESIÓN Y DATOS
# ══════════════════════════════════════════════════════
rol    = st.session_state.rol
usuario= st.session_state.usuario
modo   = st.session_state.get("modo", MODO_IND)
fa     = st.session_state.get("fondo_asignado")

df_inv_all  = load_inv()
df_ap_all   = load_aportes()
df_usr_all  = load_usuarios()

fondos_set  = (set(df_ap_all["Fondo"].dropna()) | set(df_inv_all["Fondo"].dropna())) - {""}
fondos_list = sorted(fondos_set) or ["Arkez Invest"]
if "Arkez Invest" not in fondos_list: fondos_list.insert(0, "Arkez Invest")

# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""<div style="text-align:center;padding:14px 0 10px">
      <div style="display:inline-block;width:34px;height:34px;margin-bottom:7px;
                  background:linear-gradient(135deg,#C8A84B,#A07830);
                  clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%)"></div>
      <div style="font:600 14px/1 IBM Plex Mono,mono;color:#C8A84B;letter-spacing:3px">ARKEZ</div>
    </div>""", unsafe_allow_html=True)

    rc = "#C8A84B" if rol=="admin" else "#2ECC87"
    st.markdown(f"""<div style="background:#152034;border:1px solid #1E3354;border-radius:8px;
        padding:10px 12px;margin-bottom:10px">
      <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px;margin-bottom:3px">USUARIO</div>
      <div style="font:400 11px/1.4 IBM Plex Mono,mono;color:#ffffff;word-break:break-all">{usuario}</div>
      <span style="display:inline-block;margin-top:4px;background:rgba(200,168,75,.12);color:{rc};
                   border:1px solid {rc};padding:1px 9px;border-radius:20px;
                   font:600 9px/1.8 IBM Plex Mono,mono">
        {'⬡ ADMIN' if rol=='admin' else '● '+modo.split()[0].upper()}</span></div>""",
        unsafe_allow_html=True)

    if rol == "admin":
        idx = fondos_list.index(st.session_state.get("fondo_sel","Arkez Invest")) \
              if st.session_state.get("fondo_sel") in fondos_list else 0
        fondo = st.selectbox("🏦 Fondo activo", fondos_list, index=idx)
        st.session_state.fondo_sel = fondo
    else:
        if fa and fa in fondos_list:
            fondo = fa
        else:
            fondo = f"personal_{usuario.split('@')[0]}"
        st.markdown(f"""<div style="background:#152034;border:1px solid #1E3354;border-radius:6px;
            padding:8px 12px;margin-bottom:8px">
          <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8">FONDO / PORTAFOLIO</div>
          <div style="font:600 12px IBM Plex Mono,mono;color:#C8A84B">{fondo}</div>
        </div>""", unsafe_allow_html=True)

    trm = get_trm()
    st.markdown(f"""<div style="background:#152034;border:1px solid #1E3354;border-radius:8px;
        padding:9px 12px;margin:8px 0">
      <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">TRM USD/COP</div>
      <div style="font:600 16px/1.5 IBM Plex Mono,mono;color:#F0C040">${trm:,.2f}</div>
    </div>""", unsafe_allow_html=True)

    moneda = st.radio("Moneda", ["USD","COP"], horizontal=True)
    factor = trm if moneda=="COP" else 1.0
    sfx    = " COP" if moneda=="COP" else " USD"

    st.markdown("---")
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# ══════════════════════════════════════════════════════
# FILTRAR DATOS
# ══════════════════════════════════════════════════════
def inv_visibles(df):
    if df.empty: return df
    if rol == "admin": return df[df["Fondo"]==fondo]
    if modo == MODO_OBS: return df[df["Fondo"]==fondo]
    # Portafolio individual: sus propias inversiones
    mask = pd.Series([False]*len(df))
    if "Usuario" in df.columns: mask = mask | (df["Usuario"]==usuario)
    if "Fondo" in df.columns:   mask = mask | (df["Fondo"]==fondo)
    return df[mask]

df_inv = inv_visibles(df_inv_all).copy()
df_ap  = df_ap_all[df_ap_all["Fondo"]==fondo].copy() if not df_ap_all.empty else pd.DataFrame()
prices = get_prices(df_inv)

# Calcular todas las posiciones
posiciones = []
total_invertido = 0
total_actual    = 0
total_gp        = 0

for _, row in df_inv.iterrows():
    inv, act, gp, gp_pct, px, chg = calcular_posicion(row, prices)
    total_invertido += inv
    total_actual    += act
    total_gp        += gp
    posiciones.append({
        "Activo":     row.get("Activo","—"),
        "Categoria":  row.get("Categoria","—"),
        "Ticker":     row.get("Ticker_API","—"),
        "Estado":     row.get("Estado","Abierta"),
        "F_Compra":   row.get("Fecha_Compra","—"),
        "F_Venta":    row.get("Fecha_Venta",""),
        "Cantidad":   float(row.get("Cantidad",0) or 0),
        "Px_Compra":  float(row.get("Precio_Compra",0) or 0),
        "Px_Actual":  px,
        "Chg24":      chg,
        "Invertido":  inv,
        "Val_Actual": act,
        "GP_usd":     gp,
        "GP_pct":     gp_pct,
        "_id":        row.get("_id",""),
        "Usuario":    row.get("Usuario","—"),
    })

rend_pct = total_gp / total_invertido * 100 if total_invertido > 0 else 0

pos_abiertas = [p for p in posiciones if p["Estado"]=="Abierta"]
pos_cerradas = [p for p in posiciones if p["Estado"]=="Cerrada"]

# ══════════════════════════════════════════════════════
# HEADER + KPIs
# ══════════════════════════════════════════════════════
badge = ""
if rol != "admin":
    badge = ' <span style="font:600 9px IBM Plex Mono,mono;background:rgba(46,204,135,.12);color:#2ECC87;border:1px solid #2ECC87;padding:1px 7px;border-radius:20px">PORTAFOLIO PERSONAL</span>' \
            if modo == MODO_IND else \
            ' <span style="font:600 9px IBM Plex Mono,mono;background:rgba(155,142,196,.12);color:#9B8EC4;border:1px solid #9B8EC4;padding:1px 7px;border-radius:20px">SOLO LECTURA</span>'

st.markdown(f"""<div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:4px">
  <div style="width:36px;height:36px;flex-shrink:0;background:linear-gradient(135deg,#C8A84B,#A07830);
              clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%)"></div>
  <div>
    <div style="font:600 18px/1 IBM Plex Mono,mono;color:#C8A84B;letter-spacing:2px">
      {fondo.upper()}{badge}</div>
    <div style="font:400 10px/1.5 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">
      ARKEZ · PLATAFORMA · PRECIOS EN TIEMPO REAL</div>
  </div>
  <div style="margin-left:auto;font:400 10px IBM Plex Mono,mono;color:#8BA5C8">
    {datetime.now().strftime('%d/%m/%Y %H:%M')}</div></div>
<hr style="margin:12px 0 18px">""", unsafe_allow_html=True)

# ── FILTRO DE PERIODO ──────────────────────────────────
col_per1, col_per2, col_per3 = st.columns([2,2,4])
with col_per1:
    periodo = st.selectbox("📅 Ver período",
        ["Todo el historial","Este mes","Este año",
         "Última semana","Últimos 3 meses","Personalizado"],
        key="periodo_sel")
with col_per2:
    if periodo == "Personalizado":
        fecha_desde = st.date_input("Desde", value=date(date.today().year,1,1), key="f_desde")
        fecha_hasta = st.date_input("Hasta", value=date.today(), key="f_hasta")
    else:
        fecha_desde = None
        fecha_hasta = None

# Calcular rango de fechas según periodo
hoy = pd.Timestamp.now().normalize()
if   periodo == "Este mes":        f_ini = hoy.replace(day=1);              f_fin = hoy
elif periodo == "Este año":        f_ini = hoy.replace(month=1,day=1);      f_fin = hoy
elif periodo == "Última semana":   f_ini = hoy - pd.Timedelta(days=7);      f_fin = hoy
elif periodo == "Últimos 3 meses": f_ini = hoy - pd.Timedelta(days=90);     f_fin = hoy
elif periodo == "Personalizado" and fecha_desde and fecha_hasta:
    f_ini = pd.Timestamp(fecha_desde); f_fin = pd.Timestamp(fecha_hasta)
else:
    f_ini = None; f_fin = None  # Todo el historial

# Aplicar filtro de periodo a las posiciones
def en_periodo(p):
    if f_ini is None: return True
    try:
        fc = pd.to_datetime(p["F_Compra"])
        fv = pd.to_datetime(p["F_Venta"]) if p["F_Venta"] else hoy
        # Incluir si hay superposición con el rango
        return fc <= f_fin and fv >= f_ini
    except: return True

pos_periodo   = [p for p in posiciones if en_periodo(p) and p["Estado"] != "Archivada"]
pos_ab_per    = [p for p in pos_periodo if p["Estado"] == "Abierta"]
pos_cer_per   = [p for p in pos_periodo if p["Estado"] == "Cerrada"]
inv_per       = sum(p["Invertido"]  for p in pos_periodo)
act_per       = sum(p["Val_Actual"] for p in pos_periodo)
gp_per        = sum(p["GP_usd"]     for p in pos_periodo)
rend_per      = gp_per / inv_per * 100 if inv_per > 0 else 0

# Badge de periodo
per_badge = f'<span style="font:400 10px IBM Plex Mono,mono;color:#8BA5C8;margin-left:8px">Período: {periodo}</span>'
if f_ini:
    per_badge = f'<span style="font:400 10px IBM Plex Mono,mono;color:#8BA5C8;margin-left:8px">{f_ini.strftime("%d/%m/%Y")} → {f_fin.strftime("%d/%m/%Y")}</span>'

st.markdown(f'<div style="margin:4px 0 12px">{per_badge}</div>', unsafe_allow_html=True)

gc = "#2ECC87" if gp_per >= 0 else "#E85555"
k1,k2,k3,k4,k5 = st.columns(5)
with k1: st.markdown(card("Portafolio actual",   money(act_per,factor)+sfx), unsafe_allow_html=True)
with k2: st.markdown(card("Total invertido",     money(inv_per,factor)+sfx, color="#8BA5C8"), unsafe_allow_html=True)
with k3: st.markdown(card("Ganancia / Pérdida",
    f"{'+'if gp_per>=0 else ''}{money(gp_per,factor)}{sfx}",
    f"{'▲' if rend_per>=0 else '▼'} {abs(rend_per):.2f}%", color=gc), unsafe_allow_html=True)
with k4: st.markdown(card("Posiciones abiertas", str(len(pos_ab_per)),
    f"{len(pos_cer_per)} cerradas en período", color="#F0C040"), unsafe_allow_html=True)
with k5:
    ganadoras_per = sum(1 for p in pos_cer_per if p["GP_usd"] > 0)
    wr = ganadoras_per/len(pos_cer_per)*100 if pos_cer_per else 0
    st.markdown(card("Win rate", f"{wr:.1f}%",
        f"{ganadoras_per}/{len(pos_cer_per)} cerradas en verde", color="#9B8EC4"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════
puede_registrar = (rol=="admin") or (modo==MODO_IND)

if rol == "admin":
    tabs = st.tabs(["⬡ Dashboard","◈ Portafolio","📌 Registrar","💰 Capital","👥 Usuarios","⚙ Admin"])
    t_dash,t_port,t_reg,t_cap,t_usr,t_adm = tabs
elif puede_registrar:
    tabs = st.tabs(["⬡ Dashboard","◈ Mi portafolio","📌 Registrar"])
    t_dash,t_port,t_reg = tabs
else:
    tabs = st.tabs(["⬡ Dashboard","◈ Portafolio"])
    t_dash,t_port = tabs

# ══════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════
with t_dash:
    cl, cr = st.columns([3,2])

    with cl:
        sec("Evolución del portafolio")
        # Construir serie temporal: para cada inversión, agregar su valor en cada fecha
        if pos_periodo:
            # Puntos clave: fecha compra y hoy (o fecha venta si cerrada)
            puntos = []
            for p in pos_periodo:
                try:
                    fc = pd.to_datetime(p["F_Compra"])
                    # En la fecha de compra: valor = invertido
                    puntos.append({"fecha": fc, "valor": p["Invertido"]})
                    # Hoy o fecha venta: valor actual
                    fv = pd.to_datetime(p["F_Venta"]) if p["F_Venta"] else pd.Timestamp.now()
                    puntos.append({"fecha": fv, "valor": p["Val_Actual"]})
                except: pass

            if puntos:
                df_ev = pd.DataFrame(puntos).sort_values("fecha")
                df_ev = df_ev.groupby("fecha")["valor"].sum().reset_index()
                df_ev["valor"] = df_ev["valor"] * factor

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_ev["fecha"], y=df_ev["valor"],
                    mode="lines+markers",
                    line=dict(color="#C8A84B", width=2.5),
                    fill="tozeroy", fillcolor="rgba(200,168,75,0.08)",
                    marker=dict(color="#C8A84B", size=6),
                    name="Valor portafolio",
                    hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:$,.0f}"+sfx+"<extra></extra>"
                ))
                # Línea de costo (invertido)
                df_cost = pd.DataFrame(puntos).sort_values("fecha")
                df_cost = df_cost.groupby("fecha")["valor"].first().reset_index()
                fig.add_trace(go.Scatter(
                    x=df_ev["fecha"],
                    y=[total_invertido * factor] * len(df_ev),
                    mode="lines",
                    line=dict(color="#8BA5C8", width=1, dash="dash"),
                    name="Capital invertido",
                    hovertemplate="Capital: %{y:$,.0f}"+sfx+"<extra></extra>"
                ))
                fig.update_layout(**PT,
                    title=dict(text=f"Valor del portafolio ({moneda})",
                               font=dict(size=11,color="#8BA5C8"),x=.5),
                    yaxis_title=moneda,
                    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8BA5C8", size=10)))
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        else:
            st.info("Registra tu primera inversión para ver la gráfica.")

    with cr:
        sec("Distribución por tipo")
        if posiciones:
            dist = {}
            for p in posiciones:
                cat = p["Categoria"]
                dist[cat] = dist.get(cat,0) + p["Val_Actual"]
            if dist:
                fig2 = go.Figure(go.Pie(
                    labels=list(dist.keys()),
                    values=[v*factor for v in dist.values()],
                    hole=.6,
                    marker=dict(colors=[CAT_CLR.get(c,"#8BA5C8") for c in dist.keys()],
                                line=dict(color="#111827",width=2)),
                    hovertemplate="<b>%{label}</b><br>%{value:$,.0f}"+sfx+"<br>%{percent}<extra></extra>",
                    textfont=dict(color="#ffffff")
                ))
                fig2.update_layout(**PT,
                    title=dict(text="Por categoría",font=dict(size=11,color="#8BA5C8"),x=.5))
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

    # Precios en tiempo real
    if prices:
        sec("Precios en tiempo real")
        cols_p = st.columns(min(len(prices),5))
        for i,(tk,d) in enumerate(list(prices.items())[:10]):
            chg=d.get("chg24",0); px=d.get("price",0)
            clr="#2ECC87" if chg>=0 else "#E85555"
            pxs=f"${px:,.4f}" if px<10 else f"${px:,.2f}"
            with cols_p[i%min(len(prices),5)]:
                st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
                    border-radius:8px;padding:12px;text-align:center;margin-bottom:8px">
                  <div style="font:600 11px/1.5 IBM Plex Mono,mono;color:#C8A84B">{tk}</div>
                  <div style="font:600 15px/1.4 IBM Plex Mono,mono;color:#ffffff">{pxs}</div>
                  <div style="font:400 10px/1.3 IBM Plex Mono,mono;color:{clr}">
                    {'▲' if chg>=0 else '▼'} {abs(chg):.2f}%</div></div>""",
                    unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# PORTAFOLIO — posiciones con P&L en vivo
# ══════════════════════════════════════════════════════
with t_port:
    if pos_ab_per:
        sec("Posiciones abiertas — P&L en tiempo real")
        for p in pos_ab_per:
            gc2 = "#2ECC87" if p["GP_usd"]>=0 else "#E85555"
            sg  = "+" if p["GP_usd"]>=0 else ""
            pxd = prices.get(p["Ticker"].upper(), {})
            px_str = f"${p['Px_Actual']:,.4f}" if p["Px_Actual"]<10 else f"${p['Px_Actual']:,.2f}"
            chg_str = f"{'▲' if p['Chg24']>=0 else '▼'} {abs(p['Chg24']):.2f}%" if p["Chg24"]!=0 else "—"
            chg_clr = "#2ECC87" if p["Chg24"]>=0 else "#E85555"

            st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
                border-radius:10px;padding:14px 18px;margin-bottom:10px;
                display:flex;align-items:center;gap:16px;flex-wrap:wrap">
              <div style="min-width:120px">
                <div style="font:600 15px/1.3 IBM Plex Mono,mono;color:#C8A84B">{p['Activo']}</div>
                <div style="font:400 10px/1.4 IBM Plex Mono,mono;color:#8BA5C8">
                  {p['Ticker']} · {p['Categoria']}</div>
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">Compra: {p['F_Compra']}</div>
              </div>
              <div style="text-align:center;min-width:80px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">CANTIDAD</div>
                <div style="font:500 13px IBM Plex Mono,mono;color:#ffffff">{p['Cantidad']:,.4f}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">PX COMPRA</div>
                <div style="font:500 13px IBM Plex Mono,mono;color:#ffffff">${p['Px_Compra']:,.4f}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">PX ACTUAL</div>
                <div style="font:500 13px IBM Plex Mono,mono;color:#ffffff">{px_str}</div>
                <div style="font:400 9px IBM Plex Mono,mono;color:{chg_clr}">{chg_str} 24h</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">INVERTIDO</div>
                <div style="font:500 13px IBM Plex Mono,mono;color:#ffffff">{money(p['Invertido'],factor)}{sfx}</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">VALOR HOY</div>
                <div style="font:600 14px IBM Plex Mono,mono;color:#ffffff">{money(p['Val_Actual'],factor)}{sfx}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">P&L</div>
                <div style="font:600 15px IBM Plex Mono,mono;color:{gc2}">{sg}{money(p['GP_usd'],factor)}{sfx}</div>
                <div style="font:500 10px IBM Plex Mono,mono;color:{gc2}">{sg}{p['GP_pct']:.2f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)

    if pos_cer_per:
        sec("Posiciones cerradas")
        for p in pos_cer_per:
            gc3 = "#2ECC87" if p["GP_usd"]>=0 else "#E85555"
            sg3 = "+" if p["GP_usd"]>=0 else ""
            st.markdown(f"""<div style="background:#0F1A2B;border:1px solid #1E3354;
                border-radius:10px;padding:12px 18px;margin-bottom:8px;
                display:flex;align-items:center;gap:16px;flex-wrap:wrap;opacity:.9">
              <div style="min-width:120px">
                <div style="font:600 14px/1.3 IBM Plex Mono,mono;color:#8BA5C8">{p['Activo']}</div>
                <div style="font:400 10px IBM Plex Mono,mono;color:#4a6f8a">{p['Ticker']} · {p['Categoria']}</div>
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">
                  {p['F_Compra']} → {p['F_Venta']}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">PX COMPRA</div>
                <div style="font:500 12px IBM Plex Mono,mono;color:#8BA5C8">${p['Px_Compra']:,.4f}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">PX VENTA</div>
                <div style="font:500 12px IBM Plex Mono,mono;color:#8BA5C8">${p['Px_Actual']:,.4f}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">INVERTIDO</div>
                <div style="font:500 12px IBM Plex Mono,mono;color:#8BA5C8">{money(p['Invertido'],factor)}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">RECUPERADO</div>
                <div style="font:500 12px IBM Plex Mono,mono;color:#8BA5C8">{money(p['Val_Actual'],factor)}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">RESULTADO</div>
                <div style="font:600 14px IBM Plex Mono,mono;color:{gc3}">{sg3}{money(p['GP_usd'],factor)}{sfx}</div>
                <div style="font:500 10px IBM Plex Mono,mono;color:{gc3}">{sg3}{p['GP_pct']:.2f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)

    if not posiciones:
        st.info("Aún no tienes inversiones registradas.")

# ══════════════════════════════════════════════════════
# REGISTRAR INVERSIÓN
# ══════════════════════════════════════════════════════
if puede_registrar:
    with t_reg:
        sec("Registrar compra de activo")
        st.markdown(f'<div style="font:400 11px/1.5 IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:10px">'
                    f'Usuario: <strong style="color:#C8A84B">{usuario}</strong> · '
                    f'Fondo: <strong style="color:#C8A84B">{fondo}</strong></div>',
                    unsafe_allow_html=True)

        with st.form("form_compra", clear_on_submit=True):
            c1,c2,c3 = st.columns(3)
            fecha_c   = c1.date_input("📅 Fecha de compra", value=date.today())
            activo    = c2.text_input("Nombre del activo", placeholder="Apple, Bitcoin, VTI…")
            categoria = c3.selectbox("Categoría", CATEGORIAS)

            c4,c5,c6 = st.columns(3)
            precio_c  = c4.number_input("Precio de compra (USD)", min_value=0.0, step=0.0001, format="%.4f",
                                         help="Para CDT/Remunerada: ingresa la TEA decimal (ej: 0.1285 = 12.85%)")
            valor_pos = c5.number_input("Capital invertido (USD)", min_value=0.0, step=0.01, format="%.2f")
            broker    = c6.text_input("Broker / Exchange", placeholder="Schwab, Binance…")

            c7,c8 = st.columns(2)
            ticker_api = c7.text_input("Ticker para precio en vivo",
                                        placeholder="AAPL · BTC · VTI · ETH",
                                        help="Símbolo exacto: acciones → AAPL, cripto → BTC")
            notas = c8.text_input("Notas (opcional)")

            # Cantidad calculada automáticamente
            qty = round(valor_pos / precio_c, 8) if precio_c > 0 and valor_pos > 0 else 0.0
            st.text_input("Cantidad / Unidades (calculada automáticamente)",
                          value=f"{qty:,.8f}  =  ${valor_pos:,.2f} ÷ ${precio_c:,.4f}",
                          disabled=True)

            if st.form_submit_button("💾 REGISTRAR COMPRA", use_container_width=True):
                if not activo.strip():
                    st.error("❌ El nombre del activo es obligatorio")
                elif precio_c <= 0 or valor_pos <= 0:
                    st.error("❌ El precio y el capital invertido deben ser mayores a 0")
                else:
                    ok, msg = fs_post("inversiones", {
                        "Fondo":         fondo,
                        "Usuario":       usuario,
                        "Fecha_Compra":  str(fecha_c),
                        "Activo":        activo.strip(),
                        "Categoria":     categoria,
                        "Cantidad":      float(qty),
                        "Precio_Compra": float(precio_c),
                        "Broker":        broker.strip(),
                        "Ticker_API":    ticker_api.strip().upper(),
                        "Fecha_Venta":   "",
                        "Precio_Venta":  0.0,
                        "Estado":        "Abierta",
                        "Notas":         notas.strip(),
                    })
                    if ok:
                        st.success(f"✓ Compra de {activo} registrada — {qty:,.4f} unidades a ${precio_c:,.4f}")
                        st.cache_data.clear(); time.sleep(0.5); st.rerun()
                    else:
                        st.error(f"❌ Error Firestore: {msg}")

        # ── REGISTRAR VENTA ──
        if posiciones:
            abiertas_lista = [p for p in posiciones if p["Estado"]=="Abierta" and p["Estado"]!="Archivada"]
            if abiertas_lista:
                st.markdown("---")
                sec("Registrar venta de activo")
                lbs = [f"{p['F_Compra']} — {p['Activo']} ({p['Cantidad']:,.4f} unidades)" for p in abiertas_lista]
                sel = st.selectbox("Selecciona la posición a vender", range(len(lbs)),
                                   format_func=lambda i: lbs[i])
                pos_sel = abiertas_lista[sel]

                cv1,cv2 = st.columns(2)
                fecha_v  = cv1.date_input("📅 Fecha de venta", value=date.today())
                precio_v = cv2.number_input("Precio de venta (USD)", min_value=0.0,
                                             step=0.0001, format="%.4f")

                if precio_v > 0:
                    gp_venta = (precio_v - pos_sel["Px_Compra"]) * pos_sel["Cantidad"]
                    gp_pct_v = gp_venta / pos_sel["Invertido"] * 100 if pos_sel["Invertido"] else 0
                    clr_v    = "#2ECC87" if gp_venta >= 0 else "#E85555"
                    st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
                        border-radius:8px;padding:12px 16px;margin:8px 0;
                        display:flex;gap:24px;flex-wrap:wrap">
                      <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8">RESULTADO VENTA</div>
                        <div style="font:600 16px IBM Plex Mono,mono;color:{clr_v}">
                          {'+'if gp_venta>=0 else ''}{money(gp_venta,factor)}{sfx}</div></div>
                      <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8">RENTABILIDAD</div>
                        <div style="font:600 16px IBM Plex Mono,mono;color:{clr_v}">
                          {'+'if gp_pct_v>=0 else ''}{gp_pct_v:.2f}%</div></div>
                      <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8">CAPITAL RECUPERADO</div>
                        <div style="font:600 16px IBM Plex Mono,mono;color:#ffffff">
                          {money(precio_v*pos_sel['Cantidad'],factor)}{sfx}</div></div>
                    </div>""", unsafe_allow_html=True)

                if st.button("💰 CONFIRMAR VENTA", use_container_width=True):
                    if precio_v <= 0:
                        st.error("❌ Ingresa el precio de venta")
                    else:
                        ok = fs_patch("inversiones", pos_sel["_id"], {
                            "Estado":       "Cerrada",
                            "Fecha_Venta":  str(fecha_v),
                            "Precio_Venta": float(precio_v),
                        })
                        if ok:
                            st.success(f"✓ Venta de {pos_sel['Activo']} registrada el {fecha_v}")
                            st.cache_data.clear(); time.sleep(0.5); st.rerun()
                        else:
                            st.error("❌ Error actualizando")

            # Archivar posición (nunca se borra — se marca como Archivada)
            st.markdown("---")
            sec("Archivar posición")
            st.markdown('''<div style="font:400 11px IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:8px">
              Las posiciones archivadas se ocultan del portafolio activo pero quedan guardadas
              en el historial completo. Nunca se eliminan datos.</div>''', unsafe_allow_html=True)
            all_lbs = [f"{p['F_Compra']} — {p['Activo']} ({p['Estado']})" for p in posiciones
                       if p["Estado"] != "Archivada"]
            all_ids = [p["_id"] for p in posiciones if p["Estado"] != "Archivada"]
            if all_lbs:
                arc_sel = st.selectbox("Selecciona posición a archivar", range(len(all_lbs)),
                                       format_func=lambda i: all_lbs[i], key="arc_pos")
                if st.button("📦 Archivar posición"):
                    fs_patch("inversiones", all_ids[arc_sel], {"Estado": "Archivada"})
                    st.success("✓ Archivada — sigue en el historial completo")
                    st.cache_data.clear(); st.rerun()

# ══════════════════════════════════════════════════════
# CAPITAL / SOCIOS (admin)
# ══════════════════════════════════════════════════════
if rol == "admin":
    with t_cap:
        sec("Movimientos de capital — Socios")
        with st.form("form_ap", clear_on_submit=True):
            c1,c2,c3,c4 = st.columns(4)
            socio    = c1.text_input("Nombre del socio")
            cedula   = c2.text_input("Cédula / ID")
            tipo_mov = c3.selectbox("Tipo", ["Aporte","Retiro"])
            monto    = c4.number_input("Monto (USD)", min_value=0.0, step=0.01, format="%.2f")
            fecha_a  = st.date_input("Fecha", value=date.today())
            if st.form_submit_button("💾 GUARDAR", use_container_width=True):
                if not socio.strip():
                    st.error("❌ Nombre obligatorio")
                else:
                    ok, msg = fs_post("aportes", {
                        "Fondo": fondo, "Socio": socio.strip(), "Cedula": cedula.strip(),
                        "Fecha": str(fecha_a), "Tipo": tipo_mov,
                        "Monto": float(monto), "Usuario": usuario,
                    })
                    if ok: st.success("✓ Guardado"); st.cache_data.clear(); st.rerun()
                    else:  st.error(f"❌ {msg}")

        if not df_ap.empty and "Socio" in df_ap.columns:
            st.markdown("---"); sec("Historial de movimientos")
            dfh = df_ap[["Fecha","Socio","Cedula","Tipo","Monto"]].sort_values("Fecha",ascending=False).copy()
            dfh["Monto"] = dfh["Monto"] * factor
            def ct(v):
                if v=="Aporte":  return "color:#2ECC87;font-weight:600"
                if v=="Retiro":  return "color:#E85555;font-weight:600"
                return ""
            st.dataframe(dfh.style.map(ct,subset=["Tipo"]).format({"Monto":"${:,.2f}"}),
                         use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════
# USUARIOS (admin)
# ══════════════════════════════════════════════════════
if rol == "admin":
    with t_usr:
        sec("Gestión de usuarios")
        st.markdown("""<div style="background:#162236;border:1px solid #1E3354;border-left:3px solid #C8A84B;
            border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:14px;
            font:400 12px/1.7 IBM Plex Mono,mono;color:#B0C4DC">
          <strong>Portafolio Individual</strong> → el usuario entra y registra sus propias inversiones.<br>
          <strong>Observador de Fondo</strong> → solo lectura. Ve el fondo asignado sin poder editar.
        </div>""", unsafe_allow_html=True)

        with st.form("form_usr", clear_on_submit=True):
            cu1,cu2 = st.columns(2)
            u_email  = cu1.text_input("Email del usuario")
            u_nombre = cu2.text_input("Nombre / Empresa")
            cu3,cu4,cu5 = st.columns(3)
            u_pwd   = cu3.text_input("Contraseña inicial", type="password", help="Mínimo 6 caracteres")
            u_modo  = cu4.selectbox("Modo de acceso", [MODO_IND, MODO_OBS])
            u_f_opts= ["(Sin fondo — portafolio personal)"] + fondos_list
            u_fsel  = cu5.selectbox("Fondo asignado (opcional)", u_f_opts)
            u_fondo = "" if u_fsel.startswith("(Sin") else u_fsel

            if st.form_submit_button("👤 CREAR USUARIO", use_container_width=True):
                if not u_email.strip() or not u_nombre.strip() or not u_pwd.strip():
                    st.error("❌ Email, nombre y contraseña obligatorios")
                elif len(u_pwd) < 6:
                    st.error("❌ Contraseña mínimo 6 caracteres")
                elif u_modo == MODO_OBS and not u_fondo:
                    st.error("❌ Observador de Fondo requiere un fondo asignado")
                else:
                    with st.spinner("Creando en Firebase…"):
                        ok_fb, msg_fb = firebase_crear(u_email.strip(), u_pwd.strip())
                    if ok_fb or "EMAIL_EXISTS" in str(msg_fb):
                        fs_post("usuarios", {
                            "Email": u_email.strip().lower(), "Nombre": u_nombre.strip(),
                            "Modo": u_modo, "Fondo": u_fondo, "Activo": "Si",
                            "CreadoPor": usuario, "Fecha": str(date.today()),
                        })
                        lbl = "EMAIL_EXISTS" in str(msg_fb) and "actualizado" or "creado"
                        st.success(f"✓ Usuario {lbl}: {u_email} → {u_modo}" +
                                   (f" · Fondo: {u_fondo}" if u_fondo else " · Portafolio personal"))
                        st.cache_data.clear()
                    else:
                        st.error(f"❌ Firebase: {msg_fb}")

        df_u2 = load_usuarios()
        if not df_u2.empty:
            st.markdown("---"); sec("Usuarios registrados")
            cols_u = [c for c in ["Email","Nombre","Modo","Fondo","Fecha"] if c in df_u2.columns]
            st.dataframe(df_u2[cols_u], use_container_width=True, hide_index=True)
            sel_del = st.selectbox("Eliminar usuario",
                                   range(len(df_u2)),
                                   format_func=lambda i: f"{df_u2.iloc[i].get('Email','?')} — {df_u2.iloc[i].get('Nombre','?')}")
            if st.button("🗑 Eliminar acceso"):
                fs_delete("usuarios", df_u2.iloc[sel_del]["_id"])
                st.success("✓ Eliminado"); st.cache_data.clear(); st.rerun()

# ══════════════════════════════════════════════════════
# ADMINISTRACIÓN (admin)
# ══════════════════════════════════════════════════════
if rol == "admin":
    with t_adm:
        sec("Panel de administración")
        ca1,ca2 = st.columns(2)
        with ca1:
            sec("Resumen por fondo")
            rows_r = []
            for f in fondos_list:
                inv_f = df_inv_all[df_inv_all["Fondo"]==f] if not df_inv_all.empty else pd.DataFrame()
                n_inv = len(inv_f)
                rows_r.append({"Fondo":f,"# Inversiones":n_inv})
            st.dataframe(pd.DataFrame(rows_r), use_container_width=True, hide_index=True)

            sec("Crear nuevo fondo")
            nf = st.text_input("Nombre del fondo", key="nf_adm")
            if st.button("➕ CREAR FONDO"):
                if nf.strip() and nf not in fondos_list:
                    fs_post("aportes",{"Fondo":nf.strip(),"Socio":"","Cedula":"",
                                       "Fecha":str(date.today()),"Tipo":"Aporte",
                                       "Monto":0.0,"Usuario":usuario})
                    st.success(f"✓ Fondo '{nf}' creado")
                    st.cache_data.clear(); st.rerun()

        with ca2:
            sec("APIs activas")
            st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
                border-radius:8px;padding:14px;font:400 11px/2 IBM Plex Mono,mono">
              <div style="color:#8BA5C8;font-size:9px;letter-spacing:1px;margin-bottom:8px">FUENTES</div>
              <div style="color:#F0C040">● CoinMarketCap — Cripto</div>
              <div style="color:#C8A84B">● Yahoo Finance — Acciones / ETF</div>
              <div style="color:#2ECC87">● ExchangeRate-API — TRM</div>
              <div style="color:#8BA5C8;font-size:9px;margin-top:10px">
                TRM: ${trm:,.2f} · CMC: …{CMC_KEY[-6:]}</div></div>""",
                unsafe_allow_html=True)
            if st.button("🔄 Limpiar caché"):
                st.cache_data.clear(); st.success("✓ Caché limpiado")

        sec("Todas las inversiones")
        if not df_inv_all.empty:
            cols_a = [c for c in ["Fondo","Usuario","Fecha_Compra","Activo","Categoria",
                                   "Cantidad","Precio_Compra","Estado"] if c in df_inv_all.columns]
            st.dataframe(df_inv_all[cols_a].sort_values("Fecha_Compra",ascending=False),
                         use_container_width=True, hide_index=True)
