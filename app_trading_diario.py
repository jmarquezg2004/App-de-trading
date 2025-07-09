import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ------------------ CONFIG BASICS ------------------ #
st.set_page_config(page_title="Diario de Trading", layout="wide")

# ------------------ USER DEMO ------------------ #
USUARIOS = {
    "admin": {"pwd": "admin123", "fondo": "Arkez Invest", "rol": "admin"},
    "juan": {"pwd": "juan123", "fondo": "Cripto Alpha", "rol": "lector"},
    "maria": {"pwd": "maria123", "fondo": "Arkez Invest", "rol": "lector"},
}

# ------------------ INIT SESSION ------------------ #

def init_state():
    defaults = {
        "logged_in": False,
        "usuario": None,
        "rol": None,
        "fondo": "Arkez Invest",
        "fondos": ["Arkez Invest", "Cripto Alpha"],
        "aportaciones": pd.DataFrame(columns=["Fondo", "Socio", "Cedula", "Fecha", "Tipo", "Monto"]),
        "ops": pd.DataFrame(columns=["ID", "Fondo", "Fecha", "Moneda", "Estrategia", "Broker", "Valor_Pos", "TP_%", "SL_%", "TP_usd", "SL_usd", "Resultado"]),
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

init_state()

# ------------------ LOGIN ------------------ #

def login_ui():
    st.sidebar.title("🔒 Acceso Privado")
    u = st.sidebar.text_input("Usuario")
    p = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Entrar"):
        if u in USUARIOS and USUARIOS[u]["pwd"] == p:
            st.session_state.update({
                "logged_in": True,
                "usuario": u,
                "rol": USUARIOS[u]["rol"],
                "fondo": USUARIOS[u]["fondo"],
            })
            st.rerun()
        else:
            st.sidebar.error("Credenciales incorrectas ❌")
            st.stop()
    else:
        st.stop()

if not st.session_state.logged_in:
    login_ui()

usuario = st.session_state.usuario
rol = st.session_state.rol
fondo = st.session_state.fondo

# ------------------ ADMIN FONDOS ------------------ #
if rol == "admin":
    st.sidebar.subheader("🏦 Fondos")
    sel = st.sidebar.selectbox("Selecciona Fondo", st.session_state.fondos, index=st.session_state.fondos.index(fondo))
    if sel != fondo:
        st.session_state.fondo = sel
        st.rerun()
    nuevo = st.sidebar.text_input("Crear nuevo fondo")
    if st.sidebar.button("Agregar Fondo") and nuevo.strip():
        if nuevo not in st.session_state.fondos:
            st.session_state.fondos.append(nuevo)
            st.session_state.fondo = nuevo
            st.rerun()
        else:
            st.sidebar.warning("Ese fondo ya existe")

# ------------------ HEADER ------------------ #
st.title("📈 Diario & Gestor de Fondos de Inversión")
st.markdown(f"**👤 {usuario}** — **Fondo:** {fondo}")
st.markdown("---")

# ==================== APORTES / RETIROS ==================== #
if rol == "admin":
    st.subheader("💰 Movimientos de Capital (Socios)")
    with st.form("mov_cap"):
        c1, c2, c3, c4 = st.columns(4)
        socio = c1.text_input("Socio")
        ced = c2.text_input("Cédula/ID")
        tipo = c3.selectbox("Tipo", ["Aporte", "Retiro"])
        monto = c4.number_input("Monto USD", step=0.01)
        fecha = st.date_input("Fecha", datetime.today())
        if st.form_submit_button("Guardar"):
            row = {"Fondo": fondo, "Socio": socio, "Cedula": ced, "Fecha": fecha, "Tipo": tipo, "Monto": monto}
            st.session_state.aportaciones = pd.concat([st.session_state.aportaciones, pd.DataFrame([row])], ignore_index=True)
            st.success("Movimiento registrado")
            st.rerun()
    st.dataframe(
        st.session_state.aportaciones.query("Fondo==@fondo").sort_values("Fecha", ascending=False),
        use_container_width=True,
    )
    st.markdown("---")

# ==================== REGISTRO OPERACIONES =================== #
if rol == "admin":
    st.subheader("➕ Registrar Nueva Operación")
    with st.form("nueva_op"):
        c1, c2, c3 = st.columns(3)
        f_op = c1.date_input("Fecha", datetime.today())
        moneda = c2.text_input("Moneda", "Bitcoin")
        est = c3.selectbox("Estrategia", ["spot", "futuros", "staking", "holding", "ICO", "pool_liquidez", "farming"])
        c4, c5 = st.columns(2)
        broker = c4.text_input("Broker")
        val = c5.number_input("Valor Posición USD", min_value=0.0, step=0.01)
        c6, c7, c8 = st.columns(3)
        tp_pct = c6.number_input("TP %", min_value=0.0, step=0.1)
        sl_pct = c7.number_input("SL %", min_value=0.0, step=0.1)
        res = c8.selectbox("Resultado", ["Abierta", "Ganadora", "Perdedora"])
        tp_usd = val * tp_pct / 100
        sl_usd = val * sl_pct / 100
        st.markdown(f"TP ≈ **${tp_usd:,.2f}** | SL ≈ **${sl_usd:,.2f}**")
        if st.form_submit_button("Guardar Operación"):
            op_id = len(st.session_state.ops) + 1
            row = {
                "ID": op_id,
                "Fondo": fondo,
                "Fecha": pd.to_datetime(f_op),
                "Moneda": moneda,
                "Estrategia": est,
                "Broker": broker,
                "Valor_Pos": val,
                "TP_%": tp_pct,
                "SL_%": sl_pct,
                "TP_usd": tp_usd,
                "SL_usd": sl_usd,
                "Resultado": res,
            }
            st.session_state.ops = pd.concat([st.session_state.ops, pd.DataFrame([row])], ignore_index=True)
            st.success("Operación guardada")
            st.rerun()
    st.markdown("---")

# ----------- Actualizar operaciones abiertas ------------ #
if rol == "admin":
    abiertas = st.session_state.ops.query("Fondo==@fondo and Resultado=='Abierta'")
    if not abiertas.empty:
        st.subheader("✏️ Cerrar Operación Abierta")
        sel_id = st.selectbox("ID de operación", abiertas["ID"].tolist())
        nuevo_res = st.radio("Marcar como", ["Ganadora", "Perdedora"], horizontal=True)
        if st.button("Actualizar Resultado"):
            idx = st.session_state.ops.index[st.session_state.ops["ID"] == sel_id][0]
            st.session_state.ops.at[idx, "Resultado"] = nuevo_res
            st.success("Operación actualizada")
            st.rerun()
    st.markdown("---")

# ==================== FILTROS & TABLA ======================= #
st.subheader("🔍 Operaciones")
ops_fondo = st.session_state.ops.query("Fondo==@fondo")
if ops_fondo.empty:
    st.info("Sin operaciones para este fondo")
else:
    c1, c2, c3 = st.columns(3)
    desde = c1.date_input("Desde", ops_fondo["Fecha"].min().date())
    hasta = c1.date_input("Hasta", ops_fondo["Fecha"].max().date())
    bro_sel = c2.multiselect("Broker", sorted(ops_fondo["Broker"].unique()), default=list(ops_fondo["Broker"].unique()))
    est_sel = c3.multiselect("Estrategia", sorted(ops_fondo["Estrategia"].unique()), default=list(ops_fondo["Estrategia"].unique()))

    mask = (
        (ops_fondo["Fecha"] >= pd.to_datetime(desde))
        & (ops_fondo["Fecha"] <= pd.to_datetime(hasta))
        & (ops_fondo["Broker"].isin(bro_sel))
        & (ops_fondo["Estrategia"].

