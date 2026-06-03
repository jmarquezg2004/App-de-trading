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

/* Variables de tema — oscuro por defecto */
:root {
    --bg:         #111827;
    --sidebar-bg: #0D1929;
    --surface:    #162236;
    --surface2:   #0F1A2B;
    --border:     #1E3354;
    --text:       #ffffff;
    --muted:      #8BA5C8;
    --label:      #B0C4DC;
}
/* Tema claro */
body.tema-claro {
    --bg:         #F0F4F8;
    --sidebar-bg: #E2EAF4;
    --surface:    #FFFFFF;
    --surface2:   #EDF2F7;
    --border:     #C4D4E8;
    --text:       #1A2640;
    --muted:      #4A6080;
    --label:      #3A5070;
}

html, body { font-family: 'IBM Plex Sans', sans-serif; }
.stApp { background: var(--bg); color: var(--text); }
h1 { font-family:'IBM Plex Mono',monospace!important; color:#C8A84B!important; letter-spacing:2px; }
h2 { font-family:'IBM Plex Mono',monospace!important; font-size:11px!important; letter-spacing:1.5px; text-transform:uppercase; color:var(--muted)!important; }
h3 { font-family:'IBM Plex Mono',monospace!important; font-size:13px!important; color:#C8A84B!important; }
hr { border-color:var(--border)!important; }

section[data-testid="stSidebar"] { background:var(--sidebar-bg)!important; border-right:1px solid var(--border); }
section[data-testid="stSidebar"] label { color:var(--muted)!important; font-size:12px!important; }

/* TODOS los inputs */
input, textarea {
    background:var(--surface)!important; color:var(--text)!important;
    -webkit-text-fill-color:var(--text)!important;
    border:1px solid var(--border)!important; border-radius:6px!important;
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
    background:var(--surface)!important; border:1px solid var(--border)!important;
    border-radius:6px!important; color:var(--text)!important;
}
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] p { color:#ffffff!important; font-size:13px!important; }

/* Dropdown abierto */
[data-baseweb="popover"], [data-baseweb="popover"] *,
[data-baseweb="menu"], [data-baseweb="menu"] *,
[role="listbox"], [role="listbox"] * {
    background:var(--surface)!important; color:var(--text)!important;
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
    background:var(--surface); border:1px solid var(--border); border-radius:10px;
    padding:16px!important; position:relative; overflow:hidden;
}
[data-testid="metric-container"]::before {
    content:''; position:absolute; top:0;left:0;right:0; height:2px;
    background:linear-gradient(90deg,#C8A84B,#A07830);
}
[data-testid="stMetricValue"] {
    font-family:'IBM Plex Mono',monospace!important; font-size:1.4rem!important;
    color:var(--text)!important; font-weight:600!important;
}
[data-testid="stMetricLabel"] {
    font-family:'IBM Plex Mono',monospace!important; font-size:0.68rem!important;
    letter-spacing:1.2px; text-transform:uppercase; color:#8BA5C8!important;
}

/* DataFrames */
[data-testid="stDataFrame"] { border:1px solid var(--border); border-radius:8px; overflow:hidden; }

/* Alerts */
[data-testid="stAlert"] {
    border-radius:8px!important; border-left-width:3px!important;
    background:var(--surface)!important; font-family:'IBM Plex Mono',monospace!important; color:#ffffff!important;
}

/* Form */
[data-testid="stForm"] {
    background:var(--bg)!important; border:1px solid var(--border)!important;
    border-radius:10px!important; padding:20px!important;
}

/* Radio */
[data-testid="stRadio"] label span,
[data-testid="stRadio"] label p,
[data-testid="stRadio"] p { color:#ffffff!important; font-weight:600!important; }
</style>
""", unsafe_allow_html=True)

# ── Tema claro — sobreescribe variables oscuras ──────────
_tc = st.session_state.get("tema_sel", "🌙 Oscuro") == "☀️ Claro"
if _tc:
    st.markdown("""<style>
    .stApp { background:#F0F4F8 !important; color:#1A2640 !important; }
    section[data-testid="stSidebar"] { background:#E2EAF4 !important; }
    section[data-testid="stSidebar"] * { color:#1A2640 !important; }
    input, textarea {
        background:#FFFFFF !important; color:#1A2640 !important;
        -webkit-text-fill-color:#1A2640 !important; border-color:#C4D4E8 !important;
    }
    input::placeholder, textarea::placeholder {
        color:#6A8090 !important; -webkit-text-fill-color:#6A8090 !important;
    }
    input:disabled { color:#C8A84B !important; -webkit-text-fill-color:#C8A84B !important; }
    [data-testid="stSelectbox"]>div>div {
        background:#FFFFFF !important; color:#1A2640 !important; border-color:#C4D4E8 !important;
    }
    [data-testid="stSelectbox"] span,
    [data-testid="stSelectbox"] p { color:#1A2640 !important; }
    [data-baseweb="popover"], [data-baseweb="popover"] *,
    [data-baseweb="menu"], [data-baseweb="menu"] *,
    [role="listbox"], [role="listbox"] * {
        background:#FFFFFF !important; color:#1A2640 !important;
    }
    [role="option"]:hover { background:#E2EAF4 !important; color:#C8A84B !important; }
    [data-testid="metric-container"] {
        background:#FFFFFF !important; border-color:#C4D4E8 !important;
    }
    [data-testid="stMetricValue"] { color:#1A2640 !important; }
    [data-testid="stMetricLabel"] { color:#4A6080 !important; }
    [data-testid="stForm"] { background:#EDF2F7 !important; border-color:#C4D4E8 !important; }
    [data-testid="stDataFrame"] { border-color:#C4D4E8 !important; }
    [data-testid="stAlert"] { background:#FFFFFF !important; color:#1A2640 !important; }
    [data-testid="stTabs"] button { color:#4A6080 !important; background:transparent !important; }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color:#C8A84B !important; border-bottom-color:#C8A84B !important;
    }
    [data-testid="stRadio"] label span,
    [data-testid="stRadio"] label p { color:#1A2640 !important; font-weight:600 !important; }
    [data-testid="stNumberInput"] button {
        background:#E2EAF4 !important; color:#1A2640 !important; border-color:#C4D4E8 !important;
    }
    hr { border-color:#C4D4E8 !important; }
    h1 { color:#C8A84B !important; }
    h2 { color:#4A6080 !important; }
    h3 { color:#A07830 !important; }
    .stButton>button { color:#0D1929 !important; }
    </style>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# CONSTANTES
# ══════════════════════════════════════════════════════
FIREBASE_KEY = "AIzaSyC52gIJJRTE1B4BqeUwDmaX2fWKS3sSw10"
FS_URL       = "https://firestore.googleapis.com/v1/projects/plataforma-de-inversiones/databases/(default)/documents"
ADMIN_EMAIL  = "jmarquezg2004@gmail.com"
CMC_KEY      = st.secrets.get("CMC_KEY", "d67913f039804c6b900905ebad7c1aaf")

CATEGORIAS = [
    # ── Mercados digitales ──
    "Acción", "ETF", "Cripto", "CDT", "Fondo", "Cuenta Remunerada",
    # ── Activos reales / alternativos ──
    "Inmueble",         # apartamentos, casas, lotes, fincas
    "Negocio",          # empresa propia o participación
    "Ganadería",        # animales de cría, criaderos
    "Vehículo",         # vehículos en alquiler
    "Dividendo",        # dividendos, herencias, fideicomisos
    "Seguro",           # seguros en dólares, pólizas de inversión
    "Arriendo",         # ingresos por arrendamiento
    "Otro",
]
# Categorías sin precio de mercado (el usuario actualiza el valor manualmente)
CATS_MANUALES = {"Inmueble","Negocio","Ganadería","Vehículo","Dividendo","Seguro","Arriendo","Otro"}
# Colores por categoría
CAT_CLR_MAP = {
    "Acción":"#C8A84B","ETF":"#2ECC87","Cripto":"#E87844",
    "CDT":"#6BA3BE","Fondo":"#9B8EC4","Cuenta Remunerada":"#F0C040",
    "Inmueble":"#E85555","Negocio":"#FF9F43","Ganadería":"#A29BFE",
    "Vehículo":"#55EFC4","Dividendo":"#FFEAA7","Seguro":"#74B9FF",
    "Arriendo":"#FD79A8","Otro":"#8BA5C8",
}
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

def _auth_header():
    """Retorna header de autorización con el token del usuario logueado."""
    token = st.session_state.get("auth_token", "")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def fs_get(col, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else _auth_header()
    try:
        r = requests.get(f"{FS_URL}/{col}", headers=headers, timeout=10)
        if r.status_code == 200:
            docs = r.json().get("documents", [])
            rows = [{"_id": d["name"].split("/")[-1],
                     **{k: list(v.values())[0] for k, v in d.get("fields", {}).items()}}
                    for d in docs]
            return pd.DataFrame(rows) if rows else pd.DataFrame()
    except Exception: pass
    return pd.DataFrame()

def fs_post(col, datos, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else _auth_header()
    try:
        r = requests.post(f"{FS_URL}/{col}",
                          headers=headers,
                          json={"fields": {k: _f(v) for k, v in datos.items()}}, timeout=10)
        if r.status_code in (200, 201): return True, ""
        return False, f"Error {r.status_code}: {r.text[:300]}"
    except Exception as e: return False, str(e)

def fs_patch(col, doc_id, datos, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else _auth_header()
    mask = "&".join(f"updateMask.fieldPaths={k}" for k in datos)
    try:
        requests.patch(f"{FS_URL}/{col}/{doc_id}?{mask}",
                       headers=headers,
                       json={"fields": {k: _f(v) for k, v in datos.items()}}, timeout=10)
        return True
    except Exception: return False

def fs_delete(col, doc_id, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else _auth_header()
    try:
        requests.delete(f"{FS_URL}/{col}/{doc_id}", headers=headers, timeout=10)
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
    """Solo obtiene precios de posiciones ABIERTAS — cerradas/archivadas no necesitan precio en vivo."""
    out = {}
    if df.empty: return out
    # Filtrar solo posiciones abiertas
    df_ab = df[df["Estado"] == "Abierta"] if "Estado" in df.columns else df
    if df_ab.empty: return out
    criptos = [x.strip().upper() for x in df_ab[df_ab["Categoria"]=="Cripto"]["Ticker_API"].dropna() if x.strip()]
    if criptos: out.update(get_cmc(tuple(set(criptos))))
    stocks = [x.strip().upper() for x in df_ab[df_ab["Categoria"].isin(["Acción","ETF","Fondo"])]["Ticker_API"].dropna() if x.strip()]
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

@st.cache_data(ttl=60, show_spinner=False)
def load_inv():
    """Lee colección 'inversiones' (nueva) + 'operaciones' (legacy) y unifica formato."""

    COLS = ["_id","Fondo","Usuario","Fecha_Compra","Activo","Categoria",
            "Cantidad","Precio_Compra","Broker","Ticker_API",
            "Fecha_Venta","Precio_Venta","Estado","Notas"]

    def normalizar(df):
        num = ["Cantidad","Precio_Compra","Precio_Venta"]
        for c in num:
            if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
            else: df[c] = 0.0
        for c in COLS:
            if c not in df.columns: df[c] = ""
        return df[COLS]

    # ── Colección nueva: inversiones ──────────────────────
    df_new = fs_get("inversiones")
    if not df_new.empty:
        df_new = normalizar(df_new)
    else:
        df_new = pd.DataFrame(columns=COLS)

    # ── Colección legacy: operaciones → convertir al formato nuevo ──
    df_ops = fs_get("operaciones")
    rows_legacy = []
    if not df_ops.empty:
        for _, r in df_ops.iterrows():
            # Mapeo de campos operaciones → inversiones
            resultado = str(r.get("Resultado","Abierta"))
            if resultado == "Abierta":
                estado = "Abierta"
                fv, pv = "", 0.0
            elif resultado in ("Ganadora","Perdedora","Cancelada"):
                estado = "Cerrada"
                # Precio de venta aproximado desde TP/SL o precio entrada
                pe = float(r.get("Precio_Entrada",0) or 0)
                tp = float(r.get("TP_%",0) or r.get("TP_pct",0) or 0)
                sl = float(r.get("SL_%",0) or r.get("SL_pct",0) or 0)
                if resultado == "Ganadora" and tp > 0:
                    pv = pe * (1 + tp/100)
                elif resultado == "Perdedora" and sl > 0:
                    pv = pe * (1 - sl/100)
                else:
                    pv = pe
                fv = str(r.get("Fecha",""))
            else:
                estado = "Abierta"
                fv, pv = "", 0.0

            # Cantidad: usar Cantidad si existe, sino calcular desde Valor_Pos / Precio_Entrada
            cant = float(r.get("Cantidad",0) or 0)
            pe   = float(r.get("Precio_Entrada",0) or 0)
            vp   = float(r.get("Valor_Pos",0) or 0)
            if cant == 0 and pe > 0 and vp > 0:
                cant = round(vp / pe, 8)

            # Categoria: mapear si viene de campo "Categoria" o "Moneda"
            cat = str(r.get("Categoria","") or r.get("Moneda","") or "Otro")

            rows_legacy.append({
                "_id":           str(r.get("_id","")),
                "Fondo":         str(r.get("Fondo","")),
                "Usuario":       str(r.get("Usuario","")),
                "Fecha_Compra":  str(r.get("Fecha","")),
                "Activo":        str(r.get("Activo","") or r.get("Moneda","")),
                "Categoria":     cat,
                "Cantidad":      cant,
                "Precio_Compra": pe,
                "Broker":        str(r.get("Broker","")),
                "Ticker_API":    str(r.get("Ticker_API","")),
                "Fecha_Venta":   fv,
                "Precio_Venta":  pv,
                "Estado":        estado,
                "Notas":         str(r.get("Notas","")),
            })

    if rows_legacy:
        df_leg = pd.DataFrame(rows_legacy)
        df_leg["Cantidad"]      = pd.to_numeric(df_leg["Cantidad"],      errors="coerce").fillna(0.0)
        df_leg["Precio_Compra"] = pd.to_numeric(df_leg["Precio_Compra"], errors="coerce").fillna(0.0)
        df_leg["Precio_Venta"]  = pd.to_numeric(df_leg["Precio_Venta"],  errors="coerce").fillna(0.0)
    else:
        df_leg = pd.DataFrame(columns=COLS)

    # Unir ambas — los _id de operaciones tienen prefijo para no colisionar
    if not df_leg.empty:
        df_leg["_id"] = "ops_" + df_leg["_id"].astype(str)

    # Deduplicar: si ya existe en inversiones (df_new) con mismo Activo+Fecha_Compra+Usuario,
    # no incluir la versión legacy para evitar duplicados tras migración
    if not df_new.empty and not df_leg.empty:
        keys_new = set(
            zip(df_new["Activo"].str.upper().str.strip(),
                df_new["Fecha_Compra"].astype(str).str[:10],
                df_new["Usuario"].str.lower().str.strip())
        )
        mask_dup = df_leg.apply(
            lambda r: (
                str(r["Activo"]).upper().strip(),
                str(r["Fecha_Compra"])[:10],
                str(r["Usuario"]).lower().strip()
            ) in keys_new,
            axis=1
        )
        df_leg = df_leg[~mask_dup]

    combined = pd.concat([df_new, df_leg], ignore_index=True)
    return combined if not combined.empty else pd.DataFrame(columns=COLS)

@st.cache_data(ttl=60, show_spinner=False)
def load_aportes():
    df = fs_get("aportes")
    if df.empty:
        return pd.DataFrame(columns=["_id","Fondo","Socio","Fecha","Tipo","Monto","Usuario"])
    if "Monto" in df.columns: df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce").fillna(0.0)
    return df

@st.cache_data(ttl=60, show_spinner=False)
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
# CAT_CLR migrado a CAT_CLR_MAP en CATEGORIAS

def money(v, f=1):
    v2 = v * f
    if abs(v2) >= 1e6: return f"${v2/1e6:.2f}M"
    return f"${v2:,.2f}"

def card(label, val, sub=None, color="#C8A84B"):
    s = f'<div style="font:500 11px/1.4 IBM Plex Mono,mono;color:{color};margin-top:3px">{sub}</div>' if sub else ""
    return f"""<div style="background:var(--surface);border:1px solid var(--border);border-radius:10px;
        padding:16px 18px;position:relative;overflow:hidden;height:100%">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;background:{color}"></div>
      <div style="font:400 9px/1 IBM Plex Mono,mono;color:var(--muted);letter-spacing:1.5px;
                  text-transform:uppercase;margin-bottom:8px">{label}</div>
      <div style="font:600 22px/1 IBM Plex Mono,mono;color:var(--text)">{val}</div>{s}</div>"""

def sec(t):
    st.markdown(f'<h2 style="margin:18px 0 10px">{t}</h2>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("""<div style="text-align:center;padding:50px 0 24px">
      <div style="display:inline-block;margin-bottom:10px">
        <svg width="54" height="54" viewBox="0 0 54 54" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#D4A843"/>
      <stop offset="100%" style="stop-color:#8B6914"/>
    </linearGradient>
  </defs>
  <!-- Hexágono de fondo -->
  <polygon points="27,2 52,15 52,39 27,52 2,39 2,15"
           fill="url(#gold)" stroke="#A07830" stroke-width="1"/>
  <!-- Letra A -->
  <text x="27" y="38" text-anchor="middle"
        font-family="IBM Plex Sans,Arial,sans-serif"
        font-size="28" font-weight="700" fill="#0D1929">A</text>
</svg>
      </div><br>
      <div style="font:600 28px/1 IBM Plex Mono,mono;color:#C8A84B;letter-spacing:4px;margin-top:4px">ARKEZ</div>
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
                    em    = email.strip().lower()
                    rol   = "admin" if em == ADMIN_EMAIL.lower() else "usuario"
                    token = result.get("idToken", "")   # ← token de Firebase Auth
                    df_u  = load_usuarios()
                    modo_u = MODO_IND; fondo_u = None
                    if not df_u.empty and "Email" in df_u.columns:
                        fila = df_u[df_u["Email"].str.lower() == em]
                        if not fila.empty:
                            modo_u  = fila.iloc[0].get("Modo", MODO_IND)
                            fondo_u = fila.iloc[0].get("Fondo") or None
                    st.session_state.update({
                        "logged_in": True, "usuario": em, "rol": rol,
                        "modo": modo_u, "fondo_asignado": fondo_u,
                        "fondo_sel": "Arkez Invest",
                        "auth_token": token,   # ← guardamos el token
                    })
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
            else:
                st.warning("Completa los dos campos")

        # ── Recuperar contraseña ──────────────────────────────
        st.markdown("""<div style="text-align:center;margin-top:10px">
          <span style="font:400 12px IBM Plex Mono,mono;color:#8BA5C8">
            ¿Olvidaste tu contraseña? →</span></div>""", unsafe_allow_html=True)
        if st.button("Enviar correo de recuperación", key="btn_reset",
                     help="Te enviaremos un email para resetear tu contraseña"):
            if email.strip():
                with st.spinner("Enviando correo de recuperación…"):
                    try:
                        r_reset = requests.post(
                            f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_KEY}",
                            json={"requestType": "PASSWORD_RESET", "email": email.strip()},
                            timeout=8
                        )
                        if r_reset.status_code == 200:
                            st.success(f"✓ Correo enviado a {email.strip()} — revisa tu bandeja de entrada")
                        else:
                            err = r_reset.json().get("error", {}).get("message", "Error")
                            st.error(f"❌ {err}")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.warning("Primero escribe tu correo electrónico")
        st.markdown('</div>', unsafe_allow_html=True)
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
    st.markdown("""<div style="text-align:center;padding:14px 0 8px">
      <div style="display:inline-block;margin-bottom:6px"><svg width="36" height="36" viewBox="0 0 54 54" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="g2" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" style="stop-color:#D4A843"/>
    <stop offset="100%" style="stop-color:#8B6914"/>
  </linearGradient></defs>
  <polygon points="27,2 52,15 52,39 27,52 2,39 2,15" fill="url(#g2)" stroke="#A07830" stroke-width="1"/>
  <text x="27" y="38" text-anchor="middle" font-family="IBM Plex Sans,Arial,sans-serif"
        font-size="28" font-weight="700" fill="#0D1929">A</text>
</svg></div><br>
      <div style="font:600 13px/1 IBM Plex Mono,mono;color:#C8A84B;letter-spacing:3px">ARKEZ</div>
    </div>""", unsafe_allow_html=True)

    rc = "#C8A84B" if rol=="admin" else "#2ECC87"
    st.markdown(f"""<div style="background:#152034;border:1px solid #1E3354;border-radius:8px;
        padding:10px 12px;margin-bottom:10px">
      <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px;margin-bottom:3px">USUARIO</div>
      <div style="font:400 11px/1.4 IBM Plex Mono,mono;color:var(--text);word-break:break-all">{usuario}</div>
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
        st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);border-radius:6px;
            padding:8px 12px;margin-bottom:8px">
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted)">FONDO / PORTAFOLIO</div>
          <div style="font:600 12px IBM Plex Mono,mono;color:#C8A84B">{fondo}</div>
        </div>""", unsafe_allow_html=True)

    trm = get_trm()
    st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;
        padding:9px 12px;margin:8px 0">
      <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted);letter-spacing:1px">TRM USD/COP</div>
      <div style="font:600 16px/1.5 IBM Plex Mono,mono;color:#F0C040">${trm:,.2f}</div>
    </div>""", unsafe_allow_html=True)

    moneda = st.radio("Moneda", ["USD","COP"], horizontal=True)
    factor = trm if moneda=="COP" else 1.0
    sfx    = " COP" if moneda=="COP" else " USD"

    st.markdown("---")
    tema = st.radio("🎨 Tema", ["🌙 Oscuro","☀️ Claro"], horizontal=True,
                    key="tema_sel")
    tema_claro = tema == "☀️ Claro"

    st.markdown("---")
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# ══════════════════════════════════════════════════════
# FILTRAR DATOS
# ══════════════════════════════════════════════════════
def inv_visibles(df):
    """
    Reglas de visibilidad:
    - Admin: ve fondos GRUPALES. NO ve portafolios individuales de otros.
    - Observador: ve solo lectura del fondo grupal asignado.
    - Portafolio individual: SOLO ve sus propias inversiones (ni admin puede verlas en la UI).
    """
    if df.empty: return df

    if rol == "admin":
        # Admin ve el fondo seleccionado, EXCEPTO inversiones de portafolios individuales ajenos
        df_fondo = df[df["Fondo"] == fondo].copy()
        # Excluir registros cuyo Usuario no sea el admin y cuyo fondo sea personal_*
        if "Usuario" in df_fondo.columns and "Fondo" in df_fondo.columns:
            es_personal_ajeno = (
                df_fondo["Fondo"].str.startswith("personal_", na=False) &
                (df_fondo["Usuario"].str.lower() != usuario)
            )
            df_fondo = df_fondo[~es_personal_ajeno]
        return df_fondo

    if modo == MODO_OBS:
        # Observador: solo lectura del fondo grupal asignado
        return df[df["Fondo"] == fondo]

    # Portafolio individual: SOLO sus propias inversiones, sin importar el fondo
    mask = pd.Series([False] * len(df), index=df.index)
    if "Usuario" in df.columns:
        mask = mask | (df["Usuario"].str.lower() == usuario.lower())
    if "Fondo" in df.columns:
        mask = mask | (df["Fondo"] == fondo)
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

# Cash neto: depósitos extra + retiros (no son compras de activos)
# Aporte = entró dinero al fondo/portafolio
# Retiro = salió dinero → reduce el valor real del portafolio
cash_aportes = 0.0
cash_retiros = 0.0
if not df_ap.empty and "Tipo" in df_ap.columns:
    cash_aportes = df_ap[df_ap["Tipo"]=="Aporte"]["Monto"].sum()
    cash_retiros = df_ap[df_ap["Tipo"]=="Retiro"]["Monto"].sum()
cash_neto = cash_aportes - cash_retiros  # positivo = hay cash disponible, negativo = retiraron más

# Portafolio real = valor de posiciones abiertas + cash neto (retiros ya restan)
# Si hay retiros, el valor total baja aunque las posiciones estén bien
total_actual_real = total_actual + max(cash_neto, 0)  # solo suma cash si es positivo
total_gp_real     = total_gp + cash_neto if cash_neto < 0 else total_gp
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
    """
    Lógica correcta de período:
    - "Todo el historial": incluye todo
    - Para filtros específicos:
      * Posiciones ABIERTAS: siempre se incluyen (siguen vigentes hoy)
      * Posiciones CERRADAS: se incluyen si la fecha de VENTA cae dentro del período
      * Posiciones ARCHIVADAS: se excluyen siempre del portafolio activo
    """
    if f_ini is None: return True
    estado = p.get("Estado", "Abierta")
    if estado == "Archivada": return False
    if estado == "Abierta": return True  # posición abierta siempre es "actual"
    # Cerrada: incluir si la fecha de venta está en el período seleccionado
    try:
        fv = pd.to_datetime(p["F_Venta"]) if p["F_Venta"] else hoy
        return f_ini <= fv <= f_fin
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

# ── Indicadores de análisis (fila secundaria) ─────────────
ops_cerradas_calc = [p for p in posiciones if p["Estado"]=="Cerrada"]
if posiciones and ops_cerradas_calc:
    pnls = [p["GP_usd"] for p in ops_cerradas_calc]
    gans = [x for x in pnls if x > 0]
    pers = [x for x in pnls if x < 0]
    avg_g = sum(gans)/len(gans) if gans else 0
    avg_p = abs(sum(pers)/len(pers)) if pers else 0
    # R/R Ratio: ganancia promedio / pérdida promedio
    rr = avg_g / avg_p if avg_p > 0 else 0
    # Esperanza matemática: WR*AvgGan - (1-WR)*AvgPer
    wr_dec = len(gans)/len(pnls) if pnls else 0
    esperanza = wr_dec * avg_g - (1 - wr_dec) * avg_p
    # Profit Factor: suma ganancias / suma pérdidas
    pf = sum(gans)/abs(sum(pers)) if pers else 0

    ind1, ind2, ind3, ind_sep = st.columns([1,1,1,2])
    with ind1:
        rr_color = "#2ECC87" if rr >= 1 else "#E85555"
        st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);
            border-radius:8px;padding:10px 14px;border-left:3px solid {rr_color}">
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted);letter-spacing:1px">R/R RATIO</div>
          <div style="font:600 18px IBM Plex Mono,mono;color:{rr_color}">{rr:.2f}</div>
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted)">
            {'✓ Favorable' if rr>=1 else '✗ Desfavorable'} (meta: >1.0)</div>
        </div>""", unsafe_allow_html=True)
    with ind2:
        esp_color = "#2ECC87" if esperanza > 0 else "#E85555"
        st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);
            border-radius:8px;padding:10px 14px;border-left:3px solid {esp_color}">
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted);letter-spacing:1px">ESPERANZA MATEMÁTICA</div>
          <div style="font:600 18px IBM Plex Mono,mono;color:{esp_color}">
            {'+'if esperanza>=0 else ''}{money(esperanza,factor)}</div>
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted)">
            Por operación cerrada</div>
        </div>""", unsafe_allow_html=True)
    with ind3:
        pf_color = "#2ECC87" if pf >= 1 else "#E85555"
        st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);
            border-radius:8px;padding:10px 14px;border-left:3px solid {pf_color}">
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted);letter-spacing:1px">PROFIT FACTOR</div>
          <div style="font:600 18px IBM Plex Mono,mono;color:{pf_color}">{pf:.2f}x</div>
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted)">
            {'✓ Sistema rentable' if pf>=1 else '✗ Sistema no rentable'} (meta: >1.0)</div>
        </div>""", unsafe_allow_html=True)
    with ind_sep:
        st.markdown(f"""<div style="padding:10px 14px">
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted);margin-bottom:4px">
            Basado en {len(pnls)} ops cerradas · Avg gan: +{money(avg_g,factor)} · Avg per: -{money(avg_p,factor)}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════
puede_registrar = (rol=="admin") or (modo==MODO_IND)

if rol == "admin":
    tabs = st.tabs(["⬡ Dashboard","◈ Portafolio","📌 Registrar","💵 Capital","👥 Usuarios","⚙ Admin"])
    t_dash,t_port,t_reg,t_cap,t_usr,t_adm = tabs
elif puede_registrar:
    tabs = st.tabs(["⬡ Dashboard","◈ Mi portafolio","📌 Registrar","💵 Capital"])
    t_dash,t_port,t_reg,t_cap = tabs
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
        if pos_periodo:
            # Serie de puntos: fecha_compra con valor invertido, fecha_actual/venta con valor actual
            # Para cada posición construimos dos puntos y luego interpolamos
            eventos = []
            for p in pos_periodo:
                try:
                    fc = pd.to_datetime(p["F_Compra"])
                    fv = pd.to_datetime(p["F_Venta"]) if p["F_Venta"] else pd.Timestamp.now().normalize()
                    # Punto de entrada: el día de compra el valor era = invertido
                    eventos.append({"fecha": fc, "invertido": p["Invertido"], "actual": p["Invertido"]})
                    # Punto de salida: valor actual (precio de hoy o de venta)
                    eventos.append({"fecha": fv, "invertido": p["Invertido"], "actual": p["Val_Actual"]})
                except: pass

            if eventos:
                df_ev = pd.DataFrame(eventos).sort_values("fecha")
                # Agrupar por fecha sumando todas las posiciones activas en ese momento
                df_val = df_ev.groupby("fecha").agg(
                    invertido=("invertido","sum"),
                    actual=("actual","sum")
                ).reset_index()
                df_val["invertido"] *= factor
                df_val["actual"]    *= factor

                fig = go.Figure()
                # Área de valor actual (portafolio)
                fig.add_trace(go.Scatter(
                    x=df_val["fecha"], y=df_val["actual"],
                    mode="lines+markers",
                    line=dict(color="#C8A84B", width=2.5),
                    fill="tozeroy", fillcolor="rgba(200,168,75,0.08)",
                    marker=dict(color="#C8A84B", size=7,
                                line=dict(color="#111827", width=1.5)),
                    name=f"Valor ({moneda})",
                    hovertemplate="<b>%{x|%d/%m/%Y}</b><br>Valor: %{y:$,.2f}"+sfx+"<extra></extra>"
                ))
                # Línea de capital invertido
                fig.add_trace(go.Scatter(
                    x=df_val["fecha"], y=df_val["invertido"],
                    mode="lines",
                    line=dict(color="#38BDF8", width=2, dash="dash"),
                    name=f"Invertido ({moneda})",
                    hovertemplate="Invertido: %{y:$,.2f}"+sfx+"<extra></extra>"
                ))
                # Zona verde/roja entre ambas líneas
                fig.add_trace(go.Scatter(
                    x=list(df_val["fecha"])+list(df_val["fecha"][::-1]),
                    y=list(df_val["actual"])+list(df_val["invertido"][::-1]),
                    fill="toself",
                    fillcolor="rgba(46,204,135,0.07)" if gp_per>=0 else "rgba(232,85,85,0.07)",
                    line=dict(color="rgba(0,0,0,0)"),
                    showlegend=False, hoverinfo="skip"
                ))
                fig.update_layout(**PT,
                    title=dict(text=f"Portafolio vs Capital invertido ({moneda})",
                               font=dict(size=11,color="#8BA5C8"),x=.5),
                    yaxis_title=moneda,
                    legend=dict(bgcolor="rgba(0,0,0,0)",
                                font=dict(color="#8BA5C8",size=10),
                                orientation="h", y=-0.15))
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

            # Mini resumen textual bajo la gráfica
            gp_color = "#2ECC87" if gp_per>=0 else "#E85555"
            st.markdown(f"""<div style="display:flex;gap:24px;flex-wrap:wrap;padding:8px 4px">
              <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">INVERTIDO</div>
                <div style="font:600 14px IBM Plex Mono,mono;color:var(--text)">{money(inv_per,factor)}{sfx}</div></div>
              <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">VALOR HOY</div>
                <div style="font:600 14px IBM Plex Mono,mono;color:var(--text)">{money(act_per,factor)}{sfx}</div></div>
              <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">GANANCIA TOTAL</div>
                <div style="font:600 14px IBM Plex Mono,mono;color:{gp_color}">
                  {'+'if gp_per>=0 else ''}{money(gp_per,factor)}{sfx} ({'+' if rend_per>=0 else ''}{rend_per:.2f}%)</div></div>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Registra tu primera inversión para ver la gráfica.")

    with cr:
        pos_ab_activas = [p for p in posiciones if p["Estado"]=="Abierta"]
        vista_donut = st.radio("Ver distribución por",
                               ["📊 Activo/Ticker","🏷 Categoría"],
                               horizontal=True, key="donut_vista",
                               label_visibility="collapsed")
        if pos_ab_activas:
            PALETTE = ["#C8A84B","#2ECC87","#6BA3BE","#9B8EC4","#E87844","#E85555","#F0C040","#8BA5C8","#FF9F43","#A29BFE"]
            if vista_donut == "📊 Activo/Ticker":
                labels_d = [p["Activo"] for p in pos_ab_activas]
                values_d = [p["Val_Actual"]*factor for p in pos_ab_activas]
                colors_d = [PALETTE[i%len(PALETTE)] for i in range(len(labels_d))]
                titulo_d = "% por activo (posiciones abiertas)"
            else:
                dist_cat = {}
                for p in pos_ab_activas:
                    c = p["Categoria"]
                    dist_cat[c] = dist_cat.get(c,0) + p["Val_Actual"]*factor
                labels_d = list(dist_cat.keys())
                values_d = list(dist_cat.values())
                colors_d = [CAT_CLR_MAP.get(c, "#8BA5C8") for c in labels_d]
                titulo_d = "% por categoría (posiciones abiertas)"

            fig2 = go.Figure(go.Pie(
                labels=labels_d, values=values_d, hole=.55,
                marker=dict(colors=colors_d, line=dict(color="#111827",width=2)),
                textinfo="percent+label",
                textfont=dict(color="#ffffff", size=11),
                hovertemplate="<b>%{label}</b><br>%{value:$,.2f}"+sfx+"<br>%{percent}<extra></extra>",
            ))
            fig2.update_layout(**PT,
                title=dict(text=titulo_d, font=dict(size=11,color="#8BA5C8"),x=.5),
                showlegend=True,
                legend=dict(font=dict(color="#ffffff",size=10),bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        elif posiciones:
            st.info("Todas las posiciones están cerradas.")
        else:
            st.info("Sin posiciones registradas.")

    # Precios en tiempo real
    if prices:
        sec("Precios en tiempo real")
        st.markdown('<div style="font:400 10px IBM Plex Mono,mono;color:#8BA5C8;margin:-8px 0 10px">% = variación del día (no es tu P&L total)</div>', unsafe_allow_html=True)
        cols_p = st.columns(min(len(prices),5))
        for i,(tk,d) in enumerate(list(prices.items())[:10]):
            chg=d.get("chg24",0); px=d.get("price",0)
            clr="#2ECC87" if chg>=0 else "#E85555"
            pxs=f"${px:,.4f}" if px<10 else f"${px:,.2f}"
            # Buscar P&L real de esta posición
            pnl_real = next((p["GP_pct"] for p in posiciones
                             if p["Ticker"].upper()==tk.upper() and p["Estado"]=="Abierta"), None)
            pnl_html = f'<div style="font:400 9px IBM Plex Mono,mono;color:{"#2ECC87" if pnl_real>=0 else "#E85555"}">P&L: {"+" if pnl_real>=0 else ""}{pnl_real:.2f}%</div>' if pnl_real is not None else ""
            with cols_p[i%min(len(prices),5)]:
                st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
                    border-radius:8px;padding:12px;text-align:center;margin-bottom:8px">
                  <div style="font:600 11px/1.5 IBM Plex Mono,mono;color:#C8A84B">{tk}</div>
                  <div style="font:600 15px/1.4 IBM Plex Mono,mono;color:var(--text)">{pxs}</div>
                  <div style="font:400 10px/1.3 IBM Plex Mono,mono;color:{clr}">
                    {'▲' if chg>=0 else '▼'} {abs(chg):.2f}% hoy</div>
                  {pnl_html}</div>""",
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
                <div style="font:500 13px IBM Plex Mono,mono;color:var(--text)">{p['Cantidad']:,.4f}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">PX COMPRA</div>
                <div style="font:500 13px IBM Plex Mono,mono;color:var(--text)">${p['Px_Compra']:,.4f}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">PX ACTUAL</div>
                <div style="font:500 13px IBM Plex Mono,mono;color:var(--text)">{px_str}</div>
                <div style="font:400 9px IBM Plex Mono,mono;color:{chg_clr}">{chg_str} 24h</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">INVERTIDO</div>
                <div style="font:500 13px IBM Plex Mono,mono;color:var(--text)">{money(p['Invertido'],factor)}{sfx}</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">VALOR HOY</div>
                <div style="font:600 14px IBM Plex Mono,mono;color:var(--text)">{money(p['Val_Actual'],factor)}{sfx}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">P&L</div>
                <div style="font:600 15px IBM Plex Mono,mono;color:{gc2}">{sg}{money(p['GP_usd'],factor)}{sfx}</div>
                <div style="font:600 13px IBM Plex Mono,mono;color:{gc2}">{sg}{p['GP_pct']:.2f}%</div>
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
                # Buscador por nombre de activo
                buscar_activo = st.text_input("🔍 Buscar activo",
                    placeholder="Escribe nombre para filtrar…",
                    key="buscar_venta")
                abiertas_filtradas = [p for p in abiertas_lista
                    if buscar_activo.strip().lower() in p["Activo"].lower()]                     if buscar_activo.strip() else abiertas_lista

                if not abiertas_filtradas:
                    st.warning(f"No se encontró '{buscar_activo}' en posiciones abiertas.")
                    abiertas_filtradas = abiertas_lista  # fallback a todas

                lbs = [f"{p['F_Compra']} — {p['Activo']} ({p['Cantidad']:,.4f} uds · ${p['Px_Compra']:,.4f})"
                       for p in abiertas_filtradas]
                sel = st.selectbox("Selecciona la posición a vender", range(len(lbs)),
                                   format_func=lambda i: lbs[i])
                pos_sel = abiertas_filtradas[sel]

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
                        <div style="font:600 16px IBM Plex Mono,mono;color:var(--text)">
                          {money(precio_v*pos_sel['Cantidad'],factor)}{sfx}</div></div>
                    </div>""", unsafe_allow_html=True)

                if st.button("💰 CONFIRMAR VENTA", use_container_width=True):
                    if precio_v <= 0:
                        st.error("❌ Ingresa el precio de venta")
                    else:
                        _id = pos_sel["_id"]
                        datos_venta = {
                            "Estado":       "Cerrada",
                            "Fecha_Venta":  str(fecha_v),
                            "Precio_Venta": float(precio_v),
                        }
                        if _id.startswith("ops_"):
                            # Viene de colección 'operaciones' — guardar como nueva inversión cerrada
                            real_id = _id.replace("ops_","",1)
                            ok2, msg2 = fs_post("inversiones", {
                                "Fondo":         pos_sel.get("Usuario","").split("@")[0] if not fondo else fondo,
                                "Usuario":       pos_sel.get("Usuario", usuario),
                                "Fecha_Compra":  pos_sel["F_Compra"],
                                "Activo":        pos_sel["Activo"],
                                "Categoria":     pos_sel["Categoria"],
                                "Cantidad":      float(pos_sel["Cantidad"]),
                                "Precio_Compra": float(pos_sel["Px_Compra"]),
                                "Broker":        pos_sel.get("Broker",""),
                                "Ticker_API":    pos_sel["Ticker"],
                                "Fecha_Venta":   str(fecha_v),
                                "Precio_Venta":  float(precio_v),
                                "Estado":        "Cerrada",
                                "Notas":         f"Migrado de operaciones/{real_id}",
                            })
                            if ok2:
                                # Actualizar también en operaciones para consistencia
                                fs_patch("operaciones", real_id, {"Resultado": "Ganadora" if precio_v > pos_sel["Px_Compra"] else "Perdedora"})
                                st.success(f"✓ Venta de {pos_sel['Activo']} registrada — guardada en historial")
                                st.cache_data.clear(); time.sleep(0.5); st.rerun()
                            else:
                                st.error(f"❌ Error: {msg2}")
                        else:
                            # Nueva colección inversiones — patch directo
                            ok = fs_patch("inversiones", _id, datos_venta)
                            if ok:
                                st.success(f"✓ Venta de {pos_sel['Activo']} registrada el {fecha_v}")
                                st.cache_data.clear(); time.sleep(0.5); st.rerun()
                            else:
                                st.error("❌ Error actualizando")

            # ── EDITAR POSICIÓN CERRADA ──
            pos_cerradas_todas = [p for p in posiciones if p["Estado"]=="Cerrada"]
            if pos_cerradas_todas:
                st.markdown("---")
                sec("Editar posición cerrada")
                st.markdown('<div style="font:400 11px IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:8px">Corrige fecha o precio de venta de cualquier posición ya cerrada.</div>', unsafe_allow_html=True)
                lbs_c = [f"{p['F_Compra']} → {p['F_Venta']} — {p['Activo']} (vendido a ${p['Px_Actual']:,.4f})"
                         for p in pos_cerradas_todas]
                sel_c = st.selectbox("Selecciona posición cerrada", range(len(lbs_c)),
                                     format_func=lambda i: lbs_c[i], key="sel_cerrada")
                pc_sel = pos_cerradas_todas[sel_c]
                ec1,ec2 = st.columns(2)
                nueva_fv = ec1.date_input("Nueva fecha de venta",
                                          value=pd.to_datetime(pc_sel["F_Venta"]).date()
                                          if pc_sel["F_Venta"] else date.today(),
                                          key="edit_fv")
                nuevo_pv = ec2.number_input("Nuevo precio de venta (USD)",
                                            value=float(pc_sel["Px_Actual"]) if pc_sel["Px_Actual"] else 0.0,
                                            min_value=0.0, step=0.0001, format="%.4f", key="edit_pv")
                if st.button("✏️ ACTUALIZAR POSICIÓN CERRADA"):
                    _id_c = pc_sel["_id"]
                    datos_edit = {"Fecha_Venta": str(nueva_fv), "Precio_Venta": float(nuevo_pv), "Estado": "Cerrada"}
                    if _id_c.startswith("ops_"):
                        # Legacy: crear/actualizar en inversiones
                        ok2, msg2 = fs_post("inversiones", {
                            "Fondo": fondo, "Usuario": usuario,
                            "Fecha_Compra": pc_sel["F_Compra"], "Activo": pc_sel["Activo"],
                            "Categoria": pc_sel["Categoria"], "Cantidad": float(pc_sel["Cantidad"]),
                            "Precio_Compra": float(pc_sel["Px_Compra"]), "Broker": "",
                            "Ticker_API": pc_sel["Ticker"], "Fecha_Venta": str(nueva_fv),
                            "Precio_Venta": float(nuevo_pv), "Estado": "Cerrada",
                            "Notas": f"Editado desde operaciones/{_id_c.replace('ops_','')}",
                        })
                        if ok2: st.success("✓ Posición actualizada"); st.cache_data.clear(); st.rerun()
                        else:   st.error(f"❌ {msg2}")
                    else:
                        ok = fs_patch("inversiones", _id_c, datos_edit)
                        if ok: st.success("✓ Posición actualizada"); st.cache_data.clear(); st.rerun()
                        else:  st.error("❌ Error actualizando")

            # Archivar / Desarchivar posición
            st.markdown("---")
            col_arc, col_dearc = st.columns(2)

            with col_arc:
                sec("Archivar posición")
                st.markdown('''<div style="font:400 11px IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:8px">
                  Saca la posición del fondo. No cuenta en totales.
                  Queda en historial. Nunca se borra.</div>''', unsafe_allow_html=True)
                activas_arc = [p for p in posiciones if p["Estado"] != "Archivada"]
                if activas_arc:
                    lbs_arc = [f"{p['F_Compra']} — {p['Activo']} ({p['Estado']})" for p in activas_arc]
                    arc_sel = st.selectbox("Posición a archivar", range(len(lbs_arc)),
                                           format_func=lambda i: lbs_arc[i], key="arc_pos")
                    if st.button("📦 ARCHIVAR"):
                        _id_a = activas_arc[arc_sel]["_id"]
                        col = "inversiones" if not _id_a.startswith("ops_") else "operaciones"
                        real_id = _id_a.replace("ops_","",1) if _id_a.startswith("ops_") else _id_a
                        fs_patch(col, real_id, {"Estado": "Archivada"})
                        st.success("✓ Archivada"); st.cache_data.clear(); st.rerun()
                else:
                    st.info("No hay posiciones para archivar.")

            with col_dearc:
                sec("Desarchivar posición")
                st.markdown('''<div style="font:400 11px IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:8px">
                  Reactiva una posición archivada. Vuelve a contar
                  en el portafolio con todos sus datos intactos.</div>''', unsafe_allow_html=True)
                archivadas = [p for p in posiciones if p["Estado"] == "Archivada"]
                if archivadas:
                    lbs_da = [f"{p['F_Compra']} — {p['Activo']}" for p in archivadas]
                    da_sel = st.selectbox("Posición a desarchivar", range(len(lbs_da)),
                                          format_func=lambda i: lbs_da[i], key="dearc_pos")
                    # Determinar si tenía fecha de venta para restaurar al estado correcto
                    p_da = archivadas[da_sel]
                    estado_restaurar = "Cerrada" if p_da.get("F_Venta") else "Abierta"
                    st.markdown(f'<div style="font:400 10px IBM Plex Mono,mono;color:#C8A84B;margin-bottom:6px">'
                                f'Se restaurará como: <strong>{estado_restaurar}</strong></div>',
                                unsafe_allow_html=True)
                    if st.button("♻️ DESARCHIVAR"):
                        _id_da = p_da["_id"]
                        col_da = "inversiones" if not _id_da.startswith("ops_") else "operaciones"
                        real_da = _id_da.replace("ops_","",1) if _id_da.startswith("ops_") else _id_da
                        fs_patch(col_da, real_da, {"Estado": estado_restaurar})
                        st.success(f"✓ Restaurada como {estado_restaurar}")
                        st.cache_data.clear(); st.rerun()
                else:
                    st.info("No hay posiciones archivadas.")

# ══════════════════════════════════════════════════════
# CAPITAL — disponible para admin y portafolio individual
# Lógica: compra → capital invertido sube automáticamente
#         depósito → cash disponible (aún no invertido)
#         retiro → baja el valor real del portafolio
# ══════════════════════════════════════════════════════
if rol == "admin" or puede_registrar:
    with t_cap:
        # Resumen de cash actual
        cap1, cap2, cap3 = st.columns(3)
        with cap1:
            st.markdown(card("Depósitos acumulados",
                money(cash_aportes, factor)+sfx, color="#2ECC87"), unsafe_allow_html=True)
        with cap2:
            st.markdown(card("Retiros acumulados",
                money(cash_retiros, factor)+sfx, color="#E85555"), unsafe_allow_html=True)
        with cap3:
            cn_color = "#2ECC87" if cash_neto >= 0 else "#E85555"
            st.markdown(card("Cash neto disponible",
                money(cash_neto, factor)+sfx,
                "Depósitos - Retiros", color=cn_color), unsafe_allow_html=True)

        st.markdown("""<div style="background:#162236;border:1px solid #1E3354;
            border-left:3px solid #C8A84B;border-radius:0 8px 8px 0;
            padding:10px 14px;margin:14px 0;font:400 11px/1.7 IBM Plex Mono,mono;color:#B0C4DC">
          <strong>Depósito:</strong> ingresaste dinero a la cuenta (aún no invertido en activos).<br>
          <strong>Retiro:</strong> sacaste dinero de la cuenta → el portafolio baja en ese monto.<br>
          Las compras de activos ya quedan registradas automáticamente al registrar una inversión.
        </div>""", unsafe_allow_html=True)

        sec("Registrar movimiento de dinero")
        with st.form("form_cap", clear_on_submit=True):
            cc1,cc2,cc3 = st.columns(3)
            tipo_mov = cc1.selectbox("Tipo de movimiento",
                ["Depósito","Retiro"],
                help="Deposito: ingresaste dinero. Retiro: sacaste dinero de la cuenta.")
            monto_cap = cc2.number_input("Monto (USD)", min_value=0.01, step=0.01, format="%.2f")
            fecha_cap = cc3.date_input("Fecha", value=date.today())

            cc4, cc5 = st.columns(2)
            concepto  = cc4.text_input("Concepto / descripción",
                placeholder="Ej: Transferencia inicial, retiro mensual…")
            broker_cap= cc5.text_input("Broker / Banco", placeholder="Schwab, Nubank, Bancolombia…")

            # Si es admin, puede registrar para un socio específico
            if rol == "admin":
                cc6,cc7 = st.columns(2)
                socio_cap = cc6.text_input("Nombre del socio", placeholder="Nombre o razón social")
                cedula_cap= cc7.text_input("Cédula / ID")
            else:
                socio_cap  = usuario.split("@")[0]
                cedula_cap = ""

            if st.form_submit_button("💾 REGISTRAR MOVIMIENTO", use_container_width=True):
                if monto_cap <= 0:
                    st.error("❌ El monto debe ser mayor a 0")
                else:
                    # Normalizamos: Depósito → Aporte, Retiro → Retiro
                    tipo_fs = "Aporte" if tipo_mov == "Depósito" else "Retiro"
                    ok, msg = fs_post("aportes", {
                        "Fondo":    fondo,
                        "Socio":    socio_cap,
                        "Cedula":   cedula_cap,
                        "Fecha":    str(fecha_cap),
                        "Tipo":     tipo_fs,
                        "Monto":    float(monto_cap),
                        "Concepto": concepto.strip(),
                        "Broker":   broker_cap.strip(),
                        "Usuario":  usuario,
                    })
                    if ok:
                        signo = "+" if tipo_fs=="Aporte" else "-"
                        st.success(f"✓ {tipo_mov} de {signo}{money(monto_cap,factor)}{sfx} registrado")
                        st.cache_data.clear(); st.rerun()
                    else:
                        st.error(f"❌ Error Firestore: {msg}")

        # Historial de movimientos
        if not df_ap.empty:
            st.markdown("---")
            sec("Historial de movimientos de capital")
            # Filtrar por usuario si no es admin
            dfh = df_ap.copy()
            if rol != "admin" and "Usuario" in dfh.columns:
                dfh = dfh[dfh["Usuario"] == usuario]
            cols_h = [c for c in ["Fecha","Socio","Tipo","Monto","Concepto","Broker"] if c in dfh.columns]
            dfh = dfh[cols_h].sort_values("Fecha", ascending=False).copy()
            if "Monto" in dfh.columns:
                dfh["Monto"] = dfh["Monto"] * factor

            def ct(v):
                if v=="Aporte":  return "color:#2ECC87;font-weight:600"
                if v=="Retiro":  return "color:#E85555;font-weight:600"
                return ""
            styled_h = dfh.style.format({"Monto":"${:,.2f}"})
            if "Tipo" in dfh.columns:
                styled_h = styled_h.map(ct, subset=["Tipo"])
            st.dataframe(styled_h, use_container_width=True, hide_index=True)

            # Resumen por tipo
            if "Tipo" in dfh.columns and len(dfh) > 0:
                total_dep = df_ap[df_ap["Tipo"]=="Aporte"]["Monto"].sum() * factor
                total_ret = df_ap[df_ap["Tipo"]=="Retiro"]["Monto"].sum() * factor
                st.markdown(f"""<div style="display:flex;gap:20px;margin-top:10px;flex-wrap:wrap">
                  <div style="font:400 10px IBM Plex Mono,mono;color:#2ECC87">
                    ▲ Total depósitos: <strong>{money(total_dep)}{sfx}</strong></div>
                  <div style="font:400 10px IBM Plex Mono,mono;color:#E85555">
                    ▼ Total retiros: <strong>{money(total_ret)}{sfx}</strong></div>
                  <div style="font:400 10px IBM Plex Mono,mono;color:#8BA5C8">
                    = Cash neto: <strong style="color:{"#2ECC87" if total_dep-total_ret>=0 else "#E85555"}">
                    {money(total_dep-total_ret)}{sfx}</strong></div>
                </div>""", unsafe_allow_html=True)

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

        sec("Resumen de actividad (sin datos privados)")
        st.markdown('''<div style="font:400 11px IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:10px">
          Por privacidad, los datos detallados de portafolios individuales no son visibles
          desde el panel de administración. Solo el cliente puede ver sus propias inversiones.
        </div>''', unsafe_allow_html=True)
        if not df_inv_all.empty:
            # Solo mostrar resumen agregado por fondo, sin detalles individuales
            resumen_act = []
            for f_r in fondos_list:
                inv_f = df_inv_all[df_inv_all["Fondo"] == f_r] if "Fondo" in df_inv_all.columns else pd.DataFrame()
                # Solo incluir fondos grupales (no personal_*)
                if f_r.startswith("personal_"):
                    resumen_act.append({"Fondo": f_r, "Tipo": "Personal (privado)",
                                        "# Posiciones": "🔒 Privado", "Estado": "—"})
                else:
                    n_ab  = len(inv_f[inv_f["Estado"]=="Abierta"])  if not inv_f.empty and "Estado" in inv_f.columns else 0
                    n_cer = len(inv_f[inv_f["Estado"]=="Cerrada"]) if not inv_f.empty and "Estado" in inv_f.columns else 0
                    resumen_act.append({"Fondo": f_r, "Tipo": "Grupal",
                                        "# Abiertas": n_ab, "# Cerradas": n_cer})
            st.dataframe(pd.DataFrame(resumen_act), use_container_width=True, hide_index=True)
