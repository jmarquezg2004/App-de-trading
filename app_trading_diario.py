import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Diario de Trading", layout="wide")

# -------------------------------------------------
# USUARIOS DEMO
# -------------------------------------------------
USUARIOS = {
    "admin": {"pwd": "admin123", "fondo": "Arkez Invest", "rol": "admin"},
    "juan":  {"pwd": "juan123",  "fondo": "Cripto Alpha", "rol": "lector"},
    "maria": {"pwd": "maria123", "fondo": "Arkez Invest", "rol": "lector"},
}
DEFAULT_FONDOS = ["Arkez Invest", "Cripto Alpha"]

# -------------------------------------------------
# INIT SESSION STATE
# -------------------------------------------------
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

# -------------------------------------------------
# LOGIN UI
# -------------------------------------------------

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

# -------------------------------------------------
# GESTIÓN DE FONDOS (ADMIN)
# -------------------------------------------------
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

# -------------------------------------------------
# ENCABEZADO
# -------------------------------------------------
st.title("📈 Diario & Gestor de Fondos de Inversión")
st.markdown(f"**👤 {usuario}** — **Fondo:** {fondo}")

# -------------------------------------------------
# APORTES / RETIROS
# -------------------------------------------------
if rol == "admin":
    st.subheader("💰 Movimientos de Capital (Socios)")
    with st.form("mov_cap"):
        c1, c2, c3, c4 = st.columns(4)
        socio  = c1.text_input("Socio")
        ced    = c2.text_input("Cédula/ID")
        tipo   = c3.selectbox("Tipo", ["Aporte", "Retiro"])
        monto  = c4.number_input("Monto USD", min_value=0.0, step=0.01)
        fecha_mov = st.date_input("Fecha", datetime.today())
        if st.form_submit_button("Guardar"):
            nuevo = {"Fondo":fondo,"Socio":socio,"Cedula":ced,"Fecha":fecha_mov,"Tipo":tipo,"Monto":monto}
            st.session_state.aportaciones = pd.concat([st.session_state.aportaciones, pd.DataFrame([nuevo])], ignore_index=True)
            st.success("Movimiento registrado ✔️")
            st.rerun()
    st.dataframe(st.session_state.aportaciones.query("Fondo==@fondo"), use_container_width=True)

# -------------------------------------------------
# REGISTRAR OPERACIÓN
# -------------------------------------------------
if rol == "admin":
    st.subheader("➕ Registrar Nueva Operación")
    with st.form("nueva_op"):
        c1,c2,c3 = st.columns(3)
        f_op = c1.date_input("Fecha", datetime.today())
        moneda = c2.text_input("Moneda","Bitcoin")
        est = c3.selectbox("Estrategia", ["spot","futuros","staking","holding","ICO","pool_liquidez","farming"])
        c4,c5 = st.columns(2)
        broker = c4.text_input("Broker")
        val = c5.number_input("Valor Posición USD", min_value=0.0, step=0.01)
        c6,c7,c8,c9 = st.columns(4)
        tp_pct = c6.number_input("TP %", min_value=0.0, step=0.1)
        sl_pct = c7.number_input("SL %", min_value=0.0, step=0.1)
        com    = c8.number_input("Comisiones USD", min_value=0.0, step=0.01)
        res    = c9.selectbox("Resultado", ["Abierta","Ganadora","Perdedora"])
        tp_usd = val*tp_pct/100 - com
        sl_usd = val*sl_pct/100 + com
        st.markdown(f"TP neto ≈ **${tp_usd:,.2f}** | SL neto ≈ **${sl_usd:,.2f}**")
        if st.form_submit_button("Guardar Operación"):
            oid = len(st.session_state.ops)+1
            nueva_op = {"ID":oid,"Fondo":fondo,"Fecha":pd.to_datetime(f_op),"Moneda":moneda,"Estrategia":est,"Broker":broker,
                        "Valor_Pos":val,"TP_%":tp_pct,"SL_%":sl_pct,"Comisiones":com,"TP_usd":tp_usd,"SL_usd":sl_usd,"Resultado":res}
            st.session_state.ops = pd.concat([st.session_state.ops, pd.DataFrame([nueva_op])], ignore_index=True)
            st.success("Operación guardada ✔️")
            st.rerun()

