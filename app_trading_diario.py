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

    # Verificar columnas necesarias
    expected_cols_ops = ["ID", "Fondo", "Fecha", "Moneda", "Estrategia", "Broker", "Valor_Pos", "TP_%", "SL_%", "TP_usd", "SL_usd", "Comision", "Resultado"]
    for col in expected_cols_ops:
        if col not in df_ops.columns:
            df_ops[col] = None

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

if not st.session_state.logged_in:
    login_ui()
    st.stop()

# Cargar datos
init_csv()
df_aportes, df_ops = load_csv_data()

# Guardar en session_state
st.session_state.df_aportes = df_aportes.copy()
st.session_state.df_ops = df_ops.copy()

usuario = st.session_state.usuario
rol = st.session_state.rol

# FONDOS DISPONIBLES
fondos_disponibles = sorted(set(st.session_state.df_aportes["Fondo"]).union(set(st.session_state.df_ops["Fondo"])))
if rol == "admin":
    fondos_disponibles = sorted(set(fondos_disponibles).union({USUARIOS[usuario]["fondo"]}))

st.set_page_config(page_title="Diario de Trading", layout="wide")
st.title("📈 Diario & Gestor de Fondos de Inversión")
fondo = st.selectbox("Selecciona el fondo", fondos_disponibles, index=fondos_disponibles.index(USUARIOS[usuario]["fondo"]))
st.session_state.fondo = fondo
st.markdown(f"**👤 {usuario}** — **Fondo:** {fondo}")
st.markdown("---")

# === MOVIMIENTOS DE CAPITAL ===
if rol == "admin":
    st.subheader("💰 Movimientos de Capital (Socios)")
    with st.form("form_aporte"):
        c1, c2, c3, c4 = st.columns(4)
        socio = c1.text_input("Socio")
        cedula = c2.text_input("Cédula")
        tipo = c3.selectbox("Tipo", ["Aporte", "Retiro"])
        monto = c4.number_input("Monto", step=0.01)
        fecha = st.date_input("Fecha", value=datetime.today())
        if st.form_submit_button("Guardar"):
            nuevo = pd.DataFrame([[fondo, socio, cedula, fecha, tipo, monto]], columns=st.session_state.df_aportes.columns)
            st.session_state.df_aportes = pd.concat([st.session_state.df_aportes, nuevo], ignore_index=True)
            save_csv(st.session_state.df_aportes, st.session_state.df_ops)
            st.success("Movimiento guardado ✔")
            st.rerun()

    df_aportes_fondo = st.session_state.df_aportes[st.session_state.df_aportes["Fondo"] == fondo]
    st.dataframe(df_aportes_fondo.sort_values("Fecha", ascending=False), use_container_width=True)
    if st.button("🗑 Eliminar último movimiento"):
        st.session_state.df_aportes = st.session_state.df_aportes.drop(df_aportes_fondo.tail(1).index)
        save_csv(st.session_state.df_aportes, st.session_state.df_ops)
        st.rerun()

# === REGISTRAR OPERACIÓN ===
if rol == "admin":
    st.subheader("📌 Registrar Nueva Operación")
    with st.form("form_op"):
        c1, c2, c3 = st.columns(3)
        fecha_op = c1.date_input("Fecha", value=datetime.today())
        moneda = c2.text_input("Moneda")
        estrategia = c3.selectbox("Estrategia", ["spot", "futuros", "staking", "holding", "ICO"])

        c4, c5, c6 = st.columns(3)
        broker = c4.text_input("Broker")
        valor_pos = c5.number_input("Valor Posición", step=0.01)
        comision = c6.number_input("Comisión USD", step=0.01)

        c7, c8, c9 = st.columns(3)
        tp_pct = c7.number_input("TP %")
        sl_pct = c8.number_input("SL %")
        resultado = c9.selectbox("Resultado", ["Abierta", "Ganadora", "Perdedora"])

        tp_usd = valor_pos * tp_pct / 100
        sl_usd = valor_pos * sl_pct / 100

        if st.form_submit_button("Guardar Operación"):
            new_id = st.session_state.df_ops["ID"].max() + 1 if not st.session_state.df_ops.empty else 1
            row = pd.Series({
                "ID": new_id,
                "Fondo": fondo,
                "Fecha": fecha_op,
                "Moneda": moneda,
                "Estrategia": estrategia,
                "Broker": broker,
                "Valor_Pos": valor_pos,
                "TP_%": tp_pct,
                "SL_%": sl_pct,
                "TP_usd": tp_usd,
                "SL_usd": sl_usd,
                "Comision": comision,
                "Resultado": resultado
            })
            st.session_state.df_ops = pd.concat([st.session_state.df_ops, row.to_frame().T], ignore_index=True)
            save_csv(st.session_state.df_aportes, st.session_state.df_ops)
            st.success("Operación guardada ✔")
            st.rerun()

    df_ops_fondo = st.session_state.df_ops[st.session_state.df_ops["Fondo"] == fondo]
    st.dataframe(df_ops_fondo.sort_values("Fecha", ascending=False), use_container_width=True)
    if st.button("🗑 Eliminar última operación"):
        st.session_state.df_ops = st.session_state.df_ops.drop(df_ops_fondo.tail(1).index)
        save_csv(st.session_state.df_aportes, st.session_state.df_ops)
        st.rerun()

