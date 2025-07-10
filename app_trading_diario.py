import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

# Archivos CSV persistentes
CSV_APORTES = "aportes.csv"
CSV_OPERACIONES = "operaciones.csv"

# Inicializar archivos si no existen
def init_csv():
    if not os.path.exists(CSV_APORTES):
        df = pd.DataFrame(columns=["Fondo", "Socio", "Cedula", "Fecha", "Tipo", "Monto"])
        df.to_csv(CSV_APORTES, index=False)
    if not os.path.exists(CSV_OPERACIONES):
        df = pd.DataFrame(columns=["ID", "Fondo", "Fecha", "Moneda", "Estrategia", "Broker", "Valor_Pos", "TP_%", "SL_%", "TP_usd", "SL_usd", "Comision", "Resultado"])
        df.to_csv(CSV_OPERACIONES, index=False)

# Cargar datos
@st.cache_data
def load_csv_data():
    df_aportes = pd.read_csv(CSV_APORTES, parse_dates=["Fecha"])
    df_ops = pd.read_csv(CSV_OPERACIONES, parse_dates=["Fecha"])
    return df_aportes, df_ops

# Guardar datos
def save_csv(df_aportes, df_ops):
    df_aportes.to_csv(CSV_APORTES, index=False)
    df_ops.to_csv(CSV_OPERACIONES, index=False)

# Usuarios demo
USUARIOS = {
    "admin": {"pwd": "admin123", "fondo": "Arkez Invest", "rol": "admin"},
    "juan": {"pwd": "juan123", "fondo": "Cripto Alpha", "rol": "lector"},
    "maria": {"pwd": "maria123", "fondo": "Arkez Invest", "rol": "lector"},
}

# Login UI
def login_ui():
    st.sidebar.title("🔒 Acceso Privado")
    user = st.sidebar.text_input("Usuario")
    pwd = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Entrar"):
        if user in USUARIOS and USUARIOS[user]["pwd"] == pwd:
            st.session_state.logged_in = True
            st.session_state.usuario = user
            st.session_state.rol = USUARIOS[user]["rol"]
            st.session_state.fondo = USUARIOS[user]["fondo"]
            st.rerun()
        else:
            st.sidebar.error("Credenciales incorrectas ❌")

# Inicializar sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Ejecutar login si no está logueado
if not st.session_state.logged_in:
    login_ui()
    st.stop()

# Cargar datos
init_csv()
df_aportes, df_ops = load_csv_data()

usuario = st.session_state.usuario
rol = st.session_state.rol
fondo = st.session_state.fondo

st.set_page_config(page_title="Diario de Trading", layout="wide")
st.title("📈 Diario & Gestor de Fondos de Inversión")
st.markdown(f"**👤 {usuario}** — **Fondo:** {fondo}")
st.markdown("---")

# =================== MOVIMIENTOS DE CAPITAL =================== #
if rol == "admin":
    st.subheader("💰 Movimientos de Capital (Socios)")
    with st.form("form_capital"):
        c1, c2, c3, c4 = st.columns(4)
        socio = c1.text_input("Socio")
        cedula = c2.text_input("Cédula")
        tipo = c3.selectbox("Tipo", ["Aporte", "Retiro"])
        monto = c4.number_input("Monto (USD)", step=0.01)
        fecha = st.date_input("Fecha", datetime.today())
        if st.form_submit_button("Guardar Movimiento"):
            nuevo = pd.DataFrame([{"Fondo": fondo, "Socio": socio, "Cedula": cedula, "Fecha": fecha, "Tipo": tipo, "Monto": monto}])
            df_aportes = pd.concat([df_aportes, nuevo], ignore_index=True)
            save_csv(df_aportes, df_ops)
            st.success("Movimiento registrado ✔")
            st.rerun()

    df_admin_aportes = df_aportes[df_aportes["Fondo"] == fondo].copy()
    for i, row in df_admin_aportes.iterrows():
        st.write(row.to_dict())
        c1, c2 = st.columns([1, 1])
        if c1.button(f"🗑️ Eliminar {i}", key=f"del_aporte_{i}"):
            df_aportes.drop(index=i, inplace=True)
            save_csv(df_aportes, df_ops)
            st.success("Registro eliminado")
            st.rerun()
        if c2.button(f"✏️ Editar {i}", key=f"edit_aporte_{i}"):
            with st.form(f"editar_aporte_{i}"):
                socio = st.text_input("Socio", row["Socio"])
                cedula = st.text_input("Cédula", row["Cedula"])
                tipo = st.selectbox("Tipo", ["Aporte", "Retiro"], index=["Aporte", "Retiro"].index(row["Tipo"]))
                monto = st.number_input("Monto (USD)", value=row["Monto"], step=0.01)
                fecha = st.date_input("Fecha", row["Fecha"])
                if st.form_submit_button("Guardar Cambios"):
                    df_aportes.at[i, "Socio"] = socio
                    df_aportes.at[i, "Cedula"] = cedula
                    df_aportes.at[i, "Tipo"] = tipo
                    df_aportes.at[i, "Monto"] = monto
                    df_aportes.at[i, "Fecha"] = fecha
                    save_csv(df_aportes, df_ops)
                    st.success("Registro editado ✔")
                    st.rerun()
    st.markdown("---")

