import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io
import base64

# ---------------------- CONFIGURACIÓN BÁSICA ---------------------- #
st.set_page_config(page_title="Diario de Trading", layout="wide")

# ------------------------- AUTENTICACIÓN ------------------------- #
#  (para demo: usuario=admin / contraseña=admin123)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.sidebar.title("🔒 Acceso Privado")
    user = st.sidebar.text_input("Usuario")
    pwd = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Entrar"):
        if user == "admin" and pwd == "admin123":
            st.session_state.logged_in = True
            st.sidebar.success("Credenciales correctas ✔️")
        else:
            st.sidebar.error("Credenciales incorrectas ❌")
    st.stop()

if not st.session_state.logged_in:
    login_page()

# --------------------- BASE DE DATOS EN MEMORIA ------------------- #
COLUMNS = [
    'Fecha', 'Estrategia', 'Broker', 'Capital_Inicial', 'Valor_Posicion',
    'TP', 'SL', 'Resultado'
]

if 'records' not in st.session_state:
    st.session_state.records = pd.DataFrame(columns=COLUMNS)

df = st.session_state.records

# -------------------- ENCABEZADO & DATOS DEL FONDO --------------- #
st.title("📈 Diario & Gestor de Fondo de Inversión")
col_fondo, col_inv = st.columns(2)
with col_fondo:
    nombre_fondo = st.text_input("Nombre del Fondo", "Arkez Invest", key="fondo")
with col_inv:
    nombre_inv = st.text_input("Nombre del Inversionista", "José", key="inversor")

st.markdown("---")

# ---------------------- FORMULARIO DE REGISTRO -------------------- #
st.subheader("➕ Registrar Nueva Posición")

with st.form("registro_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        fecha = st.date_input("Fecha", datetime.today())
    with c2:
        estrategia = st.selectbox(
            "Estrategia",
            ["spot", "futuros", "staking", "holding", "ICO", "pool_liquidez", "farming"],
        )
    with c3:
        broker = st.text_input("Broker / Exchange")

    c4, c5, c6 = st.columns(3)
    with c4:
        capital = st.number_input("Capital Inicial (USD)", min_value=0.0, step=0.01)
    with c5:
        valor = st.number_input("Valor Posición (USD)", min_value=0.0, step=0.01)
    with c6:
        resultado = st.selectbox("Resultado", ["Abierta", "Ganadora", "Perdedora"])

    c7, c8 = st.columns(2)
    with c7:
        tp = st.number_input("Take Profit (USD)", min_value=0.0, step=0.01)
    with c8:
        sl = st.number_input("Stop Loss (USD)", min_value=0.0, step=0.01)

    submitted = st.form_submit_button("Guardar Registro")
    if submitted:
        new = {
            'Fecha': pd.to_datetime(fecha),
            'Estrategia': estrategia,
            'Broker': broker,
            'Capital_Inicial': capital,
            'Valor_Posicion': valor,
            'TP': tp,
            'SL': sl,
            'Resultado': resultado,
        }
        st.session_state.records = pd.concat(
            [st.session_state.records, pd.DataFrame([new])], ignore_index=True
        )
        st.success("Registro añadido correctamente ✔️")

st.markdown("---")

# --------------------------- FILTROS ------------------------------ #
st.subheader("🔍 Filtros")

if df.empty:
    st.info("Aún no hay registros de posiciones.")
    st.stop()

colf1, colf2, colf3 = st.columns(3)
with colf1:
    fecha_desde = st.date_input("Desde", df['Fecha'].min().date())
    fecha_hasta = st.date_input("Hasta", df['Fecha'].max().date())
with colf2:
    brokers_sel = st.multiselect(
        "Broker / Exchange", sorted(df['Broker'].dropna().unique()),
        default=list(df['Broker'].dropna().unique()),
    )
with colf3:
    estr_sel = st.multiselect(
        "Estrategia", sorted(df['Estrategia'].unique()),
        default=list(df['Estrategia'].unique()),
    )

mask = (
    (df['Fecha'] >= pd.to_datetime(fecha_desde))
    & (df['Fecha'] <= pd.to_datetime(fecha_hasta))
    & (df['Broker'].isin(brokers_sel))
    & (df['Estrategia'].isin(estr_sel))
)

filtered = df[mask].copy()

# ------------------------- TABLA DETALLADA ------------------------- #
st.subheader("📄 Posiciones Filtradas")
st.dataframe(filtered, use_container_width=True)

# --------------------------- RESUMEN ------------------------------- #
filtered['PnL'] = filtered['Valor_Posicion'] - filtered['Capital_Inicial']
cap_init_sum = filtered['Capital_Inicial'].sum()
pnl_sum = filtered['PnL'].sum()

total_usd = cap_init_sum + pnl_sum
rend_pct = (pnl_sum / cap_init_sum * 100) if cap_init_sum else 0

cA, cB, cC, cD = st.columns(4)
cA.metric("Capital Inicial", f"${cap_init_sum:,.2f}")
cB.metric("Ganancia / Pérdida", f"${pnl_sum:,.2f}")
cC.metric("Total USD", f"${total_usd:,.2f}")
cD.metric("Rend. Acum.", f"{rend_pct:.2f}%")

# ------------------------ GRÁFICA DE FONDO ------------------------- #
filtered.sort_values('Fecha', inplace=True)
filtered['Equity_Diaria'] = filtered['PnL'].cumsum() + filtered['Capital_Inicial'].cumsum()
fig = px.line(filtered, x='Fecha', y='Equity_Diaria', title='Evolución del Fondo')
fig.update_layout(xaxis_title='', yaxis_title='Equity (USD)')
st.plotly_chart(fig, use_container_width=True)

# ------------------------- DESCARGA CSV ---------------------------- #
@st.cache_data
def convert_df(df_):
    return df_.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered)
b64 = base64.b64encode(csv).decode()
download_link = f'<a href="data:file/csv;base64,{b64}" download="diario_trading.csv">📥 Descargar CSV</a>'
st.markdown(download_link, unsafe_allow_html=True)

# --------------------------- THANKS ------------------------------- #
st.markdown("""<br><hr style='border:1px solid #eee'>
<center><sub>Creado con ❤ usando Streamlit · 2025</sub></center>""", unsafe_allow_html=True)
