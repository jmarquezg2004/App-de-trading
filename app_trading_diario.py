import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64

# ---------------------- CONFIGURACIÓN BÁSICA ---------------------- #
st.set_page_config(page_title="Diario de Trading", layout="wide")

# ---------------------- USUARIOS Y FONDOS ------------------------- #
USUARIOS = {
    "admin": {"pwd": "admin123", "fondo": "Arkez Invest", "rol": "admin"},
    "juan": {"pwd": "juan123", "fondo": "Cripto Alpha", "rol": "lector"},
    "maria": {"pwd": "maria123", "fondo": "Arkez Invest", "rol": "lector"},
}

# ------------------------- ESTADO DE SESIÓN ----------------------- #
for key, default in {
    "logged_in": False,
    "usuario_actual": None,
    "rol": None,
    "fondo_actual": "",
}.items():
    st.session_state.setdefault(key, default)

# ------------------------- AUTENTICACIÓN ------------------------- #

def login_page():
    """Formulario de acceso."""
    st.sidebar.title("🔒 Acceso Privado")
    user = st.sidebar.text_input("Usuario")
    pwd = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Entrar"):
        if user in USUARIOS and USUARIOS[user]["pwd"] == pwd:
            st.session_state.update({
                "logged_in": True,
                "usuario_actual": user,
                "rol": USUARIOS[user]["rol"],
                "fondo_actual": USUARIOS[user]["fondo"],
            })
            st.rerun()  # <— reemplaza experimental_rerun
        else:
            st.sidebar.error("Credenciales incorrectas ❌")
            st.stop()
    else:
        st.stop()

if not st.session_state.logged_in:
    login_page()

usuario = st.session_state.usuario_actual
rol = st.session_state.rol
nombre_fondo = st.session_state.fondo_actual

# --------------------- BASE DE DATOS EN MEMORIA ------------------- #
COLUMNS = [
    "Fondo",
    "Fecha",
    "Moneda",
    "Estrategia",
    "Broker",
    "Capital_Inicial",
    "Valor_Posicion",
    "TP",
    "SL",
    "Resultado",
]

st.session_state.setdefault("records", pd.DataFrame(columns=COLUMNS))
df = st.session_state.records

# -------------------- ENCABEZADO & DATOS DEL FONDO --------------- #
st.title("📈 Diario & Gestor de Fondos de Inversión")
st.markdown(f"**👤 Usuario:** `{usuario}` — Fondo asignado: **{nombre_fondo}**")

st.markdown("---")

# ---------------------- FORMULARIO DE REGISTRO -------------------- #
if rol == "admin":
    st.subheader("➕ Registrar Nueva Posición")

    with st.form("registro_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            fecha = st.date_input("Fecha", datetime.today())
        with c2:
            moneda = st.text_input("Moneda / Activo", "Bitcoin")
        with c3:
            estrategia = st.selectbox(
                "Estrategia",
                ["spot", "futuros", "staking", "holding", "ICO", "pool_liquidez", "farming"],
            )

        c4, c5, c6 = st.columns(3)
        with c4:
            broker = st.text_input("Broker / Exchange")
        with c5:
            capital = st.number_input("Capital Inicial (USD)", min_value=0.0, step=0.01)
        with c6:
            valor = st.number_input("Valor Posición (USD)", min_value=0.0, step=0.01)

        c7, c8, c9 = st.columns(3)
        with c7:
            tp = st.number_input("Take Profit (USD)", min_value=0.0, step=0.01)
        with c8:
            sl = st.number_input("Stop Loss (USD)", min_value=0.0, step=0.01)
        with c9:
            resultado = st.selectbox("Resultado", ["Abierta", "Ganadora", "Perdedora"])

        if st.form_submit_button("Guardar Registro"):
            nuevo = {
                "Fondo": nombre_fondo,
                "Fecha": pd.to_datetime(fecha),
                "Moneda": moneda,
                "Estrategia": estrategia,
                "Broker": broker,
                "Capital_Inicial": capital,
                "Valor_Posicion": valor,
                "TP": tp,
                "SL": sl,
                "Resultado": resultado,
            }
            st.session_state.records = pd.concat([st.session_state.records, pd.DataFrame([nuevo])], ignore_index=True)
            st.success("Registro añadido ✔️")
            st.rerun()  # <— reemplaza experimental_rerun

    st.markdown("---")

# --------------------------- FILTROS ------------------------------ #
st.subheader("🔍 Filtros")

filtros_df = df[df["Fondo"] == nombre_fondo]
if filtros_df.empty:
    st.info("Aún no hay registros de posiciones para este fondo.")
    st.stop()

colf1, colf2, colf3 = st.columns(3)
with colf1:
    fecha_desde = st.date_input("Desde", filtros_df["Fecha"].min().date())
    fecha_hasta = st.date_input("Hasta", filtros_df["Fecha"].max().date())
with colf2:
    brokers_sel = st.multiselect("Broker / Exchange", sorted(filtros_df["Broker"].dropna().unique()), default=list(filtros_df["Broker"].dropna().unique()))
with colf3:
    estr_sel = st.multiselect("Estrategia", sorted(filtros_df["Estrategia"].unique()), default=list(filtros_df["Estrategia"].unique()))

mask = (
    (filtros_df["Fecha"] >= pd.to_datetime(fecha_desde)) &
    (filtros_df["Fecha"] <= pd.to_datetime(fecha_hasta)) &
    (filtros_df["Broker"].isin(brokers_sel)) &
    (filtros_df["Estrategia"].isin(estr_sel))
)
filtered = filtros_df[mask].copy()

# ------------------------- TABLA DETALLADA ------------------------- #
st.subheader("📄 Posiciones Filtradas")
st.dataframe(filtered, use_container_width=True)

# --------------------------- RESUMEN ------------------------------- #
filtered["PnL"] = filtered["Valor_Posicion"] - filtered["Capital_Inicial"]
cap_init_sum = filtered["Capital_Inicial"].sum()
pnl_sum = filtered["PnL"].sum()

total_usd = cap_init_sum + pnl_sum
rend_pct = (pnl_sum / cap_init_sum * 100) if cap_init_sum else 0

cA, cB, cC, cD = st.columns(4)
cA.metric("Capital Inicial", f"${cap_init_sum:,.2f}")
cB.metric("Ganancia / Pérdida", f"${pnl_sum:,.2f}")
cC.metric("Total USD", f"${total_usd:,.2f}")
cD.metric("Rend. Acum.", f"{rend_pct:.2f}%")

# ------------------------ GRÁFICA DE FONDO ------------------------- #
filtered.sort_values("Fecha", inplace=True)
filtered["Equity_Diaria"] = filtered["PnL"].cumsum() + filtered["Capital_Inicial"].cumsum()
fig = px.line(filtered, x="Fecha", y="Equity_Diaria", title="Evolución del Fondo")
fig.update_layout(xaxis_title="", yaxis_title="Equity (USD)")
st.plotly_chart(fig, use_container_width=True)

# ------------------------- DESCARGA CSV ---------------------------- #
@st.cache_data
def convert_df(df_):
    return df_.to_csv(index=False).encode("utf-8")

csv = convert_df(filtered)
b64 = base64.b64encode(csv).decode()
st.markdown(f'<a href="data:file/csv;base64,{b64}" download="diario_trading.csv">📥 Descargar CSV</a>', unsafe_allow_html=True)

# --------------------------- THANKS ------------------------------- #
st.markdown("<br><hr style='border:1px solid #eee'><center><sub>Creado con ❤ usando Streamlit · 2025</sub></center>", unsafe_allow_html=True)
