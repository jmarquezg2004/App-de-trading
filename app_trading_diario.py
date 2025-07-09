import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64

# ---------------------- CONFIGURACIÓN BÁSICA ---------------------- #
st.set_page_config(page_title="Diario de Trading", layout="wide")

# ---------------------- USUARIOS Y FONDOS ------------------------- #
USUARIOS = {
    "admin": {"pwd": "admin123", "fondo": "Arkez Invest", "rol": "admin"},
    "juan": {"pwd": "juan123", "fondo": "Cripto Alpha", "rol": "lector"},
    "maria": {"pwd": "maria123", "fondo": "Arkez Invest", "rol": "lector"},
}

# ------------------------- ESTADO DE SESIÓN ----------------------- #
def init_state():
    defaults = {
        "logged_in": False,
        "usuario_actual": None,
        "rol": None,
        "fondo_actual": "",
        "records": pd.DataFrame(),      # operaciones
        "aportaciones": pd.DataFrame(),  # movimientos de capital (aportes / retiros)
        "fondos": ["Arkez Invest", "Cripto Alpha"],
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

init_state()

# ------------------------- AUTENTICACIÓN ------------------------- #

def login_page():
    st.sidebar.title("🔒 Acceso Privado")
    user = st.sidebar.text_input("Usuario")
    pwd = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Entrar"):
        if user in USUARIOS and USUARIOS[user]["pwd"] == pwd:
            st.session_state.update({
                "logged_in": True,
                "usuario_actual": user,
                "rol": USUARIOS[user]["rol"],
                "fondo_actual": USUARIOS[user]["fondo"],
            })
            st.rerun()
        else:
            st.sidebar.error("Credenciales incorrectas ❌")
            st.stop()
    else:
        st.stop()

if not st.session_state.logged_in:
    login_page()

usuario = st.session_state.usuario_actual
rol = st.session_state.rol
nombre_fondo = st.session_state.fondo_actual

# -------------------- ADMIN: GESTIÓN DE FONDOS -------------------- #
if rol == "admin":
    st.sidebar.subheader("🏦 Fondos")
    fondo_sel = st.sidebar.selectbox("Selecciona Fondo", st.session_state.fondos, index=st.session_state.fondos.index(nombre_fondo))
    st.session_state.fondo_actual = fondo_sel
    nombre_fondo = fondo_sel

    nuevo_fondo = st.sidebar.text_input("Crear nuevo fondo")
    if st.sidebar.button("Agregar Fondo") and nuevo_fondo.strip():
        if nuevo_fondo not in st.session_state.fondos:
            st.session_state.fondos.append(nuevo_fondo)
            st.session_state.fondo_actual = nuevo_fondo
            st.rerun()
        else:
            st.sidebar.warning("Ese fondo ya existe")

# -------------------- ENCABEZADO & DATOS DEL FONDO --------------- #
st.title("📈 Diario & Gestor de Fondos de Inversión")
st.markdown(f"**👤 Usuario:** `{usuario}` &nbsp;—&nbsp; **Fondo actual:** **{nombre_fondo}**")

st.markdown("---")

# ------------------ ADMIN: APORTES / RETIROS SOCIOS -------------- #
if rol == "admin":
    st.subheader("💰 Movimientos de Capital (Socios)")
    AP_COLS = ["Fondo", "Socio", "Cedula", "Fecha", "Tipo", "Monto"]
    if st.session_state.aportaciones.empty:
        st.session_state.aportaciones = pd.DataFrame(columns=AP_COLS)

    with st.form("aportes_form"):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            socio = st.text_input("Nombre Socio")
        with c2:
            cedula = st.text_input("Cédula / ID")
        with c3:
            tipo = st.selectbox("Tipo", ["Aporte", "Retiro"])
        with c4:
            monto = st.number_input("Monto (USD)", step=0.01)
        fecha_apo = st.date_input("Fecha", datetime.today())
        if st.form_submit_button("Guardar Movimiento"):
            mov = {"Fondo": nombre_fondo, "Socio": socio, "Cedula": cedula, "Fecha": fecha_apo, "Tipo": tipo, "Monto": monto}
            st.session_state.aportaciones = pd.concat([st.session_state.aportaciones, pd.DataFrame([mov])], ignore_index=True)
            st.success("Movimiento guardado ✔️")
            st.rerun()

    mov_fondo = st.session_state.aportaciones[st.session_state.aportaciones["Fondo"] == nombre_fondo]
    st.dataframe(mov_fondo.sort_values("Fecha", ascending=False), use_container_width=True)
    st.markdown("---")

# ---------------------- FORMULARIO DE OPERACIÓN ------------------- #
if rol == "admin":
    st.subheader("➕ Registrar Nueva Operación")

    POS_COLS = [
        "Fondo", "Fecha", "Moneda", "Estrategia", "Broker", "Valor_Posicion", "TP_pct", "SL_pct", "TP_usd", "SL_usd", "Resultado"
    ]
    if st.session_state.records.empty:
        st.session_state.records = pd.DataFrame(columns=POS_COLS)

    with st.form("registro_op"):
        c1, c2, c3 = st.columns(3)
        with c1:
            fecha_op = st.date_input("Fecha", datetime.today(), key="op_fecha")
        with c2:
            moneda = st.text_input("Moneda / Activo", "Bitcoin", key="op_moneda")
        with c3:
            estrategia = st.selectbox("Estrategia", ["spot", "futuros", "staking", "holding", "ICO", "pool_liquidez", "farming"], key="op_est")
        c4, c5 = st.columns(2)
        with c4:
            broker = st.text_input("Broker / Exchange", key="op_broker")
        with c5:
            valor_pos = st.number_input("Valor Posición (USD)", min_value=0.0, step=0.01, key="op_valor")
        c6, c7, c8 = st.columns(3)
        with c6:
            tp_pct = st.number_input("TP %", min_value=0.0, step=0.1, key="op_tp_pct")
        with c7:
            sl_pct = st.number_input("SL %", min_value=0.0, step=0.1, key="op_sl_pct")
        with c8:
            resultado = st.selectbox("Resultado", ["Abierta", "Ganadora", "Perdedora"], key="op_res")

        # Calculados
        tp_usd_calc = valor_pos * tp_pct / 100
        sl_usd_calc = valor_pos * sl_pct / 100
        st.markdown(f"**TP USD estimado:** `${tp_usd_calc:,.2f}` &nbsp;&nbsp;|&nbsp;&nbsp; **SL USD estimado:** `${sl_usd_calc:,.2f}`")

        if st.form_submit_button("Guardar Operación"):
            op = {
                "Fondo": nombre_fondo,
                "Fecha": pd.to_datetime(fecha_op),
                "Moneda": moneda,
                "Estrategia": estrategia,
                "Broker": broker,
                "Valor_Posicion": valor_pos,
                "TP_pct": tp_pct,
                "SL_pct": sl_pct,
                "TP_usd": tp_usd_calc,
                "SL_usd": sl_usd_calc,
                "Resultado": resultado,
            }
            st.session_state.records = pd.concat([st.session_state.records, pd.DataFrame([op])], ignore_index=True)
            st.success("Operación guardada ✔️")
            st.rerun()
    st.markdown("---")

# --------------------------- FILTROS ------------------------------ #
st.subheader("🔍 Filtros de Operaciones")
ops_fondo = st.session_state.records[st.session_state.records["Fondo"] == nombre_fondo]
if ops_fondo.empty:
    st.info("No hay operaciones registradas para este fondo.")
    st.stop()

colf1, colf2, colf3 = st.columns(3)
with colf1:
    fecha_desde = st.date_input("Desde", ops_fondo["Fecha"].min().date(), key="flt_desde")
    fecha_hasta = st.date_input("Hasta", ops_fondo["Fecha"].max().date(), key="flt_hasta")
with colf2:
    brokers_filt = st.multiselect("Broker", sorted(ops_fondo["Broker"].unique()), default=list(ops_fondo["Broker"].unique()), key="flt_broker")
with colf3:
    estr_filt = st.multiselect("Estrategia", sorted(ops_fondo["Estrategia"].unique()), default=list(ops_fondo["Estrategia"].unique()), key="flt_est")

mask = (
    (ops_fondo["Fecha"] >= pd.to_datetime(fecha_desde)) &
    (ops_fondo["Fecha"] <= pd.to_datetime(fecha_hasta)) &
    (ops_fondo["Broker"].isin(brokers_filt)) &
    (ops_fondo["Estrategia"].isin(estr_filt))
)
filtered = ops_fondo[mask].copy()

# ------------------------- TABLA DETALLADA ------------------------- #
st.subheader("📄 Operaciones Filtradas")
st.dataframe(filtered, use

