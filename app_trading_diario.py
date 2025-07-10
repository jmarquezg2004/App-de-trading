import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io
import os

st.set_page_config(page_title="Diario de Trading", layout="wide")

# -------------------------------------------------
# ARCHIVOS CSV (Persistencia)
# -------------------------------------------------
APORTES_FILE = "aportaciones.csv"
OPERACIONES_FILE = "operaciones.csv"

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

    if os.path.exists(APORTES_FILE):
        st.session_state.aportaciones = pd.read_csv(APORTES_FILE)
    else:
        st.session_state.aportaciones = pd.DataFrame(columns=["idx","Fondo","Socio","Cedula","Fecha","Tipo","Monto"])

    if os.path.exists(OPERACIONES_FILE):
        st.session_state.ops = pd.read_csv(OPERACIONES_FILE)
    else:
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

# Botones de descarga CSV
st.sidebar.markdown("---")
buf_ap = io.StringIO()
st.session_state.aportaciones.to_csv(buf_ap, index=False)
st.sidebar.download_button("📥 Descargar Aportaciones CSV", buf_ap.getvalue(), "aportaciones.csv", "text/csv")

buf_op = io.StringIO()
st.session_state.ops.to_csv(buf_op, index=False)
st.sidebar.download_button("📥 Descargar Operaciones CSV", buf_op.getvalue(), "operaciones.csv", "text/csv")

# Botones de carga CSV
st.sidebar.markdown("---")
sub_ap = st.sidebar.file_uploader("📤 Cargar Aportaciones CSV", type="csv")
if sub_ap:
    df_ap = pd.read_csv(sub_ap)
    if set(df_ap.columns).issubset(set(st.session_state.aportaciones.columns)):
        st.session_state.aportaciones = df_ap
        st.session_state.aportaciones.to_csv(APORTES_FILE, index=False)
        st.sidebar.success("Aportaciones cargadas correctamente")
    else:
        st.sidebar.error("Columnas inválidas en Aportaciones")

sub_op = st.sidebar.file_uploader("📤 Cargar Operaciones CSV", type="csv")
if sub_op:
    df_op = pd.read_csv(sub_op)
    if set(df_op.columns).issubset(set(st.session_state.ops.columns)):
        st.session_state.ops = df_op
        st.session_state.ops.to_csv(OPERACIONES_FILE, index=False)
        st.sidebar.success("Operaciones cargadas correctamente")
    else:
        st.sidebar.error("Columnas inválidas en Operaciones")

# === FILTRAR DATOS ===
df_aportes = st.session_state.aportaciones.query("Fondo == @fondo")
df_ops = st.session_state.ops.query("Fondo == @fondo")

# === RENDIMIENTO POR SOCIO ===
st.subheader("👥 Rendimiento por Socio")
df_aportes = st.session_state.aportaciones.query("Fondo == @fondo")

# Asegurar que Monto sea numérico
df_aportes["Monto"] = pd.to_numeric(df_aportes["Monto"], errors="coerce")

# Filtrar aportes y retiros
aportes = df_aportes[df_aportes["Tipo"] == "Aporte"].groupby("Socio")["Monto"].sum()
retiros = df_aportes[df_aportes["Tipo"] == "Retiro"].groupby("Socio")["Monto"].sum()

# Capital neto
capital_neto = (aportes - retiros).fillna(0).astype(float)

# Participación
total_capital = capital_neto.sum()
participacion = capital_neto / total_capital

# Preparar operaciones del fondo
ops_fondo = st.session_state.ops.query("Fondo == @fondo").copy()
cols_to_numeric = ["TP_usd", "SL_usd", "Comisiones"]
for col in cols_to_numeric:
    ops_fondo[col] = pd.to_numeric(ops_fondo[col], errors="coerce")

# Calcular PnL
ops_fondo["PnL"] = 0.0
ops_fondo.loc[ops_fondo["Resultado"] == "Ganadora", "PnL"] = ops_fondo["TP_usd"] - ops_fondo["Comisiones"]
ops_fondo.loc[ops_fondo["Resultado"] == "Perdedora", "PnL"] = -ops_fondo["SL_usd"] - ops_fondo["Comisiones"]
gan_perd = ops_fondo.query("Resultado != 'Abierta'")
ganancia_total = gan_perd["PnL"].sum()

ganancia_socios = pd.to_numeric(ganancia_socios, errors="coerce")
capital_neto = pd.to_numeric(capital_neto, errors="coerce").replace(0, pd.NA)

rendimiento_pct = ((ganancia_socios / capital_neto) * 100).astype(float).round(2)

# Tabla resumen
df_rend = pd.DataFrame({
    "Capital Neto USD": capital_neto.round(2),
    "Participación %": (participacion * 100).round(2),
    "Ganancia Estimada USD": ganancia_socios.round(2),
    "Rendimiento %": rendimiento_pct
})

