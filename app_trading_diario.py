import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
from io import BytesIO
import base64
from fpdf import FPDF

# Configuración inicial
st.set_page_config(page_title="Diario de Trading", layout="wide")
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
CSV_APORTES = os.path.join(DATA_DIR, "aportes.csv")
CSV_OPERACIONES = os.path.join(DATA_DIR, "operaciones.csv")

# Inicializar archivos CSV si no existen
def init_csv():
    if not os.path.exists(CSV_APORTES):
        pd.DataFrame(columns=["Fondo", "Socio", "Cedula", "Fecha", "Tipo", "Monto"]).to_csv(CSV_APORTES, index=False)
    if not os.path.exists(CSV_OPERACIONES):
        pd.DataFrame(columns=["ID", "Fondo", "Fecha", "Moneda", "Estrategia", "Broker", "Valor_Pos", "TP_%", "SL_%", "TP_usd", "SL_usd", "Comision", "Resultado"]).to_csv(CSV_OPERACIONES, index=False)

# Cargar datos
def load_csv_data():
    df_aportes = pd.read_csv(CSV_APORTES)
    df_ops = pd.read_csv(CSV_OPERACIONES)
    df_aportes["Fecha"] = pd.to_datetime(df_aportes["Fecha"], errors="coerce")
    df_ops["Fecha"] = pd.to_datetime(df_ops["Fecha"], errors="coerce")
    return df_aportes, df_ops

# Guardar datos
def save_csv(df_aportes, df_ops):
    df_aportes.to_csv(CSV_APORTES, index=False)
    df_ops.to_csv(CSV_OPERACIONES, index=False)

