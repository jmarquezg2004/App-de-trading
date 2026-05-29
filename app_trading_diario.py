import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from io import BytesIO
import base64
from fpdf import FPDF
import requests
import yfinance as yf  # Para Acciones y ETFs con máxima fiabilidad

# Configuración inicial
st.set_page_config(page_title="Diario de Trading", layout="wide")

# === CONFIGURACIÓN DE FIREBASE (AUTENTICACIÓN Y BASE DE DATOS) ===
FIREBASE_WEB_API_KEY = "AIzaSyC52gIJJRTE1B4BqeUwDmaX2fWKS3sSw10"
FIRESTORE_URL = "https://firestore.googleapis.com/v1/projects/plataforma-de-inversiones/databases/(default)/documents"

# 👑 NUEVO ADMINISTRADOR ASIGNADO
ADMIN_EMAIL = "jmarquezg2004@gmail.com"

# --- AUTENTICACIÓN ---
def verificar_credenciales_firebase(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True, response.json()
        return False, response.json().get("error", {}).get("message", "Error")
    except Exception:
        return False, "Error de conexión"

# --- FIRESTORE (PERSISTENCIA TOTAL EN LA NUBE) ---
def cargar_documentos_firestore(coleccion):
    url = f"{FIRESTORE_URL}/{coleccion}"
    try:
        response = requests.get(url)
        if response.status_code == 200 and "documents" in response.json():
            lista_datos = []
            for doc in response.json()["documents"]:
                fields = doc.get("fields", {})
                item = {"id_documento": doc["name"].split("/")[-1]}
                for key, val in fields.items():
                    item[key] = list(val.values())[0]
                lista_datos.append(item)
            return pd.DataFrame(lista_datos)
    except Exception:
        pass
    return pd.DataFrame()

def guardar_documento_firestore(coleccion, datos):
    url = f"{FIRESTORE_URL}/{coleccion}"
    fields = {}
    for key, value in datos.items():
        if isinstance(value, (int, float)):
            fields[key] = {"doubleValue": float(value)}
        else:
            fields[key] = {"stringValue": str(value)}
    payload = {"fields": fields}
    requests.post(url, json=payload)

def eliminar_documento_firestore(coleccion, id_doc):
    url = f"{FIRESTORE_URL}/{coleccion}/{id_doc}"
    requests.delete(url)

# --- SISTEMA DE PRECIOS HÍBRIDO CONFIABLE (YAHOO FINANCE + COINGECKO) ---
def obtener_precio_realtime(ticker_simbolo):
    if not ticker_simbolo:
        return None
    
    simbolo = ticker_simbolo.lower().strip()
    
    # 1. RUTA CRIPTO (Si el ticker contiene '-usd', busca de forma dinámica en CoinGecko)
    if "-usd" in simbolo:
        id_cripto = simbolo.replace("-usd", "")
        diccionario_siglas = {"btc": "bitcoin", "eth": "ethereum", "sol": "solana", "ada": "cardano", "link": "chainlink"}
        if id_cripto in diccionario_siglas:
            id_cripto = diccionario_siglas[id_cripto]
            
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={id_cripto}&vs_currencies=usd"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if id_cripto in data:
                    return float(data[id_cripto]["usd"])
        except Exception:
            pass

    # 2. RUTA TRADICIONAL (Yahoo Finance para Acciones y ETFs)
    try:
        ticker_data = yf.Ticker(simbolo.upper())
        precio = ticker_data.fast_info.last_price
        if precio:
            return float(precio)
    except Exception:
        pass
        
    return None

# --- CONTROL DE ACCESO / LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.sidebar.title("🔒 Acceso Privado")
    user = st.sidebar.text_input("Correo Electrónico")
    pwd = st.sidebar.text_input("Contraseña", type="password")
    
    if st.sidebar.button("Entrar"):
        exito, resultado = verificar_credenciales_firebase(user, pwd)
        if exito:
            user_lower = user.lower().strip()
            if user_lower == ADMIN_EMAIL.lower():
                rol_usuario = "admin"
            else:
                rol_usuario = "operador"  # Cualquier otro correo ingresará como operador limitado
                
            st.session_state.update({
                "logged_in": True,
                "usuario": user_lower,
                "rol": rol_usuario,
                "fondo": "Arkez Invest"
            })
            st.rerun()
        else:
            st.sidebar.error("Credenciales incorrectas o usuario no registrado en Firebase ❌")
    st.stop()

if st.sidebar.button("Cerrar Sesión"):
    for key in ["logged_in", "usuario", "rol", "fondo"]:
        st.session_state.pop(key, None)
    st.rerun()

# Cargar Datos directamente desde Firebase
df_aportes = cargar_documentos_firestore("aportes")
df_ops = cargar_documentos_firestore("operaciones")

if df_aportes.empty:
    df_aportes = pd.DataFrame(columns=["id_documento", "Fondo", "Socio", "Cedula", "Fecha", "Tipo", "Monto"])
if df_ops.empty:
    df_ops = pd.DataFrame(columns=["id_documento", "ID", "Fondo", "Fecha", "Moneda", "Estrategia", "Broker", "Valor_Pos", "TP_%", "SL_%", "TP_usd", "SL_usd", "Comision", "Resultado", "Ticker_API"])

fondo_actual = st.session_state.fondo
rol = st.session_state.rol
usuario = st.session_state.usuario

fondos_disponibles = sorted(set(df_aportes["Fondo"]).union(df_ops["Fondo"])) if not df_aportes.empty or not df_ops.empty else ["Arkez Invest"]
if "Arkez Invest" not in fondos_disponibles:
    fondos_disponibles.append("Arkez Invest")

# Solo el Administrador configura nuevos fondos en la barra lateral
if rol == "admin":
    nuevo_fondo = st.sidebar.text_input("➕ Crear nuevo fondo")
    if st.sidebar.button("Agregar Fondo") and nuevo_fondo.strip():
        if nuevo_fondo not in fondos_disponibles:
            guardar_documento_firestore("aportes", {"Fondo": nuevo_fondo, "Socio": usuario, "Cedula": "", "Fecha": str(datetime.today().date()), "Tipo": "Aporte", "Monto": 0.0})
            st.success(f"Fondo '{nuevo_fondo}' creado ✔")
            st.rerun()

fondo = st.selectbox("Selecciona el fondo", fondos_disponibles, index=0 if fondo_actual not in fondos_disponibles else fondos_disponibles.index(fondo_actual))
st.session_state.fondo = fondo
st.markdown(f"**👤 {usuario}** — **Fondo:** {fondo} — **Rol:** {rol.upper()}")
st.markdown("---")

# === MOVIMIENTOS DE CAPITAL ===
st.subheader("💰 Movimientos de Capital (Socios)")
with st.form("form_aporte"):
    c1, c2, c3, c4 = st.columns(4)
    socio = c1.text_input("Socio")
    cedula = c2.text_input("Cédula")
    tipo = c3.selectbox("Tipo", ["Aporte", "Retiro"])
    monto = c4.number_input("Monto", step=0.01)
    fecha = st.date_input("Fecha", value=datetime.today())
    if st.form_submit_button("Guardar Movimiento"):
        guardar_documento_firestore("aportes", {
            "Fondo": fondo, "Socio": socio, "Cedula": cedula, 
            "Fecha": str(fecha), "Tipo": tipo, "Monto": float(monto)
        })
        st.success("Movimiento guardado con éxito ✔")
        st.rerun()

df_aportes_fondo = df_aportes[df_aportes["Fondo"] == fondo] if not df_aportes.empty else pd.DataFrame()
if not df_aportes_fondo.empty:
    st.dataframe(df_aportes_fondo.sort_values("Fecha", ascending=False), use_container_width=True)
    if rol == "admin" and st.button("🗑 Eliminar último movimiento"):
        id_a_borrar = df_aportes_fondo.sort_values("Fecha").iloc[-1]["id_documento"]
        eliminar_documento_firestore("aportes", id_a_borrar)
        st.rerun()

# === REGISTRAR OPERACIÓN ===
st.subheader("📌 Registrar Nueva Operación")
with st.form("form_op"):
    c1, c2, c3 = st.columns(3)
    fecha_op = c1.date_input("Fecha", value=datetime.today())
    moneda = c2.text_input("Nombre del Activo (ej. Bitcoin o Nubank)")
    estrategia = c3.selectbox("Estrategia", ["Spot", "Futuros", "Staking", "Holding", "Arbitraje", "Bot o Copy Trading", "Farming", "Launchpool", "ICO"])

    c4, c5, c6 = st.columns(3)
    broker = c4.text_input("Broker / Exchange")
    valor_pos = c5.number_input("Valor Posición (USD)", step=0.01)
    comision = c6.number_input("Comisión USD", step=0.01)

    c7, c8, c9 = st.columns(3)
    tp_pct = c7.number_input("TP %")
    sl_pct = c8.number_input("SL %")
    resultado = c9.selectbox("Resultado", ["Abierta", "Ganadora", "Perdedora"])
    
    ticker_api = st.text_input("Ticker para API (ej. 'NU' o 'VRT' para acciones | 'bitcoin-usd' o 'solana-usd' para criptos)")

    tp_usd = valor_pos * tp_pct / 100
    sl_usd = valor_pos * sl_pct / 100

    if st.form_submit_button("Guardar Operación"):
        new_id = float(df_ops["ID"].max() + 1 if not df_ops.empty and "ID" in df_ops.columns else 1)
        guardar_documento_firestore("operaciones", {
            "ID": new_id, "Fondo": fondo, "Fecha": str(fecha_op), "Moneda": moneda,
            "Estrategia": estrategia, "Broker": broker, "Valor_Pos": float(valor_pos),
            "TP_%": float(tp_pct), "SL_%": float(sl_pct), "TP_usd": float(tp_usd),
            "SL_usd": float(sl_usd), "Comision": float(comision), "Resultado": resultado,
            "Ticker_API": ticker_api
        })
        st.success("Operación guardada con éxito ✔")
        st.rerun()

df_ops_fondo = df_ops[df_ops["Fondo"] == fondo] if not df_ops.empty else pd.DataFrame()
if not df_ops_fondo.empty:
    
    if st.button("🔄 Consultar Cotizaciones en Tiempo Real (Híbrido Yahoo/Gecko)"):
        st.markdown("### 📈 Precios del Mercado:")
        tickers_unicos = df_ops_fondo["Ticker_API"].dropna().unique()
        for t in tickers_unicos:
            if t.strip():
                precio = obtener_precio_realtime(t)
                if precio:
                    st.success(f"Activo: **{t.upper()}** ➔ Precio Actual: **${precio:,.2f} USD**")
                else:
                    st.warning(f"No se pudo consultar el ticker: **{t}**. Recuerda usar '-usd' para criptos.")

    st.dataframe(df_ops_fondo.sort_values("Fecha", ascending=False), use_container_width=True)
    if rol == "admin" and st.button("🗑 Eliminar última operación"):
        id_op_borrar = df_ops_fondo.sort_values("Fecha").iloc[-1]["id_documento"]
        eliminar_documento_firestore("operaciones", id_op_borrar)
        st.rerun()

# === RESUMEN GENERAL ===
st.subheader("📊 Resumen del Fondo")
if not df_ops_fondo.empty:
    capital_neto = pd.to_numeric(df_aportes_fondo["Monto"], errors="coerce").sum() if not df_aportes_fondo.empty else 0.0
    ops_cerradas = df_ops_fondo[df_ops_fondo["Resultado"] != "Abierta"].copy()
    
    if not ops_cerradas.empty:
        ops_cerradas["PnL"] = 0.0
        ops_cerradas["TP_usd"] = pd.to_numeric(ops_cerradas["TP_usd"], errors="coerce").fillna(0.0)
        ops_cerradas["SL_usd"] = pd.to_numeric(ops_cerradas["SL_usd"], errors="coerce").fillna(0.0)
        ops_cerradas["Comision"] = pd.to_numeric(ops_cerradas["Comision"], errors="coerce").fillna(0.0)
        
        ops_cerradas.loc[ops_cerradas["Resultado"] == "Ganadora", "PnL"] = ops_cerradas["TP_usd"] - ops_cerradas["Comision"]
        ops_cerradas.loc[ops_cerradas["Resultado"] == "Perdedora", "PnL"] = -ops_cerradas["SL_usd"] - ops_cerradas["Comision"]

        ganancia_total = ops_cerradas["PnL"].sum()
        rendimiento_pct = (ganancia_total / capital_neto * 100) if capital_neto > 0 else 0.0
        
        color_rend = "green" if rendimiento_pct >= 0 else "red"
        st.markdown(f"### Rendimiento del Fondo: <span style='color:{color_rend}'>**{rendimiento_pct:.2f}%**</span>", unsafe_allow_html=True)
