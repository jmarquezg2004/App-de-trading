import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from pathlib import Path

# =============================================================
# CONFIGURACIÓN GLOBAL
# =============================================================
st.set_page_config(page_title="Diario de Trading", layout="wide")

PRIMARY_BLUE = "#0F2E46"        # azul oscuro logo Arkez
PRIMARY_BLUE_L = "#27425C"      # 50 % más claro
YELLOW       = "#C5A15C"        # dorado logo Arkez
BG_GRADIENT  = "linear-gradient(135deg,#e9edf3 0%,#d5dde7 100%)"

st.markdown(
    f"""
    <style>
        html, body, [class*='st-'] {{ background: {BG_GRADIENT}!important; }}
        h1 {{ background:{PRIMARY_BLUE_L}; color:{YELLOW}; padding:12px 18px; border-radius:8px; }}
        h2, h3 {{ background:{PRIMARY_BLUE_L}; color:{YELLOW}; padding:6px 12px; border-radius:6px; margin-top:1.3rem; }}
        div[data-testid='metric-container'] {{ background:white; border:1px solid #ccd; padding:8px; border-radius:8px; }}
    </style>
    """,
    unsafe_allow_html=True
)

# =============================================================
# USUARIOS Y FONDOS
# =============================================================
USUARIOS = {
    "admin": {"pwd":"admin123","fondo":"Arkez Invest","rol":"admin"},
    "juan" : {"pwd":"juan123", "fondo":"Cripto Alpha","rol":"lector"},
}
DEFAULT_FONDOS = ["Arkez Invest","Cripto Alpha"]

if "init" not in st.session_state:
    st.session_state.init=True
    st.session_state.logged_in=False
    st.session_state.usuario=None
    st.session_state.rol=None
    st.session_state.fondos=DEFAULT_FONDOS.copy()
    st.session_state.fondo=DEFAULT_FONDOS[0]
    st.session_state.aportaciones=pd.DataFrame(columns=["Fondo","Socio","Cedula","Fecha","Tipo","Monto"])
    st.session_state.ops=pd.DataFrame(columns=["ID","Fondo","Fecha","Moneda","Estrategia","Broker","Valor_Pos","TP_%","SL_%","Comisiones","TP_usd","SL_usd","Resultado"])

# ---------------- LOGIN ---------------

def login_ui():
    st.sidebar.title("🔒 Acceso Privado")
    u=st.sidebar.text_input("Usuario")
    p=st.sidebar.text_input("Contraseña",type="password")
    if st.sidebar.button("Entrar"):
        if u in USUARIOS and USUARIOS[u]["pwd"]==p:
            st.session_state.update({
                "logged_in":True,
                "usuario":u,
                "rol":USUARIOS[u]["rol"],
                "fondo":USUARIOS[u]["fondo"]
            })
            st.rerun()
        else:
            st.sidebar.error("Credenciales incorrectas ❌")

if not st.session_state.logged_in:
    login_ui()
    st.stop()

usuario=st.session_state.usuario
rol=st.session_state.rol
fondo=st.session_state.fondo

# ---------------- SIDEBAR -------------
logo_path=Path("arkez_logo.png")
if logo_path.exists():
    st.sidebar.image(str(logo_path),width=160)
else:
    st.sidebar.write("[Sube arkez_logo.png]")

if rol=="admin":
    st.sidebar.subheader("🏦 Fondos")
    seleccion=st.sidebar.selectbox("Fondo",st.session_state.fondos,index=st.session_state.fondos.index(fondo))
    if seleccion!=fondo:
        st.session_state.fondo=seleccion
        st.rerun()
    nuevo=st.sidebar.text_input("Nuevo fondo")
    if st.sidebar.button("Agregar") and nuevo.strip():
        if nuevo not in st.session_state.fondos:
            st.session_state.fondos.append(nuevo)
            st.session_state.fondo=nuevo
            st.rerun()
        else:
            st.sidebar.warning("Ya existe")

# ---------------- TITULO --------------
st.title("📈 Diario & Gestor de Fondos de Inversión")
st.markdown(f"**👤 {usuario}** — **Fondo:** {fondo}")

