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

    # Cargar datos desde CSV o iniciar vacíos
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

# === CÁLCULO DE RENDIMIENTO POR SOCIO ===
st.subheader("👥 Rendimiento por Socio")
df_aportes = st.session_state.aportaciones.query("Fondo == @fondo")

# Filtramos aportes y retiros por socio
aportes = df_aportes[df_aportes["Tipo"] == "Aporte"].groupby("Socio")["Monto"].sum()
retiros = df_aportes[df_aportes["Tipo"] == "Retiro"].groupby("Socio")["Monto"].sum()

# Capital neto por socio
capital_neto_socios = (aportes - retiros).fillna(0)

# Participación de cada socio en el fondo
total_capital = capital_neto_socios.sum()
participacion = capital_neto_socios / total_capital

# Ganancia total del fondo
ops_fondo = st.session_state.ops.query("Fondo == @fondo")
ops_fondo = ops_fondo.copy()
ops_fondo["PnL"] = 0.0
ops_fondo.loc[ops_fondo["Resultado"] == "Ganadora", "PnL"] = ops_fondo["TP_usd"] - ops_fondo["Comisiones"]
ops_fondo.loc[ops_fondo["Resultado"] == "Perdedora", "PnL"] = -ops_fondo["SL_usd"] - ops_fondo["Comisiones"]
gan_perd = ops_fondo.query("Resultado != 'Abierta'")
ganancia_total = gan_perd["PnL"].sum()

# Ganancia estimada para cada socio
ganancia_socios = participacion * ganancia_total
rendimiento_pct_socios = (ganancia_socios / capital_neto_socios * 100).round(2)

# Mostramos la tabla
df_rend_socios = pd.DataFrame({
    "Capital Neto USD": capital_neto_socios.round(2),
    "Participación %": (participacion * 100).round(2),
    "Ganancia Estimada USD": ganancia_socios.round(2),
    "Rendimiento %": rendimiento_pct_socios
})

st.dataframe(df_rend_socios, use_container_width=True)

# Gráfico de pastel
fig_socios = px.pie(df_rend_socios, values="Capital Neto USD", names=df_rend_socios.index, title="Participación en el Fondo")
st.plotly_chart(fig_socios, use_container_width=True)

# === FORMULARIO: Movimiento de Capital ===
st.subheader("💰 Movimientos de Capital (Socios)")
with st.form("form_aporte"):
    col1, col2, col3, col4 = st.columns(4)
    socio   = col1.text_input("Socio")
    cedula  = col2.text_input("Cédula/ID")
    tipo    = col3.selectbox("Tipo", ["Aporte", "Retiro"])
    monto   = col4.number_input("Monto USD", step=100.0)
    fecha   = st.date_input("Fecha", value=datetime.today())
    if st.form_submit_button("Guardar"):
        nuevo_idx = len(st.session_state.aportaciones)
        nueva_fila = {
            "idx": nuevo_idx,
            "Fondo": fondo,
            "Socio": socio,
            "Cedula": cedula,
            "Fecha": fecha.strftime("%Y-%m-%d"),
            "Tipo": tipo,
            "Monto": monto
        }
        st.session_state.aportaciones = pd.concat([st.session_state.aportaciones, pd.DataFrame([nueva_fila])], ignore_index=True)
        st.session_state.aportaciones.to_csv(APORTES_FILE, index=False)
        st.success("Movimiento registrado ✔️")
        st.rerun()

# === FORMULARIO: Nueva Operación ===
st.subheader("➕ Registrar Nueva Operación")
with st.form("form_op"):
    col1, col2, col3 = st.columns(3)
    fecha     = col1.date_input("Fecha de la Operación", value=datetime.today())
    moneda    = col2.text_input("Moneda (ej. BTC)")
    estrategia= col3.selectbox("Estrategia", ["spot", "futuros", "scalping", "swing"])

    col4, col5, col6 = st.columns(3)
    broker     = col4.text_input("Broker / Exchange")
    valor_pos  = col5.number_input("Valor de la Posición", step=10.0)
    comisiones = col6.number_input("Comisiones", step=1.0)

    col7, col8, col9 = st.columns(3)
    tp_pct     = col7.number_input("TP %", step=0.1)
    sl_pct     = col8.number_input("SL %", step=0.1)
    resultado  = col9.selectbox("Resultado", ["Abierta", "Ganadora", "Perdedora"])

    tp_usd = valor_pos * tp_pct / 100
    sl_usd = valor_pos * sl_pct / 100

    if st.form_submit_button("Registrar Operación"):
        nuevo_idx = len(st.session_state.ops)
        nueva_op = {
            "idx": nuevo_idx,
            "ID": f"{usuario.upper()}-{nuevo_idx}",
            "Fondo": fondo,
            "Fecha": fecha.strftime("%Y-%m-%d"),
            "Moneda": moneda,
            "Estrategia": estrategia,
            "Broker": broker,
            "Valor_Pos": valor_pos,
            "TP_%": tp_pct,
            "SL_%": sl_pct,
            "Comisiones": comisiones,
            "TP_usd": tp_usd,
            "SL_usd": sl_usd,
            "Resultado": resultado
        }
        st.session_state.ops = pd.concat([st.session_state.ops, pd.DataFrame([nueva_op])], ignore_index=True)
        st.session_state.ops.to_csv(OPERACIONES_FILE, index=False)
        st.success("Operación registrada ✔️")
        st.rerun()
