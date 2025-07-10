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
    st.session_state.aportaciones = pd.DataFrame(columns=["idx","Fondo","Socio","Cedula","Fecha","Tipo","Monto"])
    st.session_state.ops = pd.DataFrame(columns=[
        "idx","ID","Fondo","Fecha","Moneda","Estrategia","Broker","Valor_Pos","TP_%","SL_%","Comisiones","TP_usd","SL_usd","Resultado"
    ])

# -------------------------------------------------
# LOGIN / LOGOUT
# -------------------------------------------------

def login_ui():
    st.sidebar.title("🔒 Acceso Privado")
    user = st.sidebar.text_input("Usuario")
    pwd  = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Entrar"):
        if user in USUARIOS and USUARIOS[user]["pwd"] == pwd:
            st.session_state.logged_in = True
            st.session_state.usuario   = user
            st.session_state.rol       = USUARIOS[user]["rol"]
            st.session_state.fondo     = USUARIOS[user]["fondo"]
            st.rerun()
        else:
            st.sidebar.error("Credenciales incorrectas ❌")

if st.session_state.get("logged_in"):
    if st.sidebar.button("Cerrar Sesión ⏻"):
        for k in ["logged_in","usuario","rol","fondo"]:
            st.session_state.pop(k, None)
        st.rerun()

if not st.session_state.get("logged_in", False):
    login_ui()
    st.stop()

usuario = st.session_state.usuario
rol     = st.session_state.rol
fondo   = st.session_state.fondo

# -------------------------------------------------
# FONDOS (ADMIN)
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
# HEADER
# -------------------------------------------------
st.title("📈 Diario & Gestor de Fondos de Inversión")
st.markdown(f"**👤 {usuario}** — **Fondo:** {fondo}")

# =================================================
# MOVIMIENTOS DE CAPITAL
# =================================================
if rol == "admin":
    st.header("💰 Movimientos de Capital (Socios)")
    with st.form("form_aporte"):
        c1,c2,c3,c4 = st.columns(4)
        socio  = c1.text_input("Socio")
        cedula = c2.text_input("Cédula/ID")
        tipo   = c3.selectbox("Tipo", ["Aporte","Retiro"])
        monto  = c4.number_input("Monto USD", min_value=0.0, step=0.01)
        fecha  = st.date_input("Fecha", datetime.today())
        if st.form_submit_button("Guardar"):
            idx = len(st.session_state.aportaciones)
            nuevo = {"idx":idx,"Fondo":fondo,"Socio":socio.strip(),"Cedula":cedula.strip(),"Fecha":fecha,"Tipo":tipo,"Monto":monto}
            st.session_state.aportaciones = pd.concat([st.session_state.aportaciones, pd.DataFrame([nuevo])], ignore_index=True)
            st.success("Registro agregado ✔️")
            st.rerun()

aport_df = st.session_state.aportaciones.query("Fondo==@fondo")
if not aport_df.empty:
    st.dataframe(aport_df.drop(columns=["idx"]), use_container_width=True)
    col1,col2 = st.columns(2)
    idx_sel = col1.number_input("Fila capital a editar/eliminar",min_value=0,max_value=int(aport_df["idx"].max()),step=1)
    if col1.button("Eliminar capital"):
        st.session_state.aportaciones = st.session_state.aportaciones[st.session_state.aportaciones["idx"]!=idx_sel]
        st.success("Eliminado ✔️")
        st.rerun()
    if col2.button("Editar capital"):
        fila = st.session_state.aportaciones.loc[st.session_state.aportaciones["idx"]==idx_sel].iloc[0]
        with st.form("edit_aporte"):
            socio_e  = st.text_input("Socio", value=fila.Socio)
            ced_e    = st.text_input("Cédula", value=fila.Cedula)
            tipo_e   = st.selectbox("Tipo", ["Aporte","Retiro"], index=0 if fila.Tipo=="Aporte" else 1)
            monto_e  = st.number_input("Monto USD", value=float(fila.Monto))
            fecha_e  = st.date_input("Fecha", value=fila.Fecha)
            if st.form_submit_button("Actualizar"):
                st.session_state.aportaciones.loc[st.session_state.aportaciones["idx"]==idx_sel, ["Socio","Cedula","Tipo","Monto","Fecha"]] = [socio_e, ced_e, tipo_e, monto_e, fecha_e]
                st.success("Actualizado ✔️")
                st.rerun()
else:
    st.info("Sin movimientos registrados")

# =================================================
# REGISTRAR OPERACIÓN
# =================================================
st.header("➕ Registrar Nueva Operación")
if rol == "admin":
    with st.form("form_op"):
        c1,c2,c3 = st.columns(3)
        fecha_op = c1.date_input("Fecha", datetime.today())
        moneda   = c2.text_input("Moneda","BTC")
        est      = c3.selectbox("Estrategia",["spot","futuros","staking","holding","ICO","pool_liquidez","farming"])
        c4,c5 = st.columns(2)
        broker   = c4.text_input("Broker")
        valor_pos= c5.number_input("Valor Posición USD", min_value=0.0, step=0.01)
        c6,c7,c8,c9 = st.columns(4)
        tp_pct   = c6.number_input("TP %", min_value=0.0, step=0.1)
        sl_pct   = c7.number_input("SL %", min_value=0.0, step=0.1)
        com      = c8.number_input("Comisiones USD", min_value=0.0, step=0.01)
        res      = c9.selectbox("Resultado", ["Abierta","Ganadora","Perdedora"])
        tp_usd   = valor_pos*tp_pct/100 - com
        sl_usd   = valor_pos*sl_pct/100 + com
        st.markdown(f"TP ≈ **${tp_usd:,.2f}** | SL ≈ **${sl_usd:,.2f}**")
        if st.form_submit_button("Guardar Operación"):
            idx = len(st.session_state.ops)
            new_op = {"idx":idx,"ID":idx+1,"Fondo":fondo,"Fecha":fecha_op,"Moneda":moneda,"Estrategia":est,"Broker":broker,
                      "Valor_Pos":valor_pos,"TP_%":tp_pct,"SL_%":sl_pct,"Comisiones":com,"TP_usd":tp_usd,"SL_usd":sl_usd,"Resultado":res}
            st.session_state.ops = pd.concat([st.session_state.ops, pd.DataFrame([new_op])], ignore_index=True)
            st.success("Operación registrada ✔️")
            st.rerun()

