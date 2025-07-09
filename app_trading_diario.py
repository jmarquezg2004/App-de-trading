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
    st.sidebar.title("\U0001F512 Acceso Privado")
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
    st.sidebar.subheader("\U0001F3E6 Fondos")
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
st.title("\U0001F4C8 Diario & Gestor de Fondos de Inversión")
st.markdown(f"**\U0001F464 {usuario}** — **Fondo:** {fondo}")

# Botones de descarga CSV
st.sidebar.markdown("---")
buf_ap = io.StringIO()
st.session_state.aportaciones.to_csv(buf_ap, index=False)
st.sidebar.download_button("\U0001F4C5 Descargar Aportaciones CSV", buf_ap.getvalue(), "aportaciones.csv", "text/csv")

buf_op = io.StringIO()
st.session_state.ops.to_csv(buf_op, index=False)
st.sidebar.download_button("\U0001F4C5 Descargar Operaciones CSV", buf_op.getvalue(), "operaciones.csv", "text/csv")

# Botones de carga CSV
st.sidebar.markdown("---")
sub_ap = st.sidebar.file_uploader("\U0001F4C4 Cargar Aportaciones CSV", type="csv")
if sub_ap:
    df_ap = pd.read_csv(sub_ap)
    if set(df_ap.columns).issubset(set(st.session_state.aportaciones.columns)):
        st.session_state.aportaciones = df_ap
        st.session_state.aportaciones.to_csv(APORTES_FILE, index=False)
        st.sidebar.success("Aportaciones cargadas correctamente")
    else:
        st.sidebar.error("Columnas inválidas en Aportaciones")

sub_op = st.sidebar.file_uploader("\U0001F4C4 Cargar Operaciones CSV", type="csv")
if sub_op:
    df_op = pd.read_csv(sub_op)
    if set(df_op.columns).issubset(set(st.session_state.ops.columns)):
        st.session_state.ops = df_op
        st.session_state.ops.to_csv(OPERACIONES_FILE, index=False)
        st.sidebar.success("Operaciones cargadas correctamente")
    else:
        st.sidebar.error("Columnas inválidas en Operaciones")

# -------------------------------------------------
# VISUALIZACIÓN DE RENDIMIENTO POR SOCIO
# -------------------------------------------------
st.subheader("\U0001F4CA Rendimiento por Socio")
df_aportes = st.session_state.aportaciones.copy()
df_ops = st.session_state.ops.copy()

# Solo del fondo actual
df_aportes = df_aportes[df_aportes["Fondo"] == fondo]
df_ops = df_ops[df_ops["Fondo"] == fondo]

# Calcular capital neto por socio
aportes = df_aportes.groupby("Socio").apply(lambda x: x.query("Tipo == 'Aporte'")["Monto"].sum()).rename("Aportes")
retiros = df_aportes.groupby("Socio").apply(lambda x: x.query("Tipo == 'Retiro'")["Monto"].sum()).rename("Retiros")
neto = pd.concat([aportes, retiros], axis=1).fillna(0)
neto["Capital Neto"] = neto["Aportes"] - neto["Retiros"]

# Calcular G/P acumulado general
df_ops = df_ops.copy()
df_ops["PnL"] = 0.0
df_ops.loc[df_ops["Resultado"] == "Ganadora", "PnL"] = df_ops["TP_usd"] - df_ops["Comisiones"]
df_ops.loc[df_ops["Resultado"] == "Perdedora", "PnL"] = -df_ops["SL_usd"] - df_ops["Comisiones"]
total_ganancia = df_ops.query("Resultado != 'Abierta'")["PnL"].sum()

# Calcular proporción de ganancia por socio (según capital neto)
total_neto = neto["Capital Neto"].sum()
neto["% Participación"] = neto["Capital Neto"] / total_neto
neto["G/P Asignado"] = neto["% Participación"] * total_ganancia
neto["Total Final"] = neto["Capital Neto"] + neto["G/P Asignado"]
neto["Rendimiento %"] = (neto["Total Final"] - neto["Capital Neto"]) / neto["Capital Neto"] * 100

st.dataframe(neto.reset_index()[["Socio", "Capital Neto", "% Participación", "G/P Asignado", "Total Final", "Rendimiento %"]], use_container_width=True)

fig = px.pie(neto.reset_index(), names="Socio", values="Total Final", title="Distribución del Fondo por Socio")
st.plotly_chart(fig, use_container_width=True)