# -------------------------------------------------
# TABLA OPERACIONES + FILTRO
# -------------------------------------------------
st.subheader("🔍 Operaciones")
ops_fondo = st.session_state.ops.query("Fondo==@fondo")
if ops_fondo.empty:
    st.info("Sin operaciones para este fondo")
    st.stop()

c1,c2,c3 = st.columns(3)
desde = c1.date_input("Desde", ops_fondo["Fecha"].min().date())
hasta = c1.date_input("Hasta", ops_fondo["Fecha"].max().date())
bro_sel = c2.multiselect("Broker", sorted(ops_fondo["Broker"].unique()), default=list(ops_fondo["Broker"].unique()))
est_sel = c3.multiselect("Estrategia", sorted(ops_fondo["Estrategia"].unique()), default=list(ops_fondo["Estrategia"].unique()))
mask = (
    (ops_fondo["Fecha"]>=pd.to_datetime(desde)) &
    (ops_fondo["Fecha"]<=pd.to_datetime(hasta)) &
    (ops_fondo["Broker"].isin(bro_sel)) &
    (ops_fondo["Estrategia"].isin(est_sel))
)
filtered_ops = ops_fondo[mask]
st.dataframe(filtered_ops.sort_values("Fecha", ascending=False), use_container_width=True)

# -------------------------------------------------
# RESUMEN DEL FONDO
# -------------------------------------------------
st.subheader("📊 Resumen del Fondo")

# Capital neto aportado
aport_fondo = st.session_state.aportaciones.query("Fondo==@fondo")
cap_in  = aport_fondo.query("Tipo=='Aporte'")["Monto"].sum()
cap_out = aport_fondo.query("Tipo=='Retiro'")["Monto"].sum()
capital_neto = cap_in - cap_out

# PnL neto
filtered_ops = filtered_ops.copy()
filtered_ops["PnL"] = 0.0
filtered_ops.loc[filtered_ops["Resultado"] == "Ganadora", "PnL"]  = filtered_ops["TP_usd"]
filtered_ops.loc[filtered_ops["Resultado"] == "Perdedora", "PnL"] = -filtered_ops["SL_usd"]

pnl_total = filtered_ops["PnL"].sum()
capital_total = capital_neto + pnl_total
rendimiento_pct = (pnl_total / capital_neto * 100) if capital_neto else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Capital Neto (USD)", f"${capital_neto:,.2f}")
m2.metric("PnL Acumulado",      f"${pnl_total:,.2f}")
m3.metric("Total USD",          f"${capital_total:,.2f}")
m4.metric("Rendimiento %",      f"{rendimiento_pct:.2f}%")

# Rendimiento por socio
st.markdown("### 👥 Rendimiento por Socio")
if not aport_fondo.empty and capital_neto > 0:
    def neto(df):
        return df.loc[df["Tipo"]=="Aporte","Monto"].sum() - df.loc[df["Tipo"]=="Retiro","Monto"].sum()
    socios_cap = aport_fondo.groupby("Socio").apply(neto).reset_index(name="Capital_Neto")
    socios_cap["% Participación"] = socios_cap["Capital_Neto"] / capital_neto * 100
    socios_cap["P/L Asignado"]    = socios_cap["Capital_Neto"] / capital_neto * pnl_total
    socios_cap["Retorno %"]       = socios_cap["P/L Asignado"] / socios_cap["Capital_Neto"] * 100
    st.dataframe(socios_cap.round(2), use_container_width=True)
else:
    st.info("Sin datos de aportes para calcular rendimiento por socio")

# Gráfica de evolución del fondo
st.markdown("#### 📈 Evolución del Fondo")
ops_cerradas = filtered_ops[filtered_ops["Resultado"] != "Abierta"].copy()
if not ops_cerradas.empty:
    ops_cerradas = ops_cerradas.sort_values("Fecha")
    ops_cerradas["Equity"] = capital_neto + ops_cerradas["PnL"].cumsum()
    fig = px.line(ops_cerradas, x="Fecha", y="Equity", markers=True, title="Equity Curve")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Aún no hay operaciones cerradas para mostrar gráfica.")
