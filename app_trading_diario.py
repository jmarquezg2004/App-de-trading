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
        "aportaciones": pd.DataFrame(),  # aportes / retiros
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
        socio = c1.text_input("Nombre Socio")
        cedula = c2.text_input("Cédula / ID")
        tipo = c3.selectbox("Tipo", ["Aporte", "Retiro"])
        monto = c4.number_input("Monto (USD)", step=0.01)
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

    POS_COLS = ["Fondo", "Fecha", "Moneda", "Estrategia", "Broker", "Valor_Posicion", "TP_pct", "SL_pct", "TP_usd", "SL_usd", "Resultado"]
    if st.session_state.records.empty:
        st.session_state.records = pd.DataFrame(columns=POS_COLS)

    with st.form("registro_op"):
        c1, c2, c3 = st.columns(3)
        fecha_op = c1.date_input("Fecha", datetime.today())
        moneda = c2.text_input("Moneda / Activo", "Bitcoin")
        estrategia = c3.selectbox("Estrategia", ["spot", "futuros", "staking", "holding", "ICO", "pool_liquidez", "farming"])
        c4, c5 = st.columns(2)
        broker = c4.text_input("Broker / Exchange")
        valor_pos = c5.number_input("Valor Posición (USD)", min_value=0.0, step=0.01)
        c6, c7, c8 = st.columns(3)
        tp_pct = c6.number_input("TP %", min_value=0.0, step=0.1)
        sl_pct = c7.number_input("SL %", min_value=0.0, step=0.1)
        resultado = c8.selectbox("Resultado", ["Abierta", "Ganadora", "Perdedora"])

        tp_usd_calc = valor_pos * tp_pct / 100
        sl_usd_calc = valor_pos * sl_pct / 100
        st.markdown(f"**TP USD estimado:** `${tp_usd_calc:,.2f}` &nbsp;|&nbsp; **SL USD estimado:** `${sl_usd_calc:,.2f}`")

        if st.form_submit_button("Guardar Operación"):
            op = {"Fondo": nombre_fondo, "Fecha": pd.to_datetime(fecha_op), "Moneda": moneda, "Estrategia": estrategia, "Broker": broker, "Valor_Posicion": valor_pos, "TP_pct": tp_pct, "SL_pct": sl_pct, "TP_usd": tp_usd_calc, "SL_usd": sl_usd_calc, "Resultado": resultado}
            st.session_state.records = pd.concat([st.session_state.records, pd.DataFrame([op])], ignore_index=True)
            st.success("Operación guardada ✔️")
            st.rerun()

    st.markdown("---")

# --------------------------- FILTROS ------------------------------ #
st.subheader("🔍 Filtros de Operaciones")
ops_fondo = st.session_state.records[st.session_state.records["Fondo"] == nombre_fondo]
if ops_fondo.empty:
    st.info("No hay operaciones registradas para este fondo.")
else:
    colf1, colf2, colf3 = st.columns(3)
    fecha_desde = colf1.date_input("Desde", ops_fondo["Fecha"].min().date())
    fecha_hasta = colf1.date_input("Hasta", ops_fondo["Fecha"].max().date())
    brokers_filt = colf2.multiselect("Broker", sorted(ops_fondo["Broker"].unique()), default=list(ops_fondo["Broker"].unique()))
    estr_filt = colf3.multiselect("Estrategia", sorted(ops_fondo["Estrategia"].unique()), default=list(ops_fondo["Estrategia"].unique()))

    mask = (
        (ops_fondo["Fecha"] >= pd.to_datetime(fecha_desde)) &
        (ops_fondo["Fecha"] <= pd.to_datetime(fecha_hasta)) &
        (ops_fondo["Broker"].isin(brokers_filt)) &
        (ops_fondo["Estrategia"].isin(estr_filt))
    )
    filtered = ops_fondo[mask].copy()

    st.subheader("📄 Operaciones Filtradas")
    st.dataframe(filtered, use_container_width=True)

    # ------------------ RESUMEN DEL FONDO ------------------------- #
    st.markdown("---")
    st.subheader("📊 Resumen del Fondo")

    # Capital neto aportado
    ap = st