elif rol == "lector":
    st.info("Solo lectura disponible para este usuario. Puedes ver los registros del fondo asociado.")
    st.subheader("📄 Movimientos de Capital Registrados")
    st.dataframe(df_aportes[df_aportes["Fondo"] == fondo].sort_values("Fecha", ascending=False), use_container_width=True)

# =================== REGISTRO DE OPERACIONES =================== #
if rol == "admin":
    st.subheader("📝 Registrar Nueva Operación")
    with st.form("form_operacion"):
        c1, c2, c3 = st.columns(3)
        fecha_op = c1.date_input("Fecha de la Operación", datetime.today())
        moneda = c2.text_input("Cripto / Activo", "BTC")
        estrategia = c3.selectbox("Estrategia", ["spot", "futuros", "holding", "staking", "otros"])

        c4, c5, c6 = st.columns(3)
        broker = c4.text_input("Broker / Exchange")
        valor_pos = c5.number_input("Valor de la Posición (USD)", step=0.01)
        comision = c6.number_input("Comisión (USD)", step=0.01)

        c7, c8, c9 = st.columns(3)
        tp_pct = c7.number_input("Take Profit %", step=0.1)
        sl_pct = c8.number_input("Stop Loss %", step=0.1)
        resultado = c9.selectbox("Resultado", ["Abierta", "Ganadora", "Perdedora"])

        tp_usd = valor_pos * tp_pct / 100
        sl_usd = valor_pos * sl_pct / 100
        st.markdown(f"**TP Estimado:** ${tp_usd:,.2f} | **SL Estimado:** ${sl_usd:,.2f}")

        if st.form_submit_button("Guardar Operación"):
            nueva_op = pd.DataFrame([{"ID": len(df_ops)+1, "Fondo": fondo, "Fecha": fecha_op, "Moneda": moneda, "Estrategia": estrategia, "Broker": broker, "Valor_Pos": valor_pos, "TP_%": tp_pct, "SL_%": sl_pct, "TP_usd": tp_usd, "SL_usd": sl_usd, "Comision": comision, "Resultado": resultado}])
            df_ops = pd.concat([df_ops, nueva_op], ignore_index=True)
            save_csv(df_aportes, df_ops)
            st.success("Operación guardada ✔")
            st.rerun()

