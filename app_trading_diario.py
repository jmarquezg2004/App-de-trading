import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from pathlib import Path

# =============================================================
# CONFIGURACIÓN GLOBAL DE ESTILOS
# =============================================================
st.set_page_config(page_title="Diario de Trading", layout="wide")

PRIMARY_BLUE = "#0F2E46"        # azul corporativo Arkez
PRIMARY_BLUE_L = "#27425C"      # 50 % más claro
YELLOW        = "#C5A15C"       # amarillo/dorado del logo
BG_GRADIENT   = "linear-gradient(135deg,#e9edf3 0%,#d5dde7 100%)"  # gris‑azul claro

st.markdown(
    f"""
    <style>
        html, body, [class*='st-'] {{ background: {BG_GRADIENT}!important; }}
        h1 {{ background:{PRIMARY_BLUE_L}; color:{YELLOW}; padding:12px 18px; border-radius:8px; }}
        h2, h3 {{ background:{PRIMARY_BLUE_L}; color:{YELLOW}; padding:6px 12px; border-radius:6px; margin-top:1.3rem; }}
        div[data-testid='metric-container'] {{ background:white; border:1px solid #ccd; padding:8px; border-radius:8px; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================================================
# DATOS DE USUARIOS DEMO
# =============================================================
USUARIOS = {
    "admin": {"pwd": "admin123", "fondo": "Arkez Invest", "rol": "admin"},
    "juan" : {"pwd": "juan123",  "fondo": "Cripto Alpha", "rol": "lector"},
}
DEFAULT_FONDOS = ["Arkez Invest", "Cripto Alpha"]

# =============================================================
# INICIALIZAR SESSION_STATE
# =============================================================
if "init" not in st.session_state:
    st.session_state.init         = True
    st.session_state.logged_in    = False
    st.session_state.usuario      = None
    st.session_state.rol          = None
    st.session_state.fondos       = DEFAULT_FONDOS.copy()
    st.session_state.fondo        = DEFAULT_FONDOS[0]
    st.session_state.aportaciones = pd.DataFrame(columns=["Fondo", "Socio", "Cedula", "Fecha", "Tipo", "Monto"])
    st.session_state.ops          = pd.DataFrame(columns=[
        "ID", "Fondo", "Fecha", "Moneda", "Estrategia", "Broker", "Valor_Pos", "TP_%", "SL_%", "Comisiones", "TP_usd", "SL_usd", "Resultado"
    ])

# =============================================================
# FUNCIÓN DE LOGIN
# =============================================================

def login_ui():
    st.sidebar.title("🔒 Acceso Privado")
    u = st.sidebar.text_input("Usuario")
    p = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Entrar"):
        if u in USUARIOS and USUARIOS[u]["pwd"] == p:
            st.session_state.logged_in = True
            st.session_state.usuario   = u
            st.session_state.rol       = USUARIOS[u]["rol"]
            st.session_state.fondo     = USUARIOS[u]["fondo"]
            st.rerun()
        else:
            st.sidebar.error("Credenciales incorrectas ❌")

if not st.session_state.logged_in:
    login_ui()
    st.stop()

# =============================================================
# VARIABLES DE SESIÓN
# =============================================================
usuario = st.session_state.usuario
rol     = st.session_state.rol
fondo   = st.session_state.fondo

# =============================================================
# SIDEBAR: LOGO Y FONDOS
# =============================================================
logo_path = Path("arkez_logo.png")
if logo_path.exists():
    st.sidebar.image(str(logo_path), width=160)
else:
    st.sidebar.write("[Sube arkez_logo.png]")

if rol == "admin":
    st.sidebar.subheader("🏦 Fondos")
    sel = st.sidebar.selectbox("Fondo", st.session_state.fondos, index=st.session_state.fondos.index(fondo))
    if sel != fondo:
        st.session_state.fondo = sel
        st.rerun()
    nuevo = st.sidebar.text_input("Nuevo fondo")
    if st.sidebar.button("Agregar") and nuevo.strip():
        if nuevo not in st.session_state.fondos:
            st.session_state.fondos.append(nuevo)
            st.session_state.fondo = nuevo
            st.rerun()
        else:
            st.sidebar.warning("Ese fondo ya existe")

# =============================================================
# ENCABEZADO PRINCIPAL
# =============================================================
st.title("📈 Diario & Gestor de Fondos de Inversión")
st.markdown(f"**👤 {usuario}** — **Fondo:** {fondo}")

# =============================================================
# SECCIÓN: APORTES / RETIROS
# =============================================================
if rol == "admin":
    st.header("Movimientos de Capital (Socios)")
    with st.form("form_aporte"):
        c1, c2, c3, c4 = st.columns(4)
        socio   = c1.text_input("Socio")
        cedula  = c2.text_input("Cédula/ID")
        tipo    = c3.selectbox("Tipo", ["Aporte", "Retiro"])
        monto   = c4.number_input("Monto USD", min_value=0.0, step=0.01)
        fecha   = st.date_input("Fecha", datetime.today())
        if st.form_submit_button("Guardar"):
            nuevo = {"Fondo": fondo, "Socio": socio, "Cedula": cedula, "Fecha": fecha, "Tipo": tipo, "Monto": monto}
            st.session_state.aportaciones = pd.concat([st.session_state.aportaciones, pd.DataFrame([nuevo])], ignore_index=True)
            st.success("Movimiento registrado ✔️")
            st.rerun()
    st.dataframe(st.session_state.aportaciones.query("Fondo==@fondo"), use_container_width=True)

# =============================================================
# SECCIÓN: REGISTRAR OPERACIÓN
# =============================================================
if rol == "admin":
    st.header("Registrar Nueva Operación")
    with st.form("form_op"):
        c1, c2, c3 = st.columns(3)
        fecha_op   = c1.date_input("Fecha", datetime.today())
        moneda     = c2.text_input("Moneda", "BTC")
        estrategia = c3.selectbox("Estrategia", ["spot", "futuros", "staking", "holding", "ICO", "pool_liquidez", "farming"])
        c4, c5 = st.columns(2)
        broker     = c4.text_input("Broker")
        valor_pos  = c5.number_input("Valor Posición USD", min_value=0.0, step=0.01)
        c6, c7, c8, c9 = st.columns(4)
        tp_pct     = c6.number_input("TP %", min_value=0.0, step=0.1)
        sl_pct     = c7.number_input("SL %", min_value=0.0, step=0.1)
        comisiones = c8.number_input("Comisiones USD", min_value=0.0, step=0.01)
        resultado  = c9.selectbox("Resultado", ["Abierta", "Ganadora", "Perdedora"])

        tp_usd = valor_pos * tp_pct / 100 - comisiones
        sl_usd = valor_pos * sl_pct / 100 + comisiones
        st.markdown(f"TP neto ≈ **${tp_usd:,.2f}**   |   SL neto ≈ **${sl_usd:,.2f}**")

        if st.form_submit_button("Guardar Operación"):
            oid = len(st.session_state.ops) + 1
            nueva_op = {
                "ID": oid, "Fondo": fondo, "Fecha": pd.to_datetime(fecha_op), "Moneda": moneda, "Estrategia": estrategia,
                "Broker": broker, "Valor_Pos": valor_pos, "TP_%": tp_pct, "SL_%": sl_pct, "Comisiones": comisiones,
                "TP_usd": tp_usd, "SL_usd": sl_usd, "Resultado": resultado
            }
            st.session_state.ops = pd.concat([st.session_state.ops, pd.DataFrame([nueva_op])], ignore_index=True)
            st.success("Operación guardada ✔️")
            st.rerun()

# =============================================================
# FILTRO Y TABLA DE OPERACIONES
# =============================================================
st.header("Operaciones")
ops_all = st.session_state.ops.query("Fondo==@fondo")
if ops_all.empty:
    st.info("Sin operaciones registradas")
    st.stop()

c1, c2, c3 = st.columns(3)
from_d = c1.date_input("Desde", ops_all["Fecha"].min().date())