# ---------------- APORTES -------------
if rol=="admin":
    st.header("Movimientos de Capital (Socios)")
    with st.form("apo"):
        c1,c2,c3,c4=st.columns(4)
        socio=c1.text_input("Socio")
        ced=c2.text_input("Cédula")
        tipo=c3.selectbox("Tipo",["Aporte","Retiro"])
        monto=c4.number_input("Monto",min_value=0.0,step=0.01)
        fecha=st.date_input("Fecha",datetime.today())
        if st.form_submit_button("Guardar"):
            st.session_state.aportaciones=pd.concat([
                st.session_state.aportaciones,
                pd.DataFrame([{"Fondo":fondo,"Socio":socio,"Cedula":ced,"Fecha":fecha,"Tipo":tipo,"Monto":monto}])
            ],ignore_index=True)
            st.success("Guardado")
            st.rerun()
    st.dataframe(st.session_state.aportaciones.query("Fondo==@fondo"),use_container_width=True)

# ---------------- OPERACIONES ---------
if rol=="admin":
    st.header("Registrar Nueva Operación")
    with st.form("op"):
        c1,c2,c3=st.columns(3)
        fech=c1.date_input("Fecha",datetime.today())
        mon=c2.text_input("Moneda","BTC")
        est=c3.selectbox("Estrategia",["spot","futuros","staking","holding","ICO","pool_liquidez","farming"])
        c4,c5=st.columns(2)
        bro=c4.text_input("Broker")
        val=c5.number_input("Valor USD",min_value=0.0,step=0.01)
        c6,c7,c8,c9=st.columns(4)
        tp=c6.number_input("TP %",min_value=0.0,step=0.1)
        sl=c7.number_input("SL %",min_value=0.0,step=0.1)
        com=c8.number_input("Comisiones",min_value=0.0,step=0.01)
        res=c9.selectbox("Resultado",["Abierta","Ganadora","Perdedora"])
        tp_usd=val*tp/100-com
        sl_usd=val*sl/100+com
        st.markdown(f"TP neto **${tp_usd:,.2f}** | SL neto **${sl_usd:,.2f}**")
        if st.form_submit_button("Guardar"):
            oid=len(st.session_state.ops)+1
            st.session_state.ops=pd.concat([
                st.session_state.ops,
                pd.DataFrame([{"ID":oid,"Fondo":fondo,"Fecha":fech,"Moneda":mon,"Estrategia":est,"Broker":bro,"Valor_Pos":val,"TP_%":tp,"SL_%":sl,"Comisiones":com,"TP_usd":tp_usd,"SL_usd":sl_usd,"Resultado":res}])
            ],ignore_index=True)
            st.success("Operación guardada")
            st.rerun()

# ---------------- FILTRO Y TABLA ------
st.header("Operaciones")
ops=st.session_state.ops.query("Fondo==@fondo")
if ops.empty:
    st.info("Sin operaciones")
    st.stop()

c1,c2,c3=st.columns(3)
from_date=c1.date_input("Desde",ops["Fecha"].min().date())
to_date=c1.date_input("Hasta",ops["Fecha"].max().date())
sel_b=c2.multiselect("Broker",sorted(ops["Broker"].unique()),default=list(ops["Broker"].unique()))
sel_e=c3.multiselect("Estrategia",sorted(ops["Estrategia"].unique()),default=list(ops["Estrategia"].unique()))

mask=(
    (ops["Fecha"]>=pd.to_datetime(from_date)) &
    (ops["Fecha"]<=pd.to_datetime(to_date)) &
    (ops["Broker"].isin(sel_b)) &
    (ops["Estrategia"].isin(sel_e))
)
ops_f=ops[mask]

st.dataframe(ops_f.sort_values("Fecha",ascending=False),use_container_width=True)

# ---------------- KPIs Y GRÁFICA -------
st.header("Resumen del Fondo")

aport=st.session_state.aportaciones.query("Fondo==@fondo")
cap_in=aport.query("Tipo=='Aporte'")["Monto"].sum()
cap_out=aport.query("Tipo=='Retiro'")["Monto"].sum()
cap_neto=cap_in-cap_out

ops_cerradas=ops.query("Resultado!='Abierta'").copy()
ops_cerradas["PnL"]=ops_cerradas.apply(lambda r: r["TP_usd"] if r["Resultado"]=="Ganadora" else -r["SL_usd"],axis=1)

 pnl_total=ops_cerradas["PnL"].sum()
cap_total=cap_neto+pnl_total
rend_pct=(pnl_total/cap_neto*100) if cap_neto else 0

m1,