st.dataframe(df_rend, use_container_width=True)

# Gráfico de pastel
fig = px.pie(df_rend, values="Capital Neto USD", names=df_rend.index, title="Participación en el Fondo")
st.plotly_chart(fig, use_container_width=True)
# === FORMULARIO MOVIMIENTO DE CAPITAL ===
st.subheader("💰 Movimientos de Capital (Socios)")
with st.form("form_aporte"):
    col1, col2, col3, col4 = st.columns(4)
    socio = col1.text_input("Socio")
    cedula = col2.text_input("Cédula/ID")
    tipo = col3.selectbox("Tipo", ["Aporte", "Retiro"])
    monto = col4.number_input("Monto USD", step=100.0)
    fecha = st.date_input("Fecha", value=datetime.today())
    if st.form_submit_button("Guardar"):
        nuevo_idx = len(st.session_state.aportaciones)
        nueva = {"idx": nuevo_idx, "Fondo": fondo, "Socio": socio, "Cedula": cedula, "Fecha": fecha.strftime("%Y-%m-%d"), "Tipo": tipo, "Monto": monto}
        st.session_state.aportaciones = pd.concat([st.session_state.aportaciones, pd.DataFrame([nueva])], ignore_index=True)
        st.session_state.aportaciones.to_csv(APORTES_FILE, index=False)
        st.success("Movimiento registrado ✔️")
        st.rerun()

st.dataframe(df_aportes.sort_values("Fecha", ascending=False), use_container_width=True)

# === FORMULARIO NUEVA OPERACIÓN ===
st.subheader("➕ Registrar Nueva Operación")
with st.form("form_op"):
    col1, col2, col3 = st.columns(3)
    fecha = col1.date_input("Fecha", value=datetime.today())
    moneda = col2.text_input("Moneda")
    estrategia = col3.selectbox("Estrategia", ["spot", "futuros", "scalping", "swing"])

    col4, col5, col6 = st.columns(3)
    broker = col4.text_input("Broker")
    valor = col5.number_input("Valor Posición", step=10.0)
    comisiones = col6.number_input("Comisiones", step=1.0)

    col7, col8, col9 = st.columns(3)
    tp = col7.number_input("TP %", step=0.1)
    sl = col8.number_input("SL %", step=0.1)
    resultado = col9.selectbox("Resultado", ["Abierta", "Ganadora", "Perdedora"])

    tp_usd = valor * tp / 100
    sl_usd = valor * sl / 100

    if st.form_submit_button("Registrar Operación"):
        nuevo_idx = len(st.session_state.ops)
        nueva = {"idx": nuevo_idx, "ID": f"{usuario.upper()}-{nuevo_idx}", "Fondo": fondo, "Fecha": fecha.strftime("%Y-%m-%d"),
                 "Moneda": moneda, "Estrategia": estrategia, "Broker": broker, "Valor_Pos": valor,
                 "TP_%": tp, "SL_%": sl, "Comisiones": comisiones, "TP_usd": tp_usd, "SL_usd": sl_usd, "Resultado": resultado}
        st.session_state.ops = pd.concat([st.session_state.ops, pd.DataFrame([nueva])], ignore_index=True)
        st.session_state.ops.to_csv(OPERACIONES_FILE, index=False)
        st.success("Operación registrada ✔️")
        st.rerun()

st.dataframe(df_ops.sort_values("Fecha", ascending=False), use_container_width=True)

# === GRAFICAS ===
st.subheader("📊 Análisis Visual")
col1, col2 = st.columns(2)
with col1:
    fig1 = px.histogram(ops_fondo, x="PnL", nbins=20, title="Histograma de PnL")
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    fig2 = px.pie(ops_fondo.query("Resultado != 'Abierta'"), names="Resultado", title="Ganadoras vs Peredoras")
    st.plotly_chart(fig2, use_container_width=True)

# === FUNCIONES EXTRA ===
if rol == "admin":
    st.markdown("---")
    st.subheader("⚙️ Edición y Eliminación (Admin)")

    st.markdown("### Aportaciones")
    for i, row in df_aportes.iterrows():
        col1, col2, col3 = st.columns([5, 2, 1])
        col1.write(row.to_dict())
        if col2.button("Eliminar", key=f"del_ap_{i}"):
            st.session_state.aportaciones = st.session_state.aportaciones.drop(row.name)
            st.session_state.aportaciones.to_csv(APORTES_FILE, index=False)
            st.rerun()

    st.markdown("### Operaciones")
    for i, row in df_ops.iterrows():
        col1, col2, col3 = st.columns([5, 2, 1])
        col1.write(row.to_dict())
        if col2.button("Eliminar", key=f"del_op_{i}"):
            st.session_state.ops = st.session_state.ops.drop(row.name)
            st.session_state.ops.to_csv(OPERACIONES_FILE, index=False)
            st.rerun()