# === RESUMEN Y GRÁFICAS ===
st.subheader("📊 Resumen del Fondo")
df_aportes_fondo = st.session_state.df_aportes[st.session_state.df_aportes["Fondo"] == fondo]
df_ops_fondo = st.session_state.df_ops[st.session_state.df_ops["Fondo"] == fondo]

capital_in = df_aportes_fondo[df_aportes_fondo["Tipo"] == "Aporte"]["Monto"].sum()
capital_out = df_aportes_fondo[df_aportes_fondo["Tipo"] == "Retiro"]["Monto"].sum()
capital_neto = capital_in - capital_out

ops_cerradas = df_ops_fondo[df_ops_fondo["Resultado"] != "Abierta"].copy()
ops_cerradas["PnL"] = 0
ops_cerradas.loc[ops_cerradas["Resultado"] == "Ganadora", "PnL"] = ops_cerradas["TP_usd"] - ops_cerradas["Comision"]
ops_cerradas.loc[ops_cerradas["Resultado"] == "Perdedora", "PnL"] = -ops_cerradas["SL_usd"] - ops_cerradas["Comision"]

ganancia_total = ops_cerradas["PnL"].sum()
total_final = capital_neto + ganancia_total
rendimiento_pct = (ganancia_total / capital_neto * 100).round(2) if capital_neto else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Capital Neto", f"${capital_neto:,.2f}")
col2.metric("Ganancia Total", f"${ganancia_total:,.2f}")
col3.metric("Total Final", f"${total_final:,.2f}")
col4.metric("Rendimiento %", f"{rendimiento_pct:.2f}%")

if not ops_cerradas.empty:
    ops_cerradas = ops_cerradas.sort_values("Fecha")
    ops_cerradas["Acumulado"] = capital_neto + ops_cerradas["PnL"].cumsum()
    st.markdown("#### 📈 Evolución del Fondo")
    fig = px.line(ops_cerradas, x="Fecha", y="Acumulado", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# === RENDIMIENTO POR SOCIO ===
st.subheader("🥮 Rendimiento por Socio")
df_socios = df_aportes_fondo.groupby("Socio")["Monto"].agg([
    ("Aportes", lambda x: x[df_aportes_fondo["Tipo"] == "Aporte"].sum()),
    ("Retiros", lambda x: x[df_aportes_fondo["Tipo"] == "Retiro"].sum()),
])
df_socios["Capital Neto"] = df_socios["Aportes"] - df_socios["Retiros"]
df_socios["Participación"] = df_socios["Capital Neto"] / capital_neto if capital_neto else 0
df_socios["Ganancia"] = df_socios["Participación"] * ganancia_total

# Asegurar tipos numéricos
df_socios["Ganancia"] = pd.to_numeric(df_socios["Ganancia"], errors="coerce")
df_socios["Capital Neto"] = pd.to_numeric(df_socios["Capital Neto"], errors="coerce")

# Cálculo del rendimiento
try:
    df_socios["Rendimiento %"] = ((df_socios["Ganancia"] / df_socios["Capital Neto"].replace(0, pd.NA)) * 100).round(2).fillna(0)
except Exception:
    df_socios["Rendimiento %"] = 0

st.dataframe(df_socios.round(2), use_container_width=True)