# Exportar a Excel
def to_excel_download_link(df_dict, nombre_archivo="informe.xlsx"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for name, df in df_dict.items():
            df.to_excel(writer, index=False, sheet_name=name[:31])
    output.seek(0)
    b64 = base64.b64encode(output.read()).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{nombre_archivo}">📥 Descargar Excel</a>'

# Exportar a PDF
def exportar_pdf(texto, nombre_archivo="informe.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for linea in texto.split("\n"):
        pdf.multi_cell(0, 10, txt=linea)
    path = os.path.join(DATA_DIR, nombre_archivo)
    pdf.output(path)
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{nombre_archivo}">📄 Descargar PDF</a>'

# Usuarios demo
USUARIOS = {
    "admin": {"pwd": "admin123", "fondo": "Arkez Invest", "rol": "admin"},
    "juan": {"pwd": "juan123", "fondo": "Cripto Alpha", "rol": "lector"},
    "maria": {"pwd": "maria123", "fondo": "Arkez Invest", "rol": "lector"},
}

# Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.sidebar.title("🔒 Acceso Privado")
    user = st.sidebar.text_input("Usuario")
    pwd = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Entrar"):
        if user in USUARIOS and USUARIOS[user]["pwd"] == pwd:
            st.session_state.update({
                "logged_in": True,
                "usuario": user,
                "rol": USUARIOS[user]["rol"],
                "fondo": USUARIOS[user]["fondo"]
            })
            st.rerun()
        else:
            st.sidebar.error("Credenciales incorrectas ❌")
    st.stop()

if st.sidebar.button("Cerrar Sesión"):
    for key in ["logged_in", "usuario", "rol", "fondo"]:
        st.session_state.pop(key, None)
    st.rerun()

# Datos y contexto
init_csv()
df_aportes, df_ops = load_csv_data()
fondo_actual = st.session_state.fondo
rol = st.session_state.rol
usuario = st.session_state.usuario

# Filtrar fondos disponibles
if rol == "admin":
    fondos_disponibles = sorted(set(df_aportes["Fondo"]).union(df_ops["Fondo"]))
else:
    fondos_disponibles = sorted(df_aportes[df_aportes["Socio"] == usuario]["Fondo"].unique())

# Crear nuevo fondo
if rol == "admin":
    nuevo_fondo = st.sidebar.text_input("➕ Crear nuevo fondo")
    if st.sidebar.button("Agregar Fondo") and nuevo_fondo.strip():
        if nuevo_fondo not in fondos_disponibles:
            fila = pd.DataFrame([[nuevo_fondo, usuario, "", datetime.today(), "Aporte", 0]], columns=df_aportes.columns)
            df_aportes = pd.concat([df_aportes, fila], ignore_index=True)
            save_csv(df_aportes, df_ops)
            st.session_state.fondo = nuevo_fondo
            st.success(f"Fondo '{nuevo_fondo}' creado ✔")
            st.rerun()
        else:
            st.warning("Ese fondo ya existe")

# Selección de fondo
fondo = st.selectbox("Selecciona el fondo", fondos_disponibles, index=fondos_disponibles.index(fondo_actual))
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
            nuevo = pd.DataFrame([[fondo, socio, cedula, fecha, tipo, monto]], columns=df_aportes.columns)
            df_aportes = pd.concat([df_aportes, nuevo], ignore_index=True)
            save_csv(df_aportes, df_ops)
            st.success("Movimiento guardado ✔")
            st.rerun()

    df_aportes_fondo = df_aportes[df_aportes["Fondo"] == fondo]
    st.dataframe(df_aportes_fondo.sort_values("Fecha", ascending=False), use_container_width=True)
    if st.button("🗑 Eliminar último movimiento"):
        df_aportes = df_aportes.drop(df_aportes_fondo.tail(1).index)
        save_csv(df_aportes, df_ops)
        st.rerun()

# === REGISTRAR OPERACIÓN ===
if rol == "admin":
    st.subheader("📌 Registrar Nueva Operación")
    with st.form("form_op"):
        c1, c2, c3 = st.columns(3)
        fecha_op = c1.date_input("Fecha", value=datetime.today())
        moneda = c2.text_input("Moneda")
        estrategia = c3.selectbox("Estrategia", ["Spot", "Futuros", "Staking", "Holding", "Arbitraje", "Bot o Copy Trading", "Farming", "Launchpool", "ICO"])

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
            new_id = df_ops["ID"].max() + 1 if not df_ops.empty else 1
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
            df_ops = pd.concat([df_ops, row.to_frame().T], ignore_index=True)
            save_csv(df_aportes, df_ops)
            st.success("Operación guardada ✔")
            st.rerun()

    df_ops_fondo = df_ops[df_ops["Fondo"] == fondo]
    st.dataframe(df_ops_fondo.sort_values("Fecha", ascending=False), use_container_width=True)
    if st.button("🗑 Eliminar última operación"):
        df_ops = df_ops.drop(df_ops_fondo.tail(1).index)
        save_csv(df_aportes, df_ops)
        st.rerun()

# === RESUMEN Y GRÁFICAS ===
st.subheader("📊 Resumen del Fondo")
df_aportes_fondo = df_aportes[df_aportes["Fondo"] == fondo]
df_ops_fondo = df_ops[df_ops["Fondo"] == fondo]

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

color_rend = "green" if rendimiento_pct >= 0 else "red"
st.markdown(f"### Rendimiento del Fondo: <span style='color:{color_rend}'>**{rendimiento_pct:.2f}%**</span>", unsafe_allow_html=True)

if not ops_cerradas.empty:
    ops_cerradas = ops_cerradas.sort_values("Fecha")
    ops_cerradas["Acumulado"] = capital_neto + ops_cerradas["PnL"].cumsum()
    st.markdown("#### 📈 Evolución del Fondo")
    fig = px.line(ops_cerradas, x="Fecha", y="Acumulado", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# === RENDIMIENTO POR SOCIO ===
st.subheader("🥮 Rendimiento por Socio")
df_socios = df_aportes_fondo.groupby("Socio")["Monto"].agg([
    ("Aportes", lambda x: x[df_aportes_fondo.loc[x.index, "Tipo"] == "Aporte"].sum()),
    ("Retiros", lambda x: x[df_aportes_fondo.loc[x.index, "Tipo"] == "Retiro"].sum()),
])
df_socios["Capital Neto"] = df_socios["Aportes"] - df_socios["Retiros"]
df_socios["Participación"] = df_socios["Capital Neto"] / capital_neto if capital_neto else 0
df_socios["Ganancia"] = df_socios["Participación"] * ganancia_total

df_socios["Ganancia"] = pd.to_numeric(df_socios["Ganancia"], errors="coerce")
df_socios["Capital Neto"] = pd.to_numeric(df_socios["Capital Neto"], errors="coerce")

try:
    df_socios["Rendimiento %"] = ((df_socios["Ganancia"] / df_socios["Capital Neto"].replace(0, pd.NA)) * 100).round(2).fillna(0)
except Exception:
    df_socios["Rendimiento %"] = 0

st.dataframe(df_socios.round(2), use_container_width=True)