ops_df = st.session_state.ops.query("Fondo==@fondo")
if not ops_df.empty:
    st.dataframe(ops_df.drop(columns=["idx"]), use_container_width=True)
    col1,col2 = st.columns(2)
    idx_op = col1.number_input("Fila op a editar/eliminar",min_value=0,max_value=int(ops_df["idx"].max()),step=1)
    if col1.button("Eliminar op"):
        st.session_state.ops = st.session_state.ops[st.session_state.ops["idx"]!=idx_op]
        st.success("Operación eliminada ✔️")
        st.rerun()

    if col2.button("Editar op"):
        row = st.session_state.ops.loc[st.session_state.ops["idx"]==idx_op].iloc[0]
        with st.form("edit_op"):
            moneda_e = st.text_input("Moneda", value=row.Moneda)
            est_e = st.selectbox("Estrategia", ["spot","futuros","staking","holding","ICO","pool_liquidez","farming"], index=["spot","futuros","staking","holding","ICO","pool_liquidez","farming"].index(row.Estrategia))
            broker_e = st.text_input("Broker", value=row.Broker)
            val_e = st.number_input("Valor Pos USD", value=float(row.Valor_Pos))
            tp_pct_e = st.number_input("TP %", value=float(row["TP_%"]))
            sl_pct_e = st.number_input("SL %", value=float(row["SL_%"]))
            com_e = st.number_input("Comisiones", value=float(row.Comisiones))
            res_e = st.selectbox("Resultado", ["Abierta","Ganadora","Perdedora"], index=["Abierta","Ganadora","Perdedora"].index(row.Resultado))
            if st.form_submit_button("Actualizar"):
                tp_usd_e = val_e*tp_pct_e/100 - com_e
                sl_usd_e = val_e*sl_pct_e/100 + com_e
                st.session_state.ops.loc[st.session_state.ops["idx"]==idx_op, ["Moneda","Estrategia","Broker","Valor_Pos","TP_%","SL_%","Comisiones","TP_usd","SL_usd","Resultado"]] = [moneda_e, est_e, broker_e, val_e, tp_pct_e, sl_pct_e, com_e, tp_usd_e, sl_usd_e, res_e]
                st.success("Operación actualizada ✔️")
                st.rerun()
else:
    st.info("Sin operaciones registradas para este fondo")

# =================================================
# RESUMEN FINAL KPIs Y GRÁFICAS
# =================================================
if not ops_df.empty:
    cerradas = ops_df[ops_df["Resultado"] != "Abierta"].copy()
    cerradas["PnL"] = 0.0
    cerradas.loc[cerradas["Resultado"] == "Ganadora", "PnL"] = cerradas["TP_usd"]
    cerradas.loc[cerradas["Resultado"] == "Perdedora", "PnL"] = -cerradas["SL_usd"]

    cap_aportes = aport_df.query("Tipo=='Aporte'")["Monto"].sum()
    cap_retiros = aport_df.query("Tipo=='Retiro'")["Monto"].sum()
    cap_neto    = cap_aportes - cap_retiros
    total_gan   = cerradas["PnL"].sum()
    total_final = cap_neto + total_gan
    rend_pct    = (total_final - cap_neto) / cap_neto * 100 if cap_neto > 0 else 0

    st.header("📊 KPIs del Fondo")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Capital Neto", f"${cap_neto:,.2f}")
    c2.metric("Gan/Perd", f"${total_gan:,.2f}")
    c3.metric("Total Final", f"${total_final:,.2f}")
    c4.metric("Rendimiento %", f"{rend_pct:.2f}%")

    st.subheader("📈 Evolución del Capital")
    if not cerradas.empty:
        cerradas = cerradas.sort_values("Fecha")
        cerradas["Total_Acc"] = cap_neto + cerradas["PnL"].cumsum()
        fig = px.line(cerradas, x="Fecha", y="Total_Acc", title="Capital Acumulado", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("💹 Rendimiento por Socio")
    resumen_socios = aport_df.query("Tipo=='Aporte'").groupby("Socio")["Monto"].sum().reset_index()
    resumen_socios["% Participación"] = resumen_socios["Monto"] / resumen_socios["Monto"].sum()
    resumen_socios["$ Ganancia"] = resumen_socios["% Participación"] * total_gan
    resumen_socios["% Rendimiento"] = resumen_socios["$ Ganancia"] / resumen_socios["Monto"] * 100
    st.dataframe(resumen_socios, use_container_width=True)
else:
    st.warning("No hay datos suficientes para calcular KPIs o gráficas.")