# =================== VISUALIZACIÓN DE OPERACIONES =================== #
st.subheader("📊 Operaciones del Fondo")
ops_fondo = df_ops[df_ops["Fondo"] == fondo].copy()
if not ops_fondo.empty:
    c1, c2 = st.columns(2)
    desde = c1.date_input("Desde", ops_fondo["Fecha"].min().date())
    hasta = c2.date_input("Hasta", ops_fondo["Fecha"].max().date())

    ops_filtradas = ops_fondo[(ops_fondo["Fecha"] >= pd.to_datetime(desde)) & (ops_fondo["Fecha"] <= pd.to_datetime(hasta))]
    ops_filtradas["PnL"] = 0.0
    ops_filtradas.loc[ops_filtradas["Resultado"] == "Ganadora", "PnL"] = ops_filtradas["TP_usd"] - ops_filtradas["Comision"]
    ops_filtradas.loc[ops_filtradas["Resultado"] == "Perdedora", "PnL"] = -ops_filtradas["SL_usd"] - ops_filtradas["Comision"]

    for i, row in ops_filtradas.iterrows():
        st.write(row.to_dict())
        c1, c2 = st.columns([1, 1])
        if rol == "admin" and c1.button(f"🗑️ Eliminar operación {i}", key=f"del_op_{i}"):
            df_ops.drop(index=i, inplace=True)
            save_csv(df_aportes, df_ops)
            st.success("Operación eliminada")
            st.rerun()
        if rol == "admin" and c2.button(f"✏️ Editar operación {i}", key=f"edit_op_{i}"):
            with st.form(f"editar_op_{i}"):
                fecha = st.date_input("Fecha", row["Fecha"])
                moneda = st.text_input("Moneda", row["Moneda"])
                estrategia = st.selectbox("Estrategia", ["spot", "futuros", "holding", "staking", "otros"], index=["spot", "futuros", "holding", "staking", "otros"].index(row["Estrategia"]))
                broker = st.text_input("Broker", row["Broker"])
                valor_pos = st.number_input("Valor Pos", value=row["Valor_Pos"], step=0.01)
                tp_pct = st.number_input("TP %", value=row["TP_%"], step=0.1)
                sl_pct = st.number_input("SL %", value=row["SL_%"], step=0.1)
                comision = st.number_input("Comisión", value=row["Comision"], step=0.01)
                resultado = st.selectbox("Resultado", ["Abierta", "Ganadora", "Perdedora"], index=["Abierta", "Ganadora", "Perdedora"].index(row["Resultado"]))
                tp_usd = valor_pos * tp_pct / 100
                sl_usd = valor_pos * sl_pct / 100

                if st.form_submit_button("Guardar Cambios"):
                    df_ops.at[i, "Fecha"] = fecha
                    df_ops.at[i, "Moneda"] = moneda
                    df_ops.at[i, "Estrategia"] = estrategia
                    df_ops.at[i, "Broker"] = broker
                    df_ops.at[i, "Valor_Pos"] = valor_pos
                    df_ops.at[i, "TP_%"] = tp_pct
                    df_ops.at[i, "SL_%"] = sl_pct
                    df_ops.at[i, "TP_usd"] = tp_usd
                    df_ops.at[i, "SL_usd"] = sl_usd
                    df_ops.at[i, "Comision"] = comision
                    df_ops.at[i, "Resultado"] = resultado
                    save_csv(df_aportes, df_ops)
                    st.success("Operación actualizada ✔")
                    st.rerun()

    st.dataframe(ops_filtradas.sort_values("Fecha", ascending=False), use_container_width=True)

    # ======== RESUMEN ======== #
    st.subheader("📈 Rendimiento del Fondo")
    aportes_fondo = df_aportes[df_aportes["Fondo"] == fondo]
    cap_in = aportes_fondo[aportes_fondo["Tipo"] == "Aporte"]["Monto"].sum()
    cap_out = aportes_fondo[aportes_fondo["Tipo"] == "Retiro"]["Monto"].sum()
    capital_neto = cap_in - cap_out
    ganancia_total = ops_filtradas["PnL"].sum()
    total_final = capital_neto + ganancia_total
    rendimiento_pct = (ganancia_total / capital_neto * 100) if capital_neto else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Capital Neto", f"${capital_neto:,.2f}")
    c2.metric("Ganancia/Perdida", f"${ganancia_total:,.2f}")
    c3.metric("Total Final", f"${total_final:,.2f}")
    c4.metric("Rendimiento %", f"{rendimiento_pct:.2f}%")

    # ======== GRÁFICO ======== #
    cerradas = ops_filtradas[ops_filtradas["Resultado"] != "Abierta"].copy()
    if not cerradas.empty:
        cerradas = cerradas.sort_values("Fecha")
        cerradas["Total_Acumulado"] = capital_neto + cerradas["PnL"].cumsum()
        fig = px.line(cerradas, x="Fecha", y="Total_Acumulado", title="Evolución del Capital", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay operaciones cerradas para graficar.")
else:
    st.info("No hay operaciones registradas para este fondo.")
