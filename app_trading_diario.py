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
    page_title="Arkez — Plataforma",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

html,body{ font-family:'IBM Plex Sans',sans-serif; }
.stApp{ background:#111827; color:#DCE5F0; }
/* Solo texto de contenido — NO los componentes de Streamlit */
.stMarkdown p, .stMarkdown span, .stText{ color:#DCE5F0; }
h1{ font-family:'IBM Plex Mono',monospace!important; color:#C8A84B!important; letter-spacing:2px; }
h2{ font-family:'IBM Plex Mono',monospace!important; font-size:11px!important;
    letter-spacing:1.5px; text-transform:uppercase; color:#8BA5C8!important; }
h3{ font-family:'IBM Plex Mono',monospace!important; font-size:13px!important; color:#C8A84B!important; }
hr{ border-color:#1E3354!important; }

/* Sidebar — sin sobreescribir * que rompe el toggle */
section[data-testid="stSidebar"]{ background:#0D1929!important; border-right:1px solid #1E3354; }
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stRadio label span { color:#DCE5F0!important; }
section[data-testid="stSidebar"] label{ color:#B0C4DC!important; font-size:12px!important; }

/* Inputs */
input,textarea{
    background:#162236!important; color:#DCE5F0!important;
    border:1px solid #1E3354!important; border-radius:6px!important;
    font-family:'IBM Plex Mono',monospace!important; font-size:13px!important;
}
input:focus,textarea:focus{ border-color:#C8A84B!important; box-shadow:0 0 0 1px #C8A84B!important; }

/* ── SELECTBOX COMPLETO — cerrado + abierto ── */
/* Control visible (cerrado) */
[data-testid="stSelectbox"] > div > div,
[data-baseweb="select"] > div {
    background: #162236 !important;
    border: 1px solid #2a4060 !important;
    border-radius: 6px !important;
}
/* Texto seleccionado */
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] p,
[data-baseweb="select"] span,
[data-baseweb="select"] input {
    color: #DCE5F0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}
/* Flecha */
[data-baseweb="select"] svg { fill: #8BA5C8 !important; }

/* Popup flotante — se renderiza fuera del árbol normal */
[data-baseweb="popover"],
[data-baseweb="popover"] *,
ul[data-baseweb="menu"],
ul[data-baseweb="menu"] *,
[role="listbox"],
[role="listbox"] *,
div[data-baseweb="menu"],
div[data-baseweb="menu"] * {
    background: #1a2d42 !important;
    color: #DCE5F0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    border-color: #2a4060 !important;
}
/* Opción al hacer hover */
[role="option"]:hover,
li[role="option"]:hover {
    background: #243b55 !important;
    color: #C8A84B !important;
}
/* Opción seleccionada activa */
[aria-selected="true"] {
    background: #1e3a5a !important;
    color: #C8A84B !important;
}

/* Labels */
[data-testid="stTextInput"] label,[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,[data-testid="stDateInput"] label,
[data-testid="stTextArea"] label,[data-testid="stRadio"]>label,
[data-testid="stCheckbox"] label{
    color:#B0C4DC!important; font-size:13px!important; font-weight:500!important;
}
[data-testid="stNumberInput"] button{
    background:#1A3050!important; color:#DCE5F0!important; border-color:#1E3354!important;
}

/* Botones */
.stButton>button{
    background:linear-gradient(135deg,#C8A84B,#A07830)!important;
    color:#0D1929!important; border:none!important; border-radius:6px!important;
    font-family:'IBM Plex Mono',monospace!important; font-weight:600!important;
    letter-spacing:1px!important; text-transform:uppercase!important; font-size:12px!important;
}
.stButton>button:hover{ filter:brightness(1.1)!important; }
.stButton>button[kind="secondary"]{
    background:#162236!important; color:#DCE5F0!important; border:1px solid #1E3354!important;
}

/* Tabs */
[data-testid="stTabs"] button{
    font-family:'IBM Plex Mono',monospace!important; font-size:11px!important;
    letter-spacing:1px; text-transform:uppercase; color:#8BA5C8!important; background:transparent!important;
}
[data-testid="stTabs"] button[aria-selected="true"]{
    color:#C8A84B!important; border-bottom:2px solid #C8A84B!important;
}
[data-testid="stTabs"]{ border-bottom:1px solid #1E3354; }

/* Métricas */
[data-testid="metric-container"]{
    background:#162236; border:1px solid #1E3354; border-radius:10px;
    padding:16px!important; position:relative; overflow:hidden;
}
[data-testid="metric-container"]::before{
    content:''; position:absolute; top:0;left:0;right:0; height:2px;
    background:linear-gradient(90deg,#C8A84B,#A07830);
}
[data-testid="stMetricValue"]{
    font-family:'IBM Plex Mono',monospace!important; font-size:1.4rem!important;
    color:#F0EAD6!important; font-weight:600!important;
}
[data-testid="stMetricLabel"]{
    font-family:'IBM Plex Mono',monospace!important; font-size:0.68rem!important;
    letter-spacing:1.2px; text-transform:uppercase; color:#8BA5C8!important;
}

/* DataFrames */
[data-testid="stDataFrame"]{ border:1px solid #1E3354; border-radius:8px; overflow:hidden; }
.stDataFrame th{ background:#0F1A2B!important; color:#8BA5C8!important; }
.stDataFrame td{ color:#DCE5F0!important; }

/* Alerts */
[data-testid="stAlert"]{
    border-radius:8px!important; border-left-width:3px!important;
    background:#162236!important; font-family:'IBM Plex Mono',monospace!important; color:#DCE5F0!important;
}

/* Form */
[data-testid="stForm"]{
    background:#0F1A2B!important; border:1px solid #1E3354!important;
    border-radius:10px!important; padding:20px!important;
}

/* Radio */
[data-testid="stRadio"] label span{ color:#DCE5F0!important; }

/* Expander */
[data-testid="stExpander"]{
    background:#162236!important; border:1px solid #1E3354!important; border-radius:8px!important;
}
[data-testid="stExpander"] summary,[data-testid="stExpander"] summary p{ color:#DCE5F0!important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# CONSTANTES
# ══════════════════════════════════════════════════════════════
FIREBASE_KEY = "AIzaSyC52gIJJRTE1B4BqeUwDmaX2fWKS3sSw10"
FS_URL       = "https://firestore.googleapis.com/v1/projects/plataforma-de-inversiones/databases/(default)/documents"
ADMIN_EMAIL  = "jmarquezg2004@gmail.com"
CMC_KEY      = st.secrets.get("CMC_KEY", "d67913f039804c6b900905ebad7c1aaf")

CATEGORIAS  = ["Acción","ETF","Cripto","CDT","Fondo","Cuenta Remunerada","Otro"]
ESTRATEGIAS = ["Spot","Holding","Futuros","Staking","Farming",
               "Arbitraje","Bot/Copy Trading","Launchpool","ICO","Renta Fija"]
RESULTADOS  = ["Abierta","Ganadora","Perdedora","Cancelada"]

# Modos de acceso del usuario
MODO_INDIVIDUAL = "Portafolio Individual"   # el usuario registra y ve solo sus ops
MODO_OBSERVADOR = "Observador de Fondo"     # el usuario solo ve, no puede editar

# ══════════════════════════════════════════════════════════════
# FIREBASE AUTH
# ══════════════════════════════════════════════════════════════
def firebase_login(email, password):
    try:
        r = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_KEY}",
            json={"email": email, "password": password, "returnSecureToken": True}, timeout=8)
        if r.status_code == 200:
            return True, r.json()
        return False, r.json().get("error", {}).get("message", "Error")
    except Exception as e:
        return False, str(e)

def firebase_crear(email, password):
    try:
        r = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_KEY}",
            json={"email": email, "password": password, "returnSecureToken": True}, timeout=8)
        if r.status_code == 200:
            return True, "OK"
        return False, r.json().get("error", {}).get("message", "Error")
    except Exception as e:
        return False, str(e)

# ══════════════════════════════════════════════════════════════
# FIRESTORE CRUD
# ══════════════════════════════════════════════════════════════
def _field(v):
    if isinstance(v, bool):   return {"booleanValue": v}
    if isinstance(v, int):    return {"integerValue": str(v)}
    if isinstance(v, float):  return {"doubleValue": v}
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
                    row[k] = list(v.values())[0]
                rows.append(row)
            return pd.DataFrame(rows) if rows else pd.DataFrame()
    except Exception:
        pass
    return pd.DataFrame()

def fs_post(col, datos: dict):
    fields = {k: _field(v) for k, v in datos.items()}
    try:
        r = requests.post(f"{FS_URL}/{col}", json={"fields": fields}, timeout=10)
        if r.status_code in (200, 201):
            return True, ""
        return False, f"Error {r.status_code}: {r.text[:500]}"
    except Exception as e:
        return False, str(e)

def fs_patch(col, doc_id, datos: dict):
    fields = {k: _field(v) for k, v in datos.items()}
    mask   = "&".join(f"updateMask.fieldPaths={k}" for k in datos)
    try:
        requests.patch(f"{FS_URL}/{col}/{doc_id}?{mask}", json={"fields": fields}, timeout=10)
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
# PRECIOS
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def get_trm():
    for url in ["https://open.er-api.com/v6/latest/USD",
                "https://api.frankfurter.app/latest?from=USD&to=COP"]:
        try:
            r = requests.get(url, timeout=6)
            if r.status_code == 200:
                cop = r.json().get("rates", {}).get("COP")
                if cop and float(cop) > 3000:
                    return float(cop)
        except Exception:
            pass
    try:
        import yfinance as yf
        px = yf.Ticker("USDCOP=X").fast_info.last_price
        if px and px > 3000: return float(px)
    except Exception:
        pass
    return 4200.0

@st.cache_data(ttl=300)
def get_cmc(syms):
    if not syms: return {}
    try:
        r = requests.get(
            "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest",
            params={"symbol": ",".join(syms), "convert": "USD"},
            headers={"X-CMC_PRO_API_KEY": CMC_KEY, "Accept": "application/json"},
            timeout=10)
        if r.status_code != 200: return {}
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
    if df_ops.empty: return out
    criptos = [x.strip().upper() for x in df_ops[df_ops["Categoria"]=="Cripto"]["Ticker_API"].dropna() if x.strip()]
    if criptos: out.update(get_cmc(tuple(set(criptos))))
    stocks  = [x.strip().upper() for x in df_ops[df_ops["Categoria"].isin(["Acción","ETF","Fondo"])]["Ticker_API"].dropna() if x.strip()]
    for t in set(stocks):
        px, chg = get_stock(t)
        if px: out[t] = {"price": px, "chg24": chg}
    return out

# ══════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════════════
COLS_AP  = ["_id","Fondo","Socio","Cedula","Fecha","Tipo","Monto","TipoCuenta","Usuario"]
COLS_OPS = ["_id","ID","Fondo","Usuario","Fecha","Activo","Categoria","Estrategia",
            "Broker","Valor_Pos","TP_pct","SL_pct","TP_usd","SL_usd","Comision",
            "Resultado","Ticker_API","Precio_Entrada","Cantidad","TEA","Notas"]
COLS_USR = ["_id","Email","Nombre","Modo","Fondo","Activo","CreadoPor","Fecha"]

@st.cache_data(ttl=60)
def load_aportes():
    df = fs_get("aportes")
    if df.empty: return pd.DataFrame(columns=COLS_AP)
    for c in COLS_AP:
        if c not in df.columns: df[c] = ""
    df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce").fillna(0.0)
    return df

@st.cache_data(ttl=60)
def load_ops():
    df = fs_get("operaciones")
    if df.empty: return pd.DataFrame(columns=COLS_OPS)
    num = ["Valor_Pos","TP_pct","SL_pct","TP_usd","SL_usd","Comision",
           "Precio_Entrada","Cantidad","TEA","ID"]
    for c in COLS_OPS:
        if c not in df.columns:
            df[c] = 0.0 if c in num else ""
    for c in num:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
    return df

@st.cache_data(ttl=60)
def load_usuarios():
    df = fs_get("usuarios")
    if df.empty: return pd.DataFrame(columns=COLS_USR)
    for c in COLS_USR:
        if c not in df.columns: df[c] = ""
    return df

# ══════════════════════════════════════════════════════════════
# CÁLCULOS
# ══════════════════════════════════════════════════════════════
def pnl(row):
    if row.get("Resultado") == "Ganadora":
        return float(row.get("TP_usd",0) or 0) - float(row.get("Comision",0) or 0)
    if row.get("Resultado") == "Perdedora":
        return -float(row.get("SL_usd",0) or 0) - float(row.get("Comision",0) or 0)
    return 0.0

def valorar(row, prices):
    t   = str(row.get("Ticker_API","")).strip().upper()
    cat = str(row.get("Categoria",""))
    pe  = float(row.get("Precio_Entrada",0) or 0)
    qty = float(row.get("Cantidad",0) or 0)
    vp  = float(row.get("Valor_Pos",0) or 0)
    tea = float(row.get("TEA",0) or 0)
    if cat in ["CDT","Cuenta Remunerada"] and tea > 0 and vp > 0:
        try:
            dias = max((pd.Timestamp.now() - pd.to_datetime(row.get("Fecha"))).days, 0)
            val  = vp * ((1+tea)**(dias/365))
            gp   = val - vp
            return val, gp, gp/vp*100
        except Exception: return vp, 0, 0
    if t and t in prices and prices[t].get("price",0) > 0:
        px = prices[t]["price"]
        if pe > 0 and qty > 0:
            val = px*qty; gp = val - pe*qty
            return val, gp, gp/(pe*qty)*100 if pe*qty else 0
        if vp > 0 and pe > 0:
            val = vp*px/pe; gp = val-vp
            return val, gp, gp/vp*100
    return vp, 0.0, 0.0

# ══════════════════════════════════════════════════════════════
# UI HELPERS
# ══════════════════════════════════════════════════════════════
PT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
          font=dict(family="IBM Plex Mono", color="#DCE5F0", size=11),
          margin=dict(l=0,r=0,t=36,b=0),
          xaxis=dict(gridcolor="#152034",linecolor="#1E3354"),
          yaxis=dict(gridcolor="#152034",linecolor="#1E3354"))

CAT_CLR = {"Acción":"#C8A84B","ETF":"#2ECC87","Cripto":"#E87844",
           "CDT":"#F0C040","Fondo":"#9B8EC4","Cuenta Remunerada":"#6BA3BE","Otro":"#8BA5C8"}

def card(label, val, sub=None, color="#C8A84B"):
    s = f'<div style="font:500 11px/1.3 IBM Plex Mono,mono;color:{color};margin-top:3px">{sub}</div>' if sub else ""
    return f"""<div style="background:#162236;border:1px solid #1E3354;border-radius:10px;
        padding:16px 18px;position:relative;overflow:hidden;height:100%">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;background:{color}"></div>
      <div style="font:400 9px/1 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1.5px;
                  text-transform:uppercase;margin-bottom:8px">{label}</div>
      <div style="font:600 22px/1 IBM Plex Mono,mono;color:#F0EAD6">{val}</div>{s}</div>"""

def money(v, f=1):
    v2 = v*f
    if abs(v2) >= 1e6: return f"${v2/1e6:.2f}M"
    return f"${v2:,.2f}"

def sec(t):
    st.markdown(f'<h2 style="margin:18px 0 10px">{t}</h2>', unsafe_allow_html=True)

def info_box(msg, color="#C8A84B"):
    st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
        border-left:3px solid {color};border-radius:0 8px 8px 0;
        padding:10px 14px;margin-bottom:14px;
        font:400 12px/1.7 IBM Plex Mono,mono;color:#B0C4DC">{msg}</div>""",
        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════
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
                    em = email.strip().lower()
                    rol = "admin" if em == ADMIN_EMAIL.lower() else "usuario"
                    # Cargar perfil del usuario desde Firestore
                    df_u = load_usuarios()
                    modo_u = MODO_INDIVIDUAL
                    fondo_u = None
                    if not df_u.empty and "Email" in df_u.columns:
                        fila = df_u[df_u["Email"].str.lower() == em]
                        if not fila.empty:
                            modo_u  = fila.iloc[0].get("Modo", MODO_INDIVIDUAL)
                            fondo_u = fila.iloc[0].get("Fondo", None) or None
                    st.session_state.update({
                        "logged_in": True, "usuario": em, "rol": rol,
                        "modo_usuario": modo_u, "fondo_asignado": fondo_u,
                        "fondo_sel": fondo_u or "Arkez Invest"
                    })
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
            else:
                st.warning("Completa los dos campos")
    st.stop()

# ══════════════════════════════════════════════════════════════
# SESIÓN
# ══════════════════════════════════════════════════════════════
rol           = st.session_state.rol
usuario       = st.session_state.usuario
modo_usuario  = st.session_state.get("modo_usuario", MODO_INDIVIDUAL)
fondo_asignado= st.session_state.get("fondo_asignado")   # None si no tiene fondo asignado

# Cargar datos globales
df_ap_all  = load_aportes()
df_ops_all = load_ops()
df_usrs    = load_usuarios()

# Lista de fondos existentes
fondos_set  = (set(df_ap_all["Fondo"].dropna()) | set(df_ops_all["Fondo"].dropna())) - {""}
fondos_list = sorted(fondos_set) or []
if "Arkez Invest" not in fondos_list:
    fondos_list.insert(0, "Arkez Invest")

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""<div style="text-align:center;padding:14px 0 10px">
      <div style="display:inline-block;width:34px;height:34px;margin-bottom:7px;
                  background:linear-gradient(135deg,#C8A84B,#A07830);
                  clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%)"></div>
      <div style="font:600 14px/1 IBM Plex Mono,mono;color:#C8A84B;letter-spacing:3px">ARKEZ</div>
    </div>""", unsafe_allow_html=True)

    rc = "#C8A84B" if rol=="admin" else "#2ECC87"
    rb = "rgba(200,168,75,.12)" if rol=="admin" else "rgba(46,204,135,.12)"
    st.markdown(f"""<div style="background:#152034;border:1px solid #1E3354;border-radius:8px;
        padding:10px 12px;margin-bottom:10px">
      <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px;margin-bottom:3px">USUARIO</div>
      <div style="font:400 11px/1.4 IBM Plex Mono,mono;color:#DCE5F0;word-break:break-all">{usuario}</div>
      <span style="display:inline-block;margin-top:4px;background:{rb};color:{rc};
                   border:1px solid {rc};padding:1px 9px;border-radius:20px;
                   font:600 9px/1.8 IBM Plex Mono,mono">
        {'⬡ ADMIN' if rol=='admin' else '● '+modo_usuario.split()[0].upper()}
      </span>
    </div>""", unsafe_allow_html=True)

    # Selección de fondo según rol
    if rol == "admin":
        fondo = st.selectbox("🏦 Fondo activo", fondos_list,
                             index=fondos_list.index(st.session_state.get("fondo_sel","Arkez Invest"))
                             if st.session_state.get("fondo_sel") in fondos_list else 0)
        st.session_state.fondo_sel = fondo
    else:
        if fondo_asignado and fondo_asignado in fondos_list:
            fondo = fondo_asignado
            st.markdown(f"""<div style="background:#152034;border:1px solid #1E3354;border-radius:6px;
                padding:8px 12px;margin-bottom:8px">
              <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">FONDO ASIGNADO</div>
              <div style="font:600 12px IBM Plex Mono,mono;color:#C8A84B">{fondo}</div>
            </div>""", unsafe_allow_html=True)
        else:
            # Sin fondo asignado: portafolio individual propio
            fondo = f"personal_{usuario.split('@')[0]}"
            st.markdown(f"""<div style="background:#152034;border:1px solid #1E3354;border-radius:6px;
                padding:8px 12px;margin-bottom:8px">
              <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">PORTAFOLIO</div>
              <div style="font:600 12px IBM Plex Mono,mono;color:#C8A84B">Personal</div>
            </div>""", unsafe_allow_html=True)

    trm = get_trm()
    st.markdown(f"""<div style="background:#152034;border:1px solid #1E3354;border-radius:8px;
        padding:9px 12px;margin:8px 0">
      <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">TRM USD/COP</div>
      <div style="font:600 16px/1.5 IBM Plex Mono,mono;color:#F0C040">${trm:,.2f}</div>
    </div>""", unsafe_allow_html=True)

    moneda = st.radio("Moneda", ["USD","COP"], horizontal=True)
    factor = trm if moneda=="COP" else 1.0

    st.markdown("---")
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# ══════════════════════════════════════════════════════════════
# FILTRAR DATOS POR FONDO Y MODO
# ══════════════════════════════════════════════════════════════
# Para un Observador de Fondo: ve todas las ops del fondo, no puede editar
# Para un Portafolio Individual: ve y edita solo sus propias ops
# Para Admin: ve y edita todo

def ops_visibles(df):
    """Retorna las operaciones que el usuario actual puede ver."""
    if df.empty: return df
    if rol == "admin":
        return df[df["Fondo"] == fondo]
    if modo_usuario == MODO_OBSERVADOR:
        return df[df["Fondo"] == fondo]
    else:
        # Portafolio individual: filtra por Usuario (funciona con o sin fondo asignado)
        if "Usuario" in df.columns:
            mask = df["Usuario"] == usuario
            # También incluir ops con el fondo personal (compatibilidad)
            if "Fondo" in df.columns:
                mask = mask | (df["Fondo"] == fondo)
            return df[mask]
        return df[df["Fondo"] == fondo]

def puede_editar():
    """Retorna True si el usuario puede registrar/editar operaciones."""
    if rol == "admin": return True
    if modo_usuario == MODO_OBSERVADOR: return False
    return True  # Portafolio individual: sí puede

df_ap  = df_ap_all[df_ap_all["Fondo"] == fondo].copy()  if not df_ap_all.empty  else pd.DataFrame()
df_ops = ops_visibles(df_ops_all).copy() if not df_ops_all.empty else pd.DataFrame()
prices = get_prices(df_ops)

capital = df_ap["Monto"].sum() if not df_ap.empty else 0.0
ops_c   = df_ops[df_ops["Resultado"].isin(["Ganadora","Perdedora"])].copy() if not df_ops.empty else pd.DataFrame()
ops_a   = df_ops[df_ops["Resultado"] == "Abierta"].copy() if not df_ops.empty else pd.DataFrame()

if not ops_c.empty:
    ops_c["PnL"] = ops_c.apply(pnl, axis=1)
    pnl_c = ops_c["PnL"].sum()
else:
    pnl_c = 0.0

abiertas, val_ab, pnl_ab = [], 0.0, 0.0
if not ops_a.empty:
    for _, row in ops_a.iterrows():
        val, gp, pct = valorar(row, prices)
        val_ab += val; pnl_ab += gp
        abiertas.append({
            "Activo": row.get("Activo","—"),      "Categoria": row.get("Categoria","—"),
            "Ticker": row.get("Ticker_API","—"),   "Val_ent":  float(row.get("Valor_Pos",0) or 0),
            "Val_act": val,                         "GP_usd":   gp,
            "GP_pct":  pct,                         "Fecha":    row.get("Fecha","—"),
            "_id":     row.get("_id",""),            "Usuario":  row.get("Usuario","—"),
        })

total_gp   = pnl_c + pnl_ab
patrimonio = capital + total_gp
rend       = total_gp/capital*100 if capital > 0 else 0
wr         = (ops_c["Resultado"]=="Ganadora").sum()/len(ops_c)*100 if not ops_c.empty else 0

# ══════════════════════════════════════════════════════════════
# HEADER + KPIs
# ══════════════════════════════════════════════════════════════
modo_badge = ""
if rol != "admin":
    if modo_usuario == MODO_OBSERVADOR:
        modo_badge = ' <span style="font:600 9px IBM Plex Mono,mono;background:rgba(155,142,196,.15);color:#9B8EC4;border:1px solid #9B8EC4;padding:1px 7px;border-radius:20px;vertical-align:middle">SOLO LECTURA</span>'
    else:
        modo_badge = ' <span style="font:600 9px IBM Plex Mono,mono;background:rgba(46,204,135,.12);color:#2ECC87;border:1px solid #2ECC87;padding:1px 7px;border-radius:20px;vertical-align:middle">PORTAFOLIO PERSONAL</span>'

st.markdown(f"""<div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:4px">
  <div style="width:36px;height:36px;flex-shrink:0;background:linear-gradient(135deg,#C8A84B,#A07830);
              clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%)"></div>
  <div>
    <div style="font:600 18px/1 IBM Plex Mono,mono;color:#C8A84B;letter-spacing:2px">
      {fondo.upper()}{modo_badge}</div>
    <div style="font:400 10px/1.5 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">
      ARKEZ · PLATAFORMA · PRECIOS EN TIEMPO REAL</div>
  </div>
  <div style="margin-left:auto;font:400 10px IBM Plex Mono,mono;color:#8BA5C8">
    {datetime.now().strftime('%d/%m/%Y %H:%M')}</div></div>
<hr style="margin:12px 0 18px">""", unsafe_allow_html=True)

gc = "#2ECC87" if total_gp>=0 else "#E85555"
k1,k2,k3,k4,k5 = st.columns(5)
with k1: st.markdown(card("Patrimonio total",   money(patrimonio,factor)), unsafe_allow_html=True)
with k2: st.markdown(card("Capital aportado",   money(capital,factor), color="#8BA5C8"), unsafe_allow_html=True)
with k3: st.markdown(card("Ganancia / Pérdida",
    f"{'+'if total_gp>=0 else ''}{money(total_gp,factor)}",
    f"{'▲' if rend>=0 else '▼'} {abs(rend):.2f}%", color=gc), unsafe_allow_html=True)
with k4: st.markdown(card("Posiciones abiertas", money(val_ab,factor),
    f"{len(abiertas)} posiciones", color="#F0C040"), unsafe_allow_html=True)
with k5: st.markdown(card("Win rate", f"{wr:.1f}%",
    f"{len(ops_c)} ops cerradas", color="#9B8EC4"), unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TABS — dinámicos según rol y modo
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    t_dash,t_pos,t_reg,t_soc,t_anal,t_usr,t_adm = st.tabs([
        "⬡ Dashboard","◈ Posiciones","📌 Registrar Op.",
        "💰 Socios / Capital","📊 Análisis","👥 Usuarios","⚙ Administración"])
elif modo_usuario == MODO_OBSERVADOR:
    # Solo lectura: sin tab de registro
    t_dash,t_pos,t_anal = st.tabs(["⬡ Dashboard","◈ Posiciones","📊 Análisis"])
else:
    # Portafolio individual: puede registrar sus ops
    t_dash,t_pos,t_reg,t_anal = st.tabs([
        "⬡ Dashboard","◈ Mis posiciones","📌 Registrar Op.","📊 Análisis"])

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
            dfe["cap"] = dfe.apply(
                lambda r: r["Monto"] if r["Tipo"]=="Aporte" else -r["Monto"], axis=1
            ).cumsum() * factor
            fig = go.Figure(go.Scatter(
                x=dfe["Fecha"], y=dfe["cap"], mode="lines+markers",
                line=dict(color="#C8A84B",width=2), fill="tozeroy",
                fillcolor="rgba(200,168,75,.07)", marker=dict(color="#C8A84B",size=5),
                hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:$,.0f}<extra></extra>"))
            fig.update_layout(**PT, title=dict(text="Evolución del capital",
                font=dict(size=11,color="#8BA5C8"),x=.5))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        else:
            st.info("Sin movimientos de capital registrados.")
    with cr:
        if not df_ops.empty:
            dist = df_ops.groupby("Categoria")["Valor_Pos"].sum().reset_index()
            dist = dist[dist["Valor_Pos"]>0]
            if not dist.empty:
                fig2 = go.Figure(go.Pie(
                    labels=dist["Categoria"], values=dist["Valor_Pos"]*factor, hole=.6,
                    marker=dict(colors=[CAT_CLR.get(c,"#8BA5C8") for c in dist["Categoria"]],
                                line=dict(color="#111827",width=2)),
                    hovertemplate="<b>%{label}</b><br>%{value:$,.0f}<br>%{percent}<extra></extra>"))
                fig2.update_layout(**PT, title=dict(text="Distribución por tipo",
                    font=dict(size=11,color="#8BA5C8"),x=.5))
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        else:
            st.info("Sin operaciones registradas.")

    if prices:
        sec("Precios en tiempo real")
        cols_p = st.columns(min(len(prices),5))
        for i,(tk,d) in enumerate(list(prices.items())[:10]):
            chg = d.get("chg24",0); px = d.get("price",0)
            clr = "#2ECC87" if chg>=0 else "#E85555"
            pxs = f"${px:,.4f}" if px<10 else f"${px:,.2f}"
            with cols_p[i%min(len(prices),5)]:
                st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
                    border-radius:8px;padding:12px;text-align:center;margin-bottom:8px">
                  <div style="font:600 11px/1.5 IBM Plex Mono,mono;color:#C8A84B">{tk}</div>
                  <div style="font:600 15px/1.4 IBM Plex Mono,mono;color:#F0EAD6">{pxs}</div>
                  <div style="font:400 10px/1.3 IBM Plex Mono,mono;color:{clr}">
                    {'▲' if chg>=0 else '▼'} {abs(chg):.2f}%</div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# POSICIONES
# ══════════════════════════════════════════════════════════════
with t_pos:
    if abiertas:
        sec("Posiciones abiertas — valorización actual")
        for a in abiertas:
            gc2 = "#2ECC87" if a["GP_usd"]>=0 else "#E85555"
            sg  = "+" if a["GP_usd"]>=0 else ""
            pxd = prices.get(a["Ticker"].upper(),{})
            pxs = (f"${pxd['price']:,.4f}" if pxd.get("price",0)<10 else f"${pxd['price']:,.2f}") if pxd else "—"
            st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
                border-radius:10px;padding:14px 18px;margin-bottom:10px;
                display:flex;align-items:center;gap:18px;flex-wrap:wrap">
              <div style="min-width:130px">
                <div style="font:600 14px/1.3 IBM Plex Mono,mono;color:#C8A84B">{a['Activo']}</div>
                <div style="font:400 10px/1.4 IBM Plex Mono,mono;color:#8BA5C8">
                  {a['Ticker']} · {a['Categoria']}</div>
                <div style="font:400 9px/1.4 IBM Plex Mono,mono;color:#4a6f8a">{a['Fecha']}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">PRECIO HOY</div>
                <div style="font:500 13px IBM Plex Mono,mono;color:#DCE5F0">{pxs}</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">ENTRADA</div>
                <div style="font:500 13px IBM Plex Mono,mono;color:#DCE5F0">{money(a['Val_ent'],factor)}</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">VALOR ACTUAL</div>
                <div style="font:600 14px IBM Plex Mono,mono;color:#F0EAD6">{money(a['Val_act'],factor)}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">G/P</div>
                <div style="font:600 15px IBM Plex Mono,mono;color:{gc2}">{sg}{money(a['GP_usd'],factor)}</div>
                <div style="font:500 10px IBM Plex Mono,mono;color:{gc2}">{sg}{a['GP_pct']:.2f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("Sin posiciones abiertas actualmente.")

    if not df_ops.empty:
        sec("Historial de operaciones")
        cols_s = [c for c in ["Fecha","Activo","Categoria","Estrategia",
                               "Valor_Pos","Resultado","Ticker_API","Usuario"] if c in df_ops.columns]
        dfs = df_ops[cols_s].sort_values("Fecha",ascending=False).copy()
        if "Valor_Pos" in dfs.columns: dfs["Valor_Pos"] = dfs["Valor_Pos"]*factor
        def cr(v):
            if v=="Ganadora":  return "color:#2ECC87;font-weight:600"
            if v=="Perdedora": return "color:#E85555;font-weight:600"
            if v=="Abierta":   return "color:#C8A84B"
            return ""
        styled = dfs.style
        if "Resultado" in dfs.columns:
            styled = styled.applymap(cr, subset=["Resultado"])
        if "Valor_Pos" in dfs.columns:
            styled = styled.format({"Valor_Pos":"${:,.2f}"})
        st.dataframe(styled, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# REGISTRAR OPERACIÓN (admin + portafolio individual)
# ══════════════════════════════════════════════════════════════
if rol == "admin" or modo_usuario == MODO_INDIVIDUAL:
    with t_reg:
        sec("Registrar nueva operación")
        st.markdown(f'<div style="font:400 11px/1.5 IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:10px">'
                    f'Registrando como: <strong style="color:#C8A84B">{usuario}</strong> · '
                    f'Fondo: <strong style="color:#C8A84B">{fondo}</strong></div>',
                    unsafe_allow_html=True)

        with st.form("form_op", clear_on_submit=True):
            c1,c2,c3,c4 = st.columns(4)
            fecha_op   = c1.date_input("Fecha", value=date.today())
            activo     = c2.text_input("Nombre del activo", placeholder="Bitcoin, Nubank, VTI…")
            categoria  = c3.selectbox("Categoría", CATEGORIAS)
            estrategia = c4.selectbox("Estrategia", ESTRATEGIAS)

            c5,c6,c7 = st.columns(3)
            broker    = c5.text_input("Broker / Exchange")
            valor_pos = c6.number_input("Valor posición USD", min_value=0.0, step=0.01, format="%.2f")
            comision  = c7.number_input("Comisión USD", min_value=0.0, step=0.01, format="%.2f")

            c8,c9,c10,c11 = st.columns(4)
            pe   = c8.number_input("Precio de entrada", min_value=0.0, step=0.0001, format="%.4f")
            tp   = c10.number_input("TP %",             min_value=0.0, step=0.1,    format="%.2f")
            sl   = c11.number_input("SL %",             min_value=0.0, step=0.1,    format="%.2f")

            # Cantidad calculada automáticamente = valor_pos / precio_entrada
            qty_calc = round(valor_pos / pe, 6) if pe > 0 and valor_pos > 0 else 0.0
            qty_label = f"{qty_calc:,.6f}" if qty_calc > 0 else "0.000000 (ingresa precio y valor)"
            c9.text_input("Cantidad / Unidades (auto)", value=qty_label, disabled=True,
                          help="Se calcula automáticamente: Valor Posición ÷ Precio de Entrada")

            c12,c13,c14 = st.columns(3)
            resultado  = c12.selectbox("Resultado actual", RESULTADOS)
            ticker_api = c13.text_input("Ticker para precios", placeholder="BTC · AAPL · VTI")
            tea_pct    = c14.number_input("TEA % anual (CDT/Remunerada)",
                             min_value=0.0, max_value=100.0, step=0.01, format="%.2f",
                             help="Solo para CDT o Cuenta Remunerada. Ej: 12.85")
            notas = st.text_area("Notas", height=60, placeholder="Observaciones opcionales…")

            if st.form_submit_button("💾 GUARDAR OPERACIÓN", use_container_width=True):
                if not activo.strip():
                    st.error("❌ El nombre del activo es obligatorio")
                else:
                    # ID seguro contra NaN y tipos inesperados
                    try:
                        ids = pd.to_numeric(df_ops_all["ID"], errors="coerce") if not df_ops_all.empty else pd.Series([], dtype=float)
                        max_id = ids.max()
                        nid = int(max_id) + 1 if not pd.isna(max_id) and max_id > 0 else 1
                    except Exception:
                        nid = 1

                    ok, err_msg = fs_post("operaciones", {
                        "ID":             nid,
                        "Fondo":          fondo,
                        "Usuario":        usuario,
                        "Fecha":          str(fecha_op),
                        "Activo":         activo.strip(),
                        "Categoria":      categoria,
                        "Estrategia":     estrategia,
                        "Broker":         broker.strip(),
                        "Valor_Pos":      float(valor_pos),
                        "TP_pct":         float(tp),
                        "SL_pct":         float(sl),
                        "TP_usd":         float(valor_pos * tp / 100),
                        "SL_usd":         float(valor_pos * sl / 100),
                        "Comision":       float(comision),
                        "Resultado":      resultado,
                        "Ticker_API":     ticker_api.strip().upper(),
                        "Precio_Entrada": float(pe),
                        "Cantidad":       float(qty_calc),
                        "TEA":            float(tea_pct / 100) if tea_pct > 0 else 0.0,
                        "Notas":          notas.strip(),
                    })
                    if ok:
                        st.success("✓ Operación guardada correctamente")
                        st.cache_data.clear(); time.sleep(0.6); st.rerun()
                    else:
                        st.error(f"❌ Error Firestore: {err_msg}")

        # Editar solo las propias (o todas si admin)
        mis_ops_e = df_ops if rol=="admin" else (
            df_ops[df_ops["Usuario"]==usuario] if not df_ops.empty and "Usuario" in df_ops.columns
            else pd.DataFrame())
        if not mis_ops_e.empty:
            st.markdown("---"); sec("Editar / eliminar operación")
            lbs = [f"{r.get('Fecha','?')} — {r.get('Activo','?')} ({r.get('Resultado','?')})"
                   for _,r in mis_ops_e.iterrows()]
            sel = st.selectbox("Selecciona operación", range(len(lbs)),
                               format_func=lambda i: lbs[i], key="sel_e")
            if sel is not None:
                sr = mis_ops_e.iloc[sel]
                ce1,ce2,ce3 = st.columns(3)
                with ce1:
                    ri = RESULTADOS.index(sr.get("Resultado","Abierta")) if sr.get("Resultado") in RESULTADOS else 0
                    nr = st.selectbox("Nuevo resultado", RESULTADOS, index=ri, key="nr_e")
                    if st.button("✏️ Actualizar resultado"):
                        fs_patch("operaciones", sr["_id"], {"Resultado": nr})
                        st.success("✓ Actualizado"); st.cache_data.clear(); st.rerun()
                with ce2:
                    nf = st.date_input("Cambiar fecha", key="nf_e")
                    if st.button("📅 Actualizar fecha"):
                        fs_patch("operaciones", sr["_id"], {"Fecha": str(nf)})
                        st.success("✓ Actualizado"); st.cache_data.clear(); st.rerun()
                with ce3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🗑 Eliminar"):
                        fs_delete("operaciones", sr["_id"])
                        st.success("✓ Eliminada"); st.cache_data.clear(); st.rerun()

# ══════════════════════════════════════════════════════════════
# SOCIOS / CAPITAL (admin)
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    with t_soc:
        sec("Movimientos de capital — Socios")
        with st.form("form_ap", clear_on_submit=True):
            c1,c2,c3,c4 = st.columns(4)
            socio    = c1.text_input("Nombre del socio")
            cedula   = c2.text_input("Cédula / ID")
            tipo_mov = c3.selectbox("Tipo", ["Aporte","Retiro"])
            monto    = c4.number_input("Monto (USD)", min_value=0.0, step=0.01, format="%.2f")
            c5,c6    = st.columns(2)
            tipo_cta = c5.selectbox("Tipo de cuenta",
                ["Fondo Grupal","Portafolio Individual"],
                help="Fondo Grupal: dinero al fondo colectivo.\nPortafolio Individual: cuenta propia.")
            fecha_a  = c6.date_input("Fecha", value=date.today())
            if st.form_submit_button("💾 GUARDAR MOVIMIENTO", use_container_width=True):
                if not socio.strip():
                    st.error("❌ Nombre del socio obligatorio")
                else:
                    ok, err_msg = fs_post("aportes", {
                        "Fondo": fondo, "Socio": socio.strip(), "Cedula": cedula.strip(),
                        "Fecha": str(fecha_a), "Tipo": tipo_mov, "Monto": float(monto),
                        "TipoCuenta": tipo_cta, "Usuario": usuario,
                    })
                    if ok:
                        st.success(f"✓ Guardado — {tipo_cta}")
                        st.cache_data.clear(); st.rerun()
                    else:
                        st.error(f"❌ Error Firestore: {err_msg}")

        if not df_ap.empty and "Socio" in df_ap.columns and df_ap["Socio"].str.strip().any():
            st.markdown("---"); sec("Resumen por socio")
            df_s = df_ap.copy()
            df_s["ms"] = df_s.apply(lambda r: r["Monto"] if r["Tipo"]=="Aporte" else -r["Monto"], axis=1)
            grp_cols = [c for c in ["Socio","Cedula","TipoCuenta"] if c in df_s.columns]
            res = df_s.groupby(grp_cols).agg(
                Aportes=("ms", lambda x: x[x>0].sum()),
                Retiros=("ms", lambda x: abs(x[x<0].sum())),
                Neto=("ms","sum")).reset_index()
            tn = res["Neto"].sum()
            res["% Fondo"] = (res["Neto"]/tn*100).round(2) if tn else 0
            for c in ["Aportes","Retiros","Neto"]:
                res[c] = res[c]*factor
            st.dataframe(res.style.format({
                "Aportes":"${:,.2f}","Retiros":"${:,.2f}","Neto":"${:,.2f}","% Fondo":"{:.2f}%"}),
                use_container_width=True, hide_index=True)

            sec("Historial de movimientos")
            hc = [c for c in ["Fecha","Socio","Cedula","Tipo","TipoCuenta","Monto"] if c in df_ap.columns]
            dfh = df_ap[hc].sort_values("Fecha",ascending=False).copy()
            if "Monto" in dfh.columns: dfh["Monto"] = dfh["Monto"]*factor
            def crt(v):
                if v=="Aporte":  return "color:#2ECC87;font-weight:600"
                if v=="Retiro":  return "color:#E85555;font-weight:600"
                return ""
            sh = dfh.style.format({"Monto":"${:,.2f}"})
            if "Tipo" in dfh.columns: sh = sh.applymap(crt,subset=["Tipo"])
            st.dataframe(sh, use_container_width=True, hide_index=True)
            if st.button("🗑 Eliminar último movimiento"):
                lid = df_ap.sort_values("Fecha").iloc[-1]["_id"]
                fs_delete("aportes",lid); st.cache_data.clear(); st.rerun()

# ══════════════════════════════════════════════════════════════
# ANÁLISIS
# ══════════════════════════════════════════════════════════════
with t_anal:
    sec("Análisis de rendimiento")
    if not ops_c.empty:
        ca1,ca2 = st.columns([3,2])
        with ca1:
            fig_b = go.Figure(go.Bar(
                x=ops_c.apply(lambda r:f"{r.get('Activo','?')} ({r.get('Fecha','?')})",axis=1),
                y=ops_c["PnL"],
                marker_color=ops_c["PnL"].apply(lambda x:"#2ECC87" if x>=0 else "#E85555"),
                text=ops_c["PnL"].apply(lambda x:f"${x:,.0f}"),
                textposition="outside", textfont=dict(size=10),
                hovertemplate="<b>%{x}</b><br>P&L: $%{y:,.2f}<extra></extra>"))
            fig_b.update_layout(**PT, title=dict(text="P&L por operación cerrada",
                font=dict(size=11,color="#8BA5C8"),x=.5))
            st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar":False})
        with ca2:
            pv    = ops_c["PnL"]
            mejor = ops_c.loc[pv.idxmax()]
            peor  = ops_c.loc[pv.idxmin()]
            avg_g = pv[pv>0].mean() if (pv>0).any() else 0
            avg_p = pv[pv<0].mean() if (pv<0).any() else 0
            pf    = abs(pv[pv>0].sum()/pv[pv<0].sum()) if (pv<0).any() else 9.99
            wr2   = (pv>0).sum()/len(pv)*100
            st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
                border-radius:10px;padding:16px">
              <div style="font:400 9px/2 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1.5px;text-transform:uppercase">Estadísticas</div>
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
        sec("Gestión de usuarios")
        info_box(
            "Dos modos de acceso:<br>"
            "<strong>① Portafolio Individual</strong> → el usuario entra y registra sus propias inversiones. "
            "Solo él las ve. Tú como admin las ves todas.<br>"
            "<strong>② Observador de Fondo</strong> → el usuario solo puede ver el fondo asignado. "
            "No puede editar nada. Perfecto para socios que quieren seguir el fondo sin tocar datos."
        )
        info_box(
            "El fondo es <strong>opcional</strong>. Si no asignas fondo, el usuario tendrá un "
            "portafolio personal con su propio espacio de datos.",
            color="#8BA5C8"
        )

        with st.form("form_usr", clear_on_submit=True):
            cu1,cu2 = st.columns(2)
            u_email  = cu1.text_input("Email del usuario (será su login)")
            u_nombre = cu2.text_input("Nombre / Empresa")

            cu3,cu4,cu5 = st.columns(3)
            u_pwd  = cu3.text_input("Contraseña inicial", type="password",
                        help="Mínimo 6 caracteres.")
            u_modo = cu4.selectbox("Modo de acceso", [MODO_INDIVIDUAL, MODO_OBSERVADOR],
                        help="Portafolio Individual: puede registrar y editar sus operaciones.\n"
                             "Observador de Fondo: solo lectura del fondo asignado.")
            # Fondo opcional
            fondos_con_ninguno = ["(Sin fondo — portafolio personal)"] + fondos_list
            u_fondo_sel = cu5.selectbox("Fondo asignado (opcional)", fondos_con_ninguno)
            u_fondo = "" if u_fondo_sel.startswith("(Sin fondo") else u_fondo_sel

            if st.form_submit_button("👤 CREAR USUARIO Y DAR ACCESO", use_container_width=True):
                if not u_email.strip() or not u_nombre.strip() or not u_pwd.strip():
                    st.error("❌ Email, nombre y contraseña son obligatorios")
                elif len(u_pwd) < 6:
                    st.error("❌ La contraseña debe tener mínimo 6 caracteres")
                elif u_modo == MODO_OBSERVADOR and not u_fondo:
                    st.error("❌ El modo Observador de Fondo requiere asignar un fondo")
                else:
                    with st.spinner("Creando acceso en Firebase…"):
                        ok_fb, msg_fb = firebase_crear(u_email.strip(), u_pwd.strip())
                    if ok_fb or "EMAIL_EXISTS" in str(msg_fb):
                        fs_post("usuarios", {
                            "Email":     u_email.strip().lower(),
                            "Nombre":    u_nombre.strip(),
                            "Modo":      u_modo,
                            "Fondo":     u_fondo,
                            "Activo":    "Si",
                            "CreadoPor": usuario,
                            "Fecha":     str(date.today()),
                        })  # resultado ignorado intencionalmente
                        if "EMAIL_EXISTS" in str(msg_fb):
                            st.warning(f"⚠ El email ya existía. Se actualizó su perfil → Modo: {u_modo}"
                                       + (f" · Fondo: {u_fondo}" if u_fondo else " · Sin fondo asignado"))
                        else:
                            st.success(f"✓ Usuario creado: {u_email} → {u_modo}"
                                       + (f" · Fondo: {u_fondo}" if u_fondo else " · Portafolio personal"))
                        st.cache_data.clear()
                    else:
                        st.error(f"❌ Firebase: {msg_fb}")

        # Lista de usuarios
        st.markdown("---"); sec("Usuarios con acceso")
        df_u2 = load_usuarios()
        if not df_u2.empty:
            show_u = [c for c in ["Email","Nombre","Modo","Fondo","Activo","Fecha"] if c in df_u2.columns]
            st.dataframe(df_u2[show_u], use_container_width=True, hide_index=True)

            sec("Eliminar acceso")
            ul = [f"{r.get('Email','?')} — {r.get('Nombre','?')} ({r.get('Modo','?')})"
                  for _,r in df_u2.iterrows()]
            su = st.selectbox("Usuario a eliminar", range(len(ul)),
                              format_func=lambda i: ul[i], key="su_e")
            if su is not None:
                sur = df_u2.iloc[su]
                if st.button("🗑 Eliminar acceso de este usuario"):
                    fs_delete("usuarios", sur["_id"])
                    st.success(f"✓ Acceso eliminado para {sur.get('Email','?')}")
                    st.cache_data.clear(); st.rerun()
        else:
            st.info("Aún no has creado usuarios con acceso.")

# ══════════════════════════════════════════════════════════════
# ADMINISTRACIÓN (admin)
# ══════════════════════════════════════════════════════════════
if rol == "admin":
    with t_adm:
        sec("Panel de administración")
        ca1,ca2 = st.columns(2)
        with ca1:
            sec("Resumen por fondo")
            rows_r = []
            for f in fondos_list:
                cap = df_ap_all[df_ap_all["Fondo"]==f]["Monto"].sum() if not df_ap_all.empty else 0
                nop = len(df_ops_all[df_ops_all["Fondo"]==f]) if not df_ops_all.empty else 0
                rows_r.append({"Fondo":f, "Capital USD":cap*factor, "# Ops":nop})
            st.dataframe(pd.DataFrame(rows_r).style.format({"Capital USD":"${:,.2f}"}),
                         use_container_width=True, hide_index=True)

            sec("Crear nuevo fondo")
            nf_i = st.text_input("Nombre del fondo", key="nf_adm")
            if st.button("➕ CREAR FONDO"):
                if nf_i.strip() and nf_i not in fondos_list:
                    fs_post("aportes",{"Fondo":nf_i.strip(),"Socio":"","Cedula":"",
                                       "Fecha":str(date.today()),"Tipo":"Aporte",
                                       "Monto":0.0,"TipoCuenta":"Fondo Grupal","Usuario":usuario})  # ok ignorado
                    st.success(f"✓ Fondo '{nf_i}' creado")
                    st.cache_data.clear(); st.rerun()
                elif nf_i in fondos_list:
                    st.warning("Ese fondo ya existe")

        with ca2:
            sec("Estado de APIs")
            st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
                border-radius:8px;padding:14px;font:400 11px/1.9 IBM Plex Mono,mono">
              <div style="color:#8BA5C8;font-size:9px;letter-spacing:1px;margin-bottom:8px">FUENTES ACTIVAS</div>
              <div style="color:#F0C040">● CoinMarketCap API — Cripto</div>
              <div style="color:#C8A84B">● Yahoo Finance — Acciones / ETF</div>
              <div style="color:#2ECC87">● ExchangeRate-API / Frankfurter — TRM</div>
              <div style="color:#8BA5C8;font-size:9px;margin-top:10px">
                TRM: ${trm:,.2f} · CMC: …{CMC_KEY[-6:]}<br>
                Caché precios: 5 min · TRM: 1 hora</div></div>""",
                unsafe_allow_html=True)
            if st.button("🔄 Limpiar caché"):
                st.cache_data.clear()
                st.success("✓ Caché limpiado")

        st.markdown("---"); sec("Todas las operaciones")
        if not df_ops_all.empty:
            cols_a = [c for c in ["Fondo","Usuario","Fecha","Activo","Categoria",
                                   "Valor_Pos","Resultado"] if c in df_ops_all.columns]
            dfa = df_ops_all[cols_a].sort_values("Fecha",ascending=False).copy() if "Fecha" in cols_a else df_ops_all[cols_a]
            if "Valor_Pos" in dfa.columns: dfa["Valor_Pos"] = dfa["Valor_Pos"]*factor
            st.dataframe(dfa.style.format({"Valor_Pos":"${:,.2f}"}),
                         use_container_width=True, hide_index=True)
        else:
            st.info("Sin operaciones registradas aún.")
