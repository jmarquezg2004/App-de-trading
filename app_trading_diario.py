import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Diario de Trading", layout="wide")

# ------------------ USUARIOS DEMO ------------------ #
USUARIOS = {
    "admin": {"pwd": "admin123", "fondo": "Arkez Invest", "rol": "admin"},
    "juan":  {"pwd": "juan123",  "fondo": "Cripto Alpha", "rol": "lector"},
    "maria": {"pwd": "maria123", "fondo": "Arkez Invest", "rol": "lector"},
}
DEFAULT_FONDOS = ["Arkez Invest", "Cripto Alpha"]

# ------------------ INIT STATE --------------------- #
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.logged_in = False
    st.session_state.usuario   = None
    st.session_state.rol       = None
    st.session_state.fondos    = DEFAULT_FONDOS.copy()
    st.session_state.fondo     = DEFAULT_FONDOS[0]
    st.session_state.aportaciones = pd.DataFrame(columns=["Fondo","Socio","Cedula","Fecha","Tipo","Monto"])
    st.session_state.ops = pd.DataFrame(columns=[
        "ID","Fondo","Fecha","Moneda","Estrategia","Broker","Valor_Pos","TP_%","SL_%","Comisiones","TP_usd","SL_usd","Resultado"
    ])

# ------------------ LOGIN UI ----------------------- #

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

usuario = st.session_state.usuario
rol     = st.session_state.rol
fondo   = st.session_state.fondo

# ------------------ ADMIN FONDOS ------------------- #
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

# ------------------ HEADER ------------------------- #
st.title("📈 Diario & Gestor de Fondos de Inversión")
st.markdown(f"**👤 {usuario}** — **Fondo:** {fondo}")
st.markdown("---")

# ------------------ APORTES / RETIROS -------------- #
if rol == "admin":
    st.subheader("💰 Movimientos de Capital (Socios)")
    with st.form("mov_cap"):
        c1, c2, c3, c4 = st.columns(4)
        socio     = c1.text_input("Socio")
        ced       = c2.text_input("Cédula/ID")
        tipo      = c3.selectbox("Tipo", ["Aporte", "Retiro"])
        monto     = c4.number_input("Monto USD", min_value=0.0, step=0.01)
        fecha_mov = st.date_input("Fecha", datetime.today())
        if st.form_submit_button("Guardar"):
            row = {"Fondo": fondo, "Socio": socio, "Cedula": ced, "Fecha": fecha_mov, "Tipo": tipo, "Monto": monto}
            st.session_state.aportaciones = pd.concat([
                st.session_state.aportaciones, pd.DataFrame([row])
            ], ignore_index=True)
            st.success("Movimiento registrado")
            st.rerun()
    st.dataframe(
        st.session_state.aportaciones.query("Fondo==@fondo").sort_values("Fecha", ascending=False),
        use_container_width=True,
    )
    st.markdown("---")

# ------------------ REGISTRO OPERACIONES ------------ #
if rol == "admin":
    st.subheader("➕ Registrar Nueva Operación")
    with st.form("nueva_op"):
        c1, c2, c3 = st.columns(3)
        f_op   = c1.date_input("Fecha", datetime.today())
        moneda = c2.text_input("Moneda", "Bitcoin")
        est    = c3.selectbox("Estrategia", ["spot","futuros","staking","holding","ICO","pool_liquidez","farming"])
        c4, c5 = st.columns(2)
        broker = c4.text_input("Broker")
        val    = c5.number_input("Valor Posición USD", min_value=0.0, step=0.01)
        c6, c7, c8, c9 = st.columns(4)
        tp_pct = c6.number_input("TP %", min_value=0.0, step=0.1)
        sl_pct = c7.number_input("SL %", min_value=0.0, step=0.1)
        com    = c8.number_input("Comisiones USD", min_value=0.0, step=0.01)
        res    = c9.selectbox("Resultado", ["Abierta", "Ganadora", "Perdedora"])
        tp_usd = val * tp_pct / 100 - com
        sl_usd = val * sl_pct / 100 + com
        st.markdown(f"TP neto ≈ **${tp_usd:,.2f}** | SL neto ≈ **${sl_usd:,.2f}**")
        if st.form_submit_button("Guardar Operación"):
            op_id = len(st.session_state.ops) + 1
            row_op = {
                "ID": op_id, "Fondo": fondo, "Fecha": pd.to_datetime(f_op), "Moneda": moneda, "Estrategia": est, "Broker": broker,
                "Valor_Pos": val, "TP_%": tp_pct, "SL_%": sl_pct, "Comisiones": com, "TP_usd": tp_usd, "SL_usd": sl_usd, "Resultado": res,
            }
            st.session_state.ops = pd.concat([
                st.session_state.ops, pd.DataFrame([row_op])
            ], ignore_index=True)
            st.success("Operación guardada")
            st.rerun()
    st.markdown("---")

# ------------------ TABLA OPERACIONES --------------- #
st.subheader("🔍 Operaciones")
ops_fondo = st.session_state.ops.query("Fondo==@fondo")
if ops_fondo.empty():
    st.info("Sin operaciones para este fondo")
    st.stop()

c1, c2, c3 = st.columns(3)
desde = c1.date_input("Desde", ops_fondo["Fecha"].min().date())
hasta = c1.date_input("Hasta", ops_fondo["Fecha"].max().date())
bro_sel = c2.multiselect("Broker", sorted(ops_fondo["Broker"].unique()), default=list(ops_fondo["Broker"].unique()))
est_sel = c3.multiselect("Estrategia", sorted(ops_fondo["Estrategia"].unique()), default=list(ops_fondo["Estrategia"].unique()))
mask = (
    (ops_fondo["Fecha"] >= pd.to_datetime(desde)) &
    (ops_fondo["Fecha"] <= pd.to_datetime(hasta)) &
    (ops_fondo["Broker"].isin(bro_sel)) &
    (ops_fondo["Estrategia"].isin(est_sel))
)
filtered_ops = ops_fondo[mask]
st.dataframe(filtered_ops.sort_values("Fecha", ascending=False), use_container_width=True)

# ------------------ RESUMEN DEL FONDO --------------- #
aport_fondo = st.session_state.aportaciones.query("Fondo==@fondo")
cap_in  = aport_fondo.query("Tipo=='Aporte'")["Monto"].sum()
cap_out = aport_fondo.query("Tipo=='Retiro'")["Monto"].sum()
capital_neto = cap_in - cap_out

filtered_ops = filtered_ops.copy()
filtered_ops["PnL"] = 0.0
filtered_ops.loc[filtered_ops["Resultado"]=="Ganadora","PnL"] = filtered_ops["TP_usd"]
filtered_ops.loc[filtered_ops["

