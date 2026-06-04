import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date
import requests
import time

st.set_page_config(page_title="Arkez — Plataforma", page_icon="⬡", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

/* Variables de tema — oscuro por defecto */
:root {
    --bg:         #111827;
    --sidebar-bg: #0D1929;
    --surface:    #162236;
    --surface2:   #0F1A2B;
    --border:     #1E3354;
    --text:       #ffffff;
    --muted:      #8BA5C8;
    --label:      #B0C4DC;
}
/* Tema claro */
body.tema-claro {
    --bg:         #F0F4F8;
    --sidebar-bg: #E2EAF4;
    --surface:    #FFFFFF;
    --surface2:   #EDF2F7;
    --border:     #C4D4E8;
    --text:       #1A2640;
    --muted:      #4A6080;
    --label:      #3A5070;
}

html, body { font-family: 'IBM Plex Sans', sans-serif; }
.stApp { background: var(--bg); color: var(--text); }
h1 { font-family:'IBM Plex Mono',monospace!important; color:#C8A84B!important; letter-spacing:2px; }
h2 { font-family:'IBM Plex Mono',monospace!important; font-size:11px!important; letter-spacing:1.5px; text-transform:uppercase; color:var(--muted)!important; }
h3 { font-family:'IBM Plex Mono',monospace!important; font-size:13px!important; color:#C8A84B!important; }
hr { border-color:var(--border)!important; }

section[data-testid="stSidebar"] { background:var(--sidebar-bg)!important; border-right:1px solid var(--border); }
section[data-testid="stSidebar"] label { color:var(--muted)!important; font-size:12px!important; }

/* TODOS los inputs */
input, textarea {
    background:var(--surface)!important; color:var(--text)!important;
    -webkit-text-fill-color:var(--text)!important;
    border:1px solid var(--border)!important; border-radius:6px!important;
    font-family:'IBM Plex Mono',monospace!important; font-size:13px!important;
    opacity:1!important;
}
input::placeholder, textarea::placeholder {
    color:#8BA5C8!important; -webkit-text-fill-color:#8BA5C8!important; opacity:1!important;
}
input:focus, textarea:focus { border-color:#C8A84B!important; }
input:disabled {
    color:#C8A84B!important; -webkit-text-fill-color:#C8A84B!important; opacity:1!important;
}

/* Selectbox */
[data-testid="stSelectbox"]>div>div {
    background:var(--surface)!important; border:1px solid var(--border)!important;
    border-radius:6px!important; color:var(--text)!important;
}
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] p { color:#ffffff!important; font-size:13px!important; }

/* Dropdown abierto */
[data-baseweb="popover"], [data-baseweb="popover"] *,
[data-baseweb="menu"], [data-baseweb="menu"] *,
[role="listbox"], [role="listbox"] * {
    background:var(--surface)!important; color:var(--text)!important;
    font-family:'IBM Plex Mono',monospace!important; font-size:13px!important;
    border-color:#2a4060!important;
}
[role="option"]:hover { background:#243b55!important; color:#C8A84B!important; }
[aria-selected="true"] { background:#1e3a5a!important; color:#C8A84B!important; }
[data-baseweb="select"] svg { fill:#8BA5C8!important; }

/* Labels */
[data-testid="stTextInput"] label, [data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label, [data-testid="stDateInput"] label,
[data-testid="stTextArea"] label, [data-testid="stRadio"]>label {
    color:#B0C4DC!important; font-size:13px!important; font-weight:500!important;
}

/* Number input buttons */
[data-testid="stNumberInput"] button {
    background:#1a3050!important; color:#ffffff!important; border-color:#2a4060!important;
}

/* Botones */
.stButton>button {
    background:linear-gradient(135deg,#C8A84B,#A07830)!important;
    color:#0D1929!important; border:none!important; border-radius:6px!important;
    font-family:'IBM Plex Mono',monospace!important; font-weight:600!important;
    letter-spacing:1px!important; text-transform:uppercase!important; font-size:12px!important;
}
.stButton>button:hover { filter:brightness(1.1)!important; }

/* Tabs */
[data-testid="stTabs"] button {
    font-family:'IBM Plex Mono',monospace!important; font-size:11px!important;
    letter-spacing:1px; text-transform:uppercase; color:#8BA5C8!important; background:transparent!important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color:#C8A84B!important; border-bottom:2px solid #C8A84B!important;
}

/* Métricas */
[data-testid="metric-container"] {
    background:var(--surface); border:1px solid var(--border); border-radius:10px;
    padding:16px!important; position:relative; overflow:hidden;
}
[data-testid="metric-container"]::before {
    content:''; position:absolute; top:0;left:0;right:0; height:2px;
    background:linear-gradient(90deg,#C8A84B,#A07830);
}
[data-testid="stMetricValue"] {
    font-family:'IBM Plex Mono',monospace!important; font-size:1.4rem!important;
    color:var(--text)!important; font-weight:600!important;
}
[data-testid="stMetricLabel"] {
    font-family:'IBM Plex Mono',monospace!important; font-size:0.68rem!important;
    letter-spacing:1.2px; text-transform:uppercase; color:#8BA5C8!important;
}

/* DataFrames */
[data-testid="stDataFrame"] { border:1px solid var(--border); border-radius:8px; overflow:hidden; }

/* Alerts */
[data-testid="stAlert"] {
    border-radius:8px!important; border-left-width:3px!important;
    background:var(--surface)!important; font-family:'IBM Plex Mono',monospace!important; color:#ffffff!important;
}

/* Form */
[data-testid="stForm"] {
    background:var(--bg)!important; border:1px solid var(--border)!important;
    border-radius:10px!important; padding:20px!important;
}

/* Radio */
[data-testid="stRadio"] label span,
[data-testid="stRadio"] label p,
[data-testid="stRadio"] p { color:#ffffff!important; font-weight:600!important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# CONSTANTES
# ══════════════════════════════════════════════════════
FIREBASE_KEY = "AIzaSyC52gIJJRTE1B4BqeUwDmaX2fWKS3sSw10"
FS_URL       = "https://firestore.googleapis.com/v1/projects/plataforma-de-inversiones/databases/(default)/documents"
ADMIN_EMAIL  = "jmarquezg2004@gmail.com"
CMC_KEY      = st.secrets.get("CMC_KEY", "d67913f039804c6b900905ebad7c1aaf")

CATEGORIAS = [
    "Acción", "ETF", "Cripto", "CDT", "Fondo", "Cuenta Remunerada",
    "Inmueble", "Negocio", "Ganadería", "Vehículo",
    "Dividendo", "Seguro", "Arriendo", "Otro",
]
CATS_MANUALES = {"Inmueble","Negocio","Ganadería","Vehículo","Dividendo","Seguro","Arriendo","Otro"}
CAT_CLR_MAP = {
    "Acción":"#C8A84B","ETF":"#2ECC87","Cripto":"#E87844",
    "CDT":"#6BA3BE","Fondo":"#9B8EC4","Cuenta Remunerada":"#F0C040",
    "Inmueble":"#E85555","Negocio":"#FF9F43","Ganadería":"#A29BFE",
    "Vehículo":"#55EFC4","Dividendo":"#FFEAA7","Seguro":"#74B9FF",
    "Arriendo":"#FD79A8","Otro":"#8BA5C8",
}
MODO_IND = "Portafolio Individual"
MODO_OBS = "Observador de Fondo"

# Logo Arkez oficial (sin INVEST) — base64 embebido
LOGO_B64    = "iVBORw0KGgoAAAANSUhEUgAAALQAAAA+CAYAAACC5jGMAAAABmJLR0QA/wD/AP+gvaeTAAALiklEQVR4nO2aeXRU1R3Hv7/7ZrKSkJAV3KhNwY2QBYoLpMHI5gLCMRAiFFCPqFjbI7Vw6rGOFbFabVH/sGLFVoRQaNEKHmyBJISABkQSkEUNSFsQAtlDlpn33v31j2SWJDOZCQQynnM/58wf77e9353ze/fd+7sPUCgUCoVCoVAoFAqFQqFQKBQKhUKhUCgUCoVCoVAoFAqFQqFQKBQKhUKhUCgUCoVCoVAoFAqFQqFQKBQKhUKhUCgUCoVCoVAoFAqFQqFQKBQKhUKhUCgUCoVCoVAoFArF94GS1XMGFxXkDe3vPBTBjaW/EwgYzXjRAooAMLO/U1EEL9TfCQTCjoK8dMH4HIBgUHZWfsGO/s5JEZyI/k4gEATjNXTkSpAr2Gb7XuStuPwEfWGUrJmVB2CcW0JppcOPzu+vfBTBTVAvOXavzw2XhnaYgaFdVFVWqQ27ec6axv7ISxG8BPWmUOraL5m6FTMAJDmEuRTAry9zSh3YRFJm6Y0mmyFkavJcrHEQxcVGIJ5jJs0YL0GaYLOOBYUwi0hAWojhIHADNFFVtmXjSb+BMjOtSU3iKuelw5A1dcf3NXgzjUnLjgHRNRbWYlmgqobqKrFvn+7UD7lp9FWmA9ZA8rdI4ThVWdYpv4TR2cmizRIRiL8Tq9TqTx76V21vfAIhaAt69/rcK0wDS3zpCVi8e3Xuqlvnbqi8nHkBQGJ66QcseaqAAAQjqUFbVQU8GIivyXJlXZO9ymRpFUKzWwgGCZIWEpIEQRDTyJxp53VDL2ppaHnvRHlxvbc4g+3WFLbySilCrCT1tlALNgN4pZNRdrYlrk57FcyPgBHCkICJ7SnNiXd5/mnSoL9waFg4E4USs91X7szSNExHC4BJnRS6eJs18+5Axu/EoZkrASzsjU8gBG1Bm7r2IgiRPZiEmBbLclzmNl5iRk4qmKd6yhiYl5yW/fyZ8uIT/vxb24zj9S32ie1Xek+m94LFI0mj77q7au/Hx70ZGFrYECbtWpDVDDHPf9RVH18nXmbwEy4BYR+12qdXVhZ2KlppDWmQWsjtHWPxg1zn16QfCcpNYcm6WRkg3O/XkDl3x5qZWZchJU+8zSoak/ZwIM6mlK59S2REePP1w649FhMdVQ1AdjMmXD8wDM9lZj7sdTnAzgmJoIHY9NTFjRw/g4EnPETfWKTlzuqvdjV1vw25ciKW35Dp+FiY9n96+xGbPT6FgULERX0RpytBN0Mzg0oLyNWm84dGYgXbbKPIZuteEH1MUurESGbT9aDFD4qpqa6tjwMABj+UkjLlucrKLT5f2QAAck+Ct6SPOLb69WWpHZd2aXKNXbfXLVyyDFtL99wIAE0tjuyo2KpcAGu7xyJXLCk11/gTUnPGSfD7ALQO0XcmyYk1Ff8+6ye1BqGf31l1eE9AyycXupxtF4bPNXioFvIHgOd7iHZVpSRswP5e3SUggq6gd63Lmw1gbKD2DKR3tPFWXbKknAiZD2AgAIRYLY5tBW/9J23SrLh2JSU0RtlnAljtJ4gvRajQaEi4Fjbk3T8+f27ozXeahmlqDsO8UgI3w1tBM1x9KuL2GTp52K2jdeJ/AAjvsKqXUkyuP1h4wt/wGNCJZa9r4tyh4vO+dElp46cxeJ6H6JQky0xs2GD68rkYgmrJsXt9bjgzlvfakbH8s/fvj74EKXWG3MuN2dOmfBE/KCbjJ2MyvnTnIRb1xW00QQlRAyJdRWIy++oguGdoaJw4fEwqh8AGIKFD3Coh7qk7uO1gYHemOAY5Lizr7sSnjh/OwF/hfOwYbYJpRvX+rd/11T26ElQztGGIpwi4xofahPsV2pVL3saLT58wiiEzndePL8jTAOA3v1jYmDO7o86Jx8SnTxhVvX/r574j+V8Ztba1fV3X0DjMea0RnfNmJzyiRUZH3tLU3DqDNevtHSKDGLPqDmwr9XtDNwRLaETyDWMWE8OUAAuAiKRFMmkAMECvXVFZWdnzsgpA/PDbooTARnS80QAwCXrgzP7CPb3Ip9cETUG3t+noV74t6DUi/iEzpnnVAk9eyjaeILnIOR9ekZx4ZnBifAYADE8ZmhETHdVQ39g00GUHLPAVx/MkSzcMwcyutpxk6DX19f/Ne2zpIKcsMtRSbrFoG73F8nw0GtvMudBCPNVPVh8o3BTwADswtbB8aGH5rmtn3ixPaI4mUYu4NwF/BW0TFF6yFuAbXCLG81XlhQW9zae3BE1BG4blJQL7atOdbrMYvw3TrXEgOQlAmBeb0EvVxhs4Ymws2B13yaIFRwEkd1yGLZo3a+8Lb/y5/XieMTspdeKSqgM9b8AAYEfZFzcNGTWpq9i5XIAmqD42MmLj3k827vXm7zlDd4XAM1NSpqz0u0kFwN1OjLkZUtYCABHpkNIOcAuDAjp8SUgvfo6YPPrS/MHZimJbIL4XS1AU9O41uT92GOYQEtglhLitq54JT0yYuaEBQENJQd7vifGM10DMuaUFeePGzl63sy/zC9XCHgLc69hz1bVi+64y1xd/zS0tnv9jKFvM+QBe9poiBbZtsVrEt8nREW+WF334im8rdq2hCVzPjAYQXQMADBpbF9H2FoD5AdzOHYd5k8VxvpDBod4MB6HG3tPxXmJa9r1getpD9JWuWRYgkBZ3H9DvBc0MKlnDC5h5mDT5CtPkEqtVGwOg/Q9lbMnKX/d3p33EgObftTZGzgPhaq/xJFawzTa679p4NgHa+ain5PnX3u65981YhNzcV/3t5DUhvkuICjvIDNQ2t12lm9L1ipZSPlte9FGPHRP2KBJNb9lMkp5xhEUsJ8ZsAADRvLjUnK9rDmzvxUZbfnj6SNkFdYziMrOvg0nuTSDQpAlz+tl9RV6P5C8F/d7l2LUu7x4htCx2bfhklq7r30LKUwBahcY/87Qfdc+mFiJ6ymdAQkbpsCPzfOp7SVLGzjsB/KCXblcnVVbf5c9ISl54qGTz5MM7N08e0GjNAOGYU2dKfgAI/DNZAd515uhnJyLCWx8E4F6iEC+LT83JCzSO5miND9TWk4EjxsZqJm0C4Ow2SWLOP/1FyZELiXeh9GtB22w2IU2+TzeMHwGc7KG6zmGYDSAsvS3vb8e6+o3NL1gPUA8nTfRC6TtTo/okSaZHOwvoIwK9ROA3CFhFwOsEegnA1s5umvcWno8Xb2XlFrs04fHwUnZ8asmsnnNzR2MpWgHg5KeftgKYDtBpZyAmfjcuLWd0j7GcxsQxgdh1xiZChXUtgBRXHKZnqyqKN/c+1sXRr0uOrKFfLjFMnutNR4ToaN36ji9flsbjJLRywOtXYoMREbEUwNNedAGTMDo7mQ2e6MoJWFW1f5vPU7TEtJzVIMxpT5AnxI/MGVZdsf1rX/ZMnf//uoOFW+JG3v4hgHs79CsT0rI+P1de8o3XAOTq75qA6drY1VQUnopJHz9Fk1SG9qVbGJg3x4644w7vPWn3U6ZbI+cm3jQuE2xI4eXzYpaytupIWb6nLCmt5EEGJnceGy9OShv/pM+xMwrPVhTd50t/ofTbDL1t7dQkEC/1pSfiZ0b+dHWzL33WnA2HCfwnX3pmLN69OjfFlz4QhK7NgvuhZ4Z8vWcP6ZkPCYHu33d4lAjL7hOKw04PAXCOe0BiTPTP4aWw2gOQBAAis6qrqn5/UQUxzQfQ1iFKFEJ+Ep8+YUj3QMJd0SSulJbQidIaOdmwRk7q+mPN0u1bDgnO7yoDEMNArK8fATd6HdNF0m8FTbplGdzrra7s23E89T1/MZi1ZwF4PXSAu413wUjPD6SIXj27v6iiJ/uz5UW7ARR6iLp1bCJCRER4iLY3xKqVSFN2m3mbjm6vAdEcdHTkQjXLyFETpj/m7X6atJ/UpF6m6W3/A6jbYqb6wPZ10qQxAA6hvaUspKl3e8iEaQ8jaRwk0zjS009Ixx4h9diu/nQBb3pJ3fPtC/4PN254FFK9DPgAAAAASUVORK5CYII="
LOGO_B64_SM = "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"
LOGO_IMG  = '<img src="data:image/png;base64,' + LOGO_B64    + '" style="width:160px;height:auto;display:block;margin:0 auto;mix-blend-mode:multiply">'
LOGO_SM   = '<img src="data:image/png;base64,' + LOGO_B64_SM + '" style="width:100px;height:auto;display:block;margin:0 auto;mix-blend-mode:multiply">'




# ── Tema claro — sobreescribe TODOS los colores ──────────────
_tc = st.session_state.get("tema_sel", "🌙 Oscuro") == "☀️ Claro"
if _tc:
    st.markdown("""<style>
    /* ── NUCLEAR: forzar texto oscuro en TODOS los elementos ── */
    [data-testid="stVerticalBlock"] *:not(svg):not(path):not(script):not(style) {
        color: #1A2640 !important;
    }
    /* Excepciones de color: mantener colores semánticos */
    [data-testid="stVerticalBlock"] *[style*="color:#2ECC87"],
    [data-testid="stVerticalBlock"] *[style*="color:#E85555"],
    [data-testid="stVerticalBlock"] *[style*="color:#C8A84B"],
    [data-testid="stVerticalBlock"] *[style*="color:#F0C040"] {
        color: inherit !important;
    }
    /* Cards HTML con fondo oscuro hardcoded */
    div[style*="background:#162236"],
    div[style*="background: #162236"],
    div[style*="background:#0F1A2B"],
    div[style*="background:#152034"],
    div[style*="background:#1a2d42"],
    div[style*="background:#111827"] {
        background: #FFFFFF !important;
        border-color: #C4D4E8 !important;
    }
    /* Fondo y texto base */
    .stApp { background:#F0F4F8 !important; color:#1A2640 !important; }

    /* Sidebar completo */
    section[data-testid="stSidebar"] { background:#E2EAF4 !important; }
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown * { color:#1A2640 !important; }

    /* Todos los textos en el área principal */
    .stMarkdown p, .stMarkdown span, .stMarkdown div,
    .stMarkdown h2, .stMarkdown h3,
    p, label { color:#1A2640 !important; }

    /* Inputs */
    input, textarea {
        background:#FFFFFF !important; color:#1A2640 !important;
        -webkit-text-fill-color:#1A2640 !important;
        border-color:#C4D4E8 !important;
    }
    input::placeholder, textarea::placeholder {
        color:#6A8090 !important; -webkit-text-fill-color:#6A8090 !important;
    }
    input:disabled {
        color:#C8A84B !important; -webkit-text-fill-color:#C8A84B !important;
    }

    /* Selectbox */
    [data-testid="stSelectbox"] > div > div {
        background:#FFFFFF !important; color:#1A2640 !important;
        border-color:#C4D4E8 !important;
    }
    [data-testid="stSelectbox"] span,
    [data-testid="stSelectbox"] p { color:#1A2640 !important; }
    [data-baseweb="popover"], [data-baseweb="popover"] *,
    [data-baseweb="menu"], [data-baseweb="menu"] *,
    [role="listbox"], [role="listbox"] * {
        background:#FFFFFF !important; color:#1A2640 !important;
    }
    [role="option"]:hover { background:#E2EAF4 !important; color:#C8A84B !important; }

    /* Métricas */
    [data-testid="metric-container"] {
        background:#FFFFFF !important; border-color:#C4D4E8 !important;
    }
    [data-testid="stMetricValue"] { color:#1A2640 !important; }
    [data-testid="stMetricLabel"] { color:#4A6080 !important; }

    /* Formularios */
    [data-testid="stForm"] { background:#EDF2F7 !important; border-color:#C4D4E8 !important; }
    [data-testid="stDataFrame"] { border-color:#C4D4E8 !important; }
    [data-testid="stAlert"] { background:#FFFFFF !important; color:#1A2640 !important; }

    /* Tabs */
    [data-testid="stTabs"] button { color:#4A6080 !important; background:transparent !important; }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color:#C8A84B !important; border-bottom-color:#C8A84B !important;
    }

    /* Radio y checkbox */
    [data-testid="stRadio"] label span,
    [data-testid="stRadio"] label p { color:#1A2640 !important; font-weight:500 !important; }

    /* Number input */
    [data-testid="stNumberInput"] button {
        background:#E2EAF4 !important; color:#1A2640 !important; border-color:#C4D4E8 !important;
    }

    /* Separadores */
    hr { border-color:#C4D4E8 !important; }

    /* Headings */
    h1 { color:#C8A84B !important; }
    h2 { color:#4A6080 !important; }
    h3 { color:#A07830 !important; }

    /* Botones */
    .stButton > button { color:#0D1929 !important; }

    /* Cards HTML inline — los div con background var(--surface) */
    /* No se pueden sobreescribir variables CSS desde aquí,
       pero forzamos el color de texto en todos los divs del main */
    [data-testid="stVerticalBlock"] div[style*="background:#162236"],
    [data-testid="stVerticalBlock"] div[style*="background: #162236"] {
        background:#FFFFFF !important; color:#1A2640 !important;
    }

    /* Expander */
    [data-testid="stExpander"] { background:#FFFFFF !important; border-color:#C4D4E8 !important; }
    [data-testid="stExpander"] summary { color:#1A2640 !important; }

    /* Selectbox base */
    [data-baseweb="select"] > div { background:#FFFFFF !important; border-color:#C4D4E8 !important; }
    [data-baseweb="select"] svg { fill:#4A6080 !important; }

    /* Date input */
    [data-testid="stDateInput"] input { color:#1A2640 !important; -webkit-text-fill-color:#1A2640 !important; }

    </style>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# FIREBASE AUTH
# ══════════════════════════════════════════════════════
def firebase_login(email, pwd):
    try:
        r = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_KEY}",
            json={"email": email, "password": pwd, "returnSecureToken": True}, timeout=8)
        if r.status_code == 200: return True, r.json()
        return False, r.json().get("error", {}).get("message", "Error")
    except Exception as e: return False, str(e)

def firebase_crear(email, pwd):
    try:
        r = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_KEY}",
            json={"email": email, "password": pwd, "returnSecureToken": True}, timeout=8)
        if r.status_code == 200: return True, "OK"
        return False, r.json().get("error", {}).get("message", "Error")
    except Exception as e: return False, str(e)

# ══════════════════════════════════════════════════════
# FIRESTORE CRUD
# ══════════════════════════════════════════════════════
def _f(v):
    if isinstance(v, bool):  return {"booleanValue": v}
    if isinstance(v, int):   return {"integerValue": str(v)}
    if isinstance(v, float): return {"doubleValue": v}
    return {"stringValue": str(v)}

def _auth_header():
    token = st.session_state.get("auth_token", "")
    return {"Authorization": f"Bearer {token}"} if token else {}

def fs_get(col):
    try:
        r = requests.get(f"{FS_URL}/{col}", timeout=10)
        if r.status_code == 200:
            docs = r.json().get("documents", [])
            rows = [{"_id": d["name"].split("/")[-1],
                     **{k: list(v.values())[0] for k,v in d.get("fields",{}).items()}}
                    for d in docs]
            return pd.DataFrame(rows) if rows else pd.DataFrame()
    except Exception: pass
    return pd.DataFrame()

def fs_post(col, datos):
    headers = _auth_header()
    try:
        r = requests.post(f"{FS_URL}/{col}", headers=headers,
                          json={"fields": {k: _f(v) for k,v in datos.items()}}, timeout=10)
        if r.status_code in (200,201): return True, ""
        return False, f"Error {r.status_code}: {r.text[:300]}"
    except Exception as e: return False, str(e)

def fs_patch(col, doc_id, datos):
    headers = _auth_header()
    mask = "&".join(f"updateMask.fieldPaths={k}" for k in datos)
    try:
        requests.patch(f"{FS_URL}/{col}/{doc_id}?{mask}", headers=headers,
                       json={"fields": {k: _f(v) for k,v in datos.items()}}, timeout=10)
        return True
    except Exception: return False

def fs_delete(col, doc_id):
    headers = _auth_header()
    try:
        requests.delete(f"{FS_URL}/{col}/{doc_id}", headers=headers, timeout=10)
        return True
    except Exception: return False

# ══════════════════════════════════════════════════════
# PRECIOS EN TIEMPO REAL
# ══════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def get_trm():
    for url in ["https://open.er-api.com/v6/latest/USD",
                "https://api.frankfurter.app/latest?from=USD&to=COP"]:
        try:
            r = requests.get(url, timeout=6)
            cop = r.json().get("rates",{}).get("COP") if r.status_code==200 else None
            if cop and float(cop)>3000: return float(cop)
        except: pass
    try:
        import yfinance as yf
        px = yf.Ticker("USDCOP=X").fast_info.last_price
        if px and px>3000: return float(px)
    except: pass
    return 4200.0

@st.cache_data(ttl=300)
def get_cmc(syms):
    if not syms: return {}
    try:
        r = requests.get(
            "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest",
            params={"symbol":",".join(syms),"convert":"USD"},
            headers={"X-CMC_PRO_API_KEY":CMC_KEY,"Accept":"application/json"}, timeout=10)
        if r.status_code!=200: return {}
        out={}
        for sym,items in r.json().get("data",{}).items():
            item = items[0] if isinstance(items,list) else items
            q = item.get("quote",{}).get("USD",{})
            out[sym.upper()]={"price":q.get("price",0),"chg24":q.get("percent_change_24h",0)}
        return out
    except: return {}

@st.cache_data(ttl=300)
def get_stock(ticker):
    try:
        import yfinance as yf
        info  = yf.Ticker(ticker).fast_info
        price = getattr(info,"last_price",None) or getattr(info,"previous_close",None)
        prev  = getattr(info,"previous_close",price) or price
        chg   = ((price-prev)/prev*100) if price and prev else 0
        return float(price) if price else None, float(chg)
    except: return None, 0

def get_prices(df):
    out={}
    if df.empty: return out
    df_ab = df[df["Estado"]=="Abierta"] if "Estado" in df.columns else df
    if df_ab.empty: return out
    criptos=[x.strip().upper() for x in df_ab[df_ab["Categoria"]=="Cripto"]["Ticker_API"].dropna() if x.strip()]
    if criptos: out.update(get_cmc(tuple(set(criptos))))
    stocks=[x.strip().upper() for x in df_ab[df_ab["Categoria"].isin(["Acción","ETF","Fondo"])]["Ticker_API"].dropna() if x.strip()]
    for t in set(stocks):
        px,chg=get_stock(t)
        if px: out[t]={"price":px,"chg24":chg}
    return out

# ══════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════
COLS = ["_id","Fondo","Usuario","Fecha_Compra","Activo","Categoria",
        "Cantidad","Precio_Compra","Broker","Ticker_API",
        "Fecha_Venta","Precio_Venta","Estado","Notas"]

@st.cache_data(ttl=60, show_spinner=False)
def load_inv():
    def norm(df):
        num=["Cantidad","Precio_Compra","Precio_Venta"]
        for c in num:
            if c in df.columns: df[c]=pd.to_numeric(df[c],errors="coerce").fillna(0.0)
            else: df[c]=0.0
        for c in COLS:
            if c not in df.columns: df[c]=""
        return df[COLS]

    df_new = fs_get("inversiones")
    df_new = norm(df_new) if not df_new.empty else pd.DataFrame(columns=COLS)

    df_ops = fs_get("operaciones")
    rows_legacy=[]
    if not df_ops.empty:
        for _,r in df_ops.iterrows():
            resultado=str(r.get("Resultado","Abierta"))
            if resultado=="Abierta": estado,fv,pv="Abierta","",0.0
            elif resultado in ("Ganadora","Perdedora","Cancelada"):
                estado="Cerrada"
                pe=float(r.get("Precio_Entrada",0) or 0)
                tp=float(r.get("TP_pct",0) or 0)
                sl=float(r.get("SL_pct",0) or 0)
                if resultado=="Ganadora" and tp>0: pv=pe*(1+tp/100)
                elif resultado=="Perdedora" and sl>0: pv=pe*(1-sl/100)
                else: pv=pe
                fv=str(r.get("Fecha",""))
            else: estado,fv,pv="Abierta","",0.0
            cant=float(r.get("Cantidad",0) or 0)
            pe=float(r.get("Precio_Entrada",0) or 0)
            vp=float(r.get("Valor_Pos",0) or 0)
            if cant==0 and pe>0 and vp>0: cant=round(vp/pe,8)
            cat=str(r.get("Categoria","") or r.get("Moneda","") or "Otro")
            rows_legacy.append({
                "_id":str(r.get("_id","")), "Fondo":str(r.get("Fondo","")),
                "Usuario":str(r.get("Usuario","")), "Fecha_Compra":str(r.get("Fecha","")),
                "Activo":str(r.get("Activo","") or r.get("Moneda","")),
                "Categoria":cat, "Cantidad":cant, "Precio_Compra":pe,
                "Broker":str(r.get("Broker","")), "Ticker_API":str(r.get("Ticker_API","")),
                "Fecha_Venta":fv, "Precio_Venta":pv, "Estado":estado,
                "Notas":str(r.get("Notas","")),
            })

    if rows_legacy:
        df_leg=pd.DataFrame(rows_legacy)
        for c in ["Cantidad","Precio_Compra","Precio_Venta"]:
            df_leg[c]=pd.to_numeric(df_leg[c],errors="coerce").fillna(0.0)
        df_leg["_id"]="ops_"+df_leg["_id"].astype(str)
        # Deduplicar
        if not df_new.empty:
            keys_new=set(zip(df_new["Activo"].str.upper().str.strip(),
                             df_new["Fecha_Compra"].astype(str).str[:10],
                             df_new["Usuario"].str.lower().str.strip()))
            mask_dup=df_leg.apply(lambda r:(
                str(r["Activo"]).upper().strip(),str(r["Fecha_Compra"])[:10],
                str(r["Usuario"]).lower().strip()) in keys_new, axis=1)
            df_leg=df_leg[~mask_dup]
    else:
        df_leg=pd.DataFrame(columns=COLS)

    combined=pd.concat([df_new,df_leg],ignore_index=True)
    return combined if not combined.empty else pd.DataFrame(columns=COLS)

@st.cache_data(ttl=60, show_spinner=False)
def load_aportes():
    df=fs_get("aportes")
    if df.empty: return pd.DataFrame(columns=["_id","Fondo","Socio","Cedula","Fecha","Tipo","Monto","TipoCuenta","Usuario"])
    if "Monto" in df.columns: df["Monto"]=pd.to_numeric(df["Monto"],errors="coerce").fillna(0.0)
    return df

@st.cache_data(ttl=60, show_spinner=False)
def load_usuarios():
    df=fs_get("usuarios")
    if df.empty: return pd.DataFrame(columns=["_id","Email","Nombre","Modo","Fondo","Activo"])
    return df

# ══════════════════════════════════════════════════════
# CÁLCULOS P&L
# ══════════════════════════════════════════════════════
def calcular_posicion(row, prices):
    ticker=str(row.get("Ticker_API","")).strip().upper()
    cat=str(row.get("Categoria",""))
    cant=float(row.get("Cantidad",0) or 0)
    pc=float(row.get("Precio_Compra",0) or 0)
    pv=float(row.get("Precio_Venta",0) or 0)
    estado=str(row.get("Estado","Abierta"))
    costo=cant*pc

    if estado=="Cerrada" and pv>0:
        val=cant*pv; gp=val-costo
        return costo,val,gp,(gp/costo*100 if costo else 0),pv,0

    if cat in ["CDT","Cuenta Remunerada"] and pc>0 and costo>0:
        try:
            dias=max((pd.Timestamp.now()-pd.to_datetime(row.get("Fecha_Compra"))).days,0)
            val=costo*((1+pc)**(dias/365)); gp=val-costo
            return costo,val,gp,(gp/costo*100 if costo else 0),pc,0
        except: return costo,costo,0,0,pc,0

    if ticker and ticker in prices and prices[ticker].get("price",0)>0:
        px=prices[ticker]["price"]; chg=prices[ticker].get("chg24",0)
        if pc>0 and cant>0:
            val=px*cant; gp=val-costo
            return costo,val,gp,(gp/costo*100 if costo else 0),px,chg
        if costo>0 and pc>0:
            val=costo*px/pc; gp=val-costo
            return costo,val,gp,(gp/costo*100 if costo else 0),px,chg

    return costo,costo,0.0,0.0,pc,0

# ══════════════════════════════════════════════════════
# UI HELPERS
# ══════════════════════════════════════════════════════
PT=dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Mono",color="#DCE5F0",size=11),
        margin=dict(l=10,r=10,t=36,b=10),
        xaxis=dict(gridcolor="#1e3350",linecolor="#2a4060",tickfont=dict(color="#8BA5C8")),
        yaxis=dict(gridcolor="#1e3350",linecolor="#2a4060",tickfont=dict(color="#8BA5C8")))

def money(v,f=1):
    v2=v*f
    if abs(v2)>=1e6: return f"${v2/1e6:.2f}M"
    return f"${v2:,.2f}"

def card(label,val,sub=None,color="#C8A84B"):
    s=f'<div style="font:500 11px/1.4 IBM Plex Mono,mono;color:{color};margin-top:3px">{sub}</div>' if sub else ""
    return f"""<div style="background:var(--surface);border:1px solid var(--border);border-radius:10px;
        padding:16px 18px;position:relative;overflow:hidden;height:100%">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;background:{color}"></div>
      <div style="font:400 9px/1 IBM Plex Mono,mono;color:var(--muted);letter-spacing:1.5px;
                  text-transform:uppercase;margin-bottom:8px">{label}</div>
      <div style="font:600 22px/1 IBM Plex Mono,mono;color:var(--text)">{val}</div>{s}</div>"""

def sec(t):
    st.markdown(f'<h2 style="margin:18px 0 10px">{t}</h2>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown(
        '<div style="text-align:center;padding:40px 0 20px">'
        + LOGO_IMG +
        '<br><div style="font:400 11px/1.5 IBM Plex Mono,mono;color:#8BA5C8;'
        'letter-spacing:2px;margin-top:8px">PLATAFORMA · ACCESO PRIVADO</div></div>',
        unsafe_allow_html=True
    )
    _, col, _ = st.columns([1,1.2,1])
    with col:
        email = st.text_input("Correo electrónico", placeholder="usuario@email.com")
        pwd   = st.text_input("Contraseña", type="password")
        if st.button("ENTRAR →", use_container_width=True):
            if email and pwd:
                with st.spinner("Verificando…"):
                    ok, result = firebase_login(email, pwd)
                if ok:
                    em    = email.strip().lower()
                    rol   = "admin" if em == ADMIN_EMAIL.lower() else "usuario"
                    token = result.get("idToken", "")
                    df_u  = load_usuarios()
                    modo_u = MODO_IND; fondo_u = None
                    if not df_u.empty and "Email" in df_u.columns:
                        fila = df_u[df_u["Email"].str.lower() == em]
                        if not fila.empty:
                            modo_u  = fila.iloc[0].get("Modo", MODO_IND)
                            fondo_u = fila.iloc[0].get("Fondo") or None
                    st.session_state.update({
                        "logged_in": True, "usuario": em, "rol": rol,
                        "modo": modo_u, "fondo_asignado": fondo_u,
                        "fondo_sel": "Arkez Invest",
                        "auth_token": token,
                    })
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
            else:
                st.warning("Completa los dos campos")

        # ── Recuperar contraseña ──────────────────────────────────────────
        st.markdown("""<div style="text-align:center;margin-top:10px">
          <span style="font:400 12px IBM Plex Mono,mono;color:#8BA5C8">
            ¿Olvidaste tu contraseña? →</span></div>""", unsafe_allow_html=True)
        if st.button("Enviar correo de recuperación", key="btn_reset",
                     help="Te enviaremos un email para resetear tu contraseña"):
            if email.strip():
                with st.spinner("Enviando correo de recuperación…"):
                    try:
                        r_reset = requests.post(
                            f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_KEY}",
                            json={"requestType": "PASSWORD_RESET", "email": email.strip()},
                            timeout=8
                        )
                        if r_reset.status_code == 200:
                            st.success(f"✓ Correo enviado a {email.strip()} — revisa tu bandeja de entrada")
                        else:
                            err = r_reset.json().get("error", {}).get("message", "Error")
                            st.error(f"❌ {err}")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.warning("Primero escribe tu correo electrónico")
    st.stop()

# ══════════════════════════════════════════════════════
# SESIÓN Y DATOS
# ══════════════════════════════════════════════════════
rol    = st.session_state.rol
usuario= st.session_state.usuario
modo   = st.session_state.get("modo", MODO_IND)
fa     = st.session_state.get("fondo_asignado")

df_inv_all  = load_inv()
df_ap_all   = load_aportes()
df_usr_all  = load_usuarios()

fondos_set  = (set(df_ap_all["Fondo"].dropna()) | set(df_inv_all["Fondo"].dropna())) - {""}
fondos_list = sorted(fondos_set) or ["Arkez Invest"]
if "Arkez Invest" not in fondos_list: fondos_list.insert(0, "Arkez Invest")

# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""<div style="text-align:center;padding:10px 0 8px">
      <div style="margin-bottom:6px">{LOGO_SM}</div>
    </div>""", unsafe_allow_html=True)

    rc = "#C8A84B" if rol=="admin" else "#2ECC87"
    st.markdown(f"""<div style="background:#152034;border:1px solid #1E3354;border-radius:8px;
        padding:10px 12px;margin-bottom:10px">
      <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px;margin-bottom:3px">USUARIO</div>
      <div style="font:400 11px/1.4 IBM Plex Mono,mono;color:var(--text);word-break:break-all">{usuario}</div>
      <span style="display:inline-block;margin-top:4px;background:rgba(200,168,75,.12);color:{rc};
                   border:1px solid {rc};padding:1px 9px;border-radius:20px;
                   font:600 9px/1.8 IBM Plex Mono,mono">
        {'⬡ ADMIN' if rol=='admin' else '● '+modo.split()[0].upper()}</span></div>""",
        unsafe_allow_html=True)

    if rol == "admin":
        idx = fondos_list.index(st.session_state.get("fondo_sel","Arkez Invest")) \
              if st.session_state.get("fondo_sel") in fondos_list else 0
        fondo = st.selectbox("🏦 Fondo activo", fondos_list, index=idx)
        st.session_state.fondo_sel = fondo
    else:
        if fa and fa in fondos_list:
            fondo = fa
        else:
            fondo = f"personal_{usuario.split('@')[0]}"
        st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);border-radius:6px;
            padding:8px 12px;margin-bottom:8px">
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted)">FONDO / PORTAFOLIO</div>
          <div style="font:600 12px IBM Plex Mono,mono;color:#C8A84B">{fondo}</div>
        </div>""", unsafe_allow_html=True)

    trm = get_trm()
    st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;
        padding:9px 12px;margin:8px 0">
      <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted);letter-spacing:1px">TRM USD/COP</div>
      <div style="font:600 16px/1.5 IBM Plex Mono,mono;color:#F0C040">${trm:,.2f}</div>
    </div>""", unsafe_allow_html=True)

    moneda = st.radio("Moneda", ["USD","COP"], horizontal=True)
    factor = trm if moneda=="COP" else 1.0
    sfx    = " COP" if moneda=="COP" else " USD"

    st.markdown("---")
    tema = st.radio("🎨 Tema", ["🌙 Oscuro","☀️ Claro"], horizontal=True,
                    key="tema_sel")
    tema_claro = tema == "☀️ Claro"

    st.markdown("---")
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# ══════════════════════════════════════════════════════
# FILTRAR DATOS
# ══════════════════════════════════════════════════════
def inv_visibles(df):
    """
    Reglas de visibilidad:
    - Admin: ve fondos GRUPALES. NO ve portafolios individuales de otros.
    - Observador: ve solo lectura del fondo grupal asignado.
    - Portafolio individual: SOLO ve sus propias inversiones (ni admin puede verlas en la UI).
    """
    if df.empty: return df

    if rol == "admin":
        # Admin ve el fondo seleccionado, EXCEPTO inversiones de portafolios individuales ajenos
        df_fondo = df[df["Fondo"] == fondo].copy()
        # Excluir registros cuyo Usuario no sea el admin y cuyo fondo sea personal_*
        if "Usuario" in df_fondo.columns and "Fondo" in df_fondo.columns:
            es_personal_ajeno = (
                df_fondo["Fondo"].str.startswith("personal_", na=False) &
                (df_fondo["Usuario"].str.lower() != usuario)
            )
            df_fondo = df_fondo[~es_personal_ajeno]
        return df_fondo

    if modo == MODO_OBS:
        # Observador: solo lectura del fondo grupal asignado
        return df[df["Fondo"] == fondo]

    # Portafolio individual: SOLO sus propias inversiones, sin importar el fondo
    mask = pd.Series([False] * len(df), index=df.index)
    if "Usuario" in df.columns:
        mask = mask | (df["Usuario"].str.lower() == usuario.lower())
    if "Fondo" in df.columns:
        mask = mask | (df["Fondo"] == fondo)
    return df[mask]

df_inv = inv_visibles(df_inv_all).copy()
df_ap  = df_ap_all[df_ap_all["Fondo"]==fondo].copy() if not df_ap_all.empty else pd.DataFrame()
prices = get_prices(df_inv)

# Calcular todas las posiciones
posiciones = []
total_invertido = 0
total_actual    = 0
total_gp        = 0

for _, row in df_inv.iterrows():
    inv, act, gp, gp_pct, px, chg = calcular_posicion(row, prices)
    total_invertido += inv
    total_actual    += act
    total_gp        += gp
    posiciones.append({
        "Activo":     row.get("Activo","—"),
        "Categoria":  row.get("Categoria","—"),
        "Ticker":     row.get("Ticker_API","—"),
        "Estado":     row.get("Estado","Abierta"),
        "F_Compra":   row.get("Fecha_Compra","—"),
        "F_Venta":    row.get("Fecha_Venta",""),
        "Cantidad":   float(row.get("Cantidad",0) or 0),
        "Px_Compra":  float(row.get("Precio_Compra",0) or 0),
        "Px_Actual":  px,
        "Chg24":      chg,
        "Invertido":  inv,
        "Val_Actual": act,
        "GP_usd":     gp,
        "GP_pct":     gp_pct,
        "_id":        row.get("_id",""),
        "Usuario":    row.get("Usuario","—"),
    })

# Cash neto: depósitos extra + retiros (no son compras de activos)
# Aporte = entró dinero al fondo/portafolio
# Retiro = salió dinero → reduce el valor real del portafolio
cash_aportes = 0.0
cash_retiros = 0.0
if not df_ap.empty and "Tipo" in df_ap.columns:
    cash_aportes = df_ap[df_ap["Tipo"]=="Aporte"]["Monto"].sum()
    cash_retiros = df_ap[df_ap["Tipo"]=="Retiro"]["Monto"].sum()
cash_neto = cash_aportes - cash_retiros  # positivo = hay cash disponible, negativo = retiraron más

# Portafolio real = valor de posiciones abiertas + cash neto (retiros ya restan)
# Si hay retiros, el valor total baja aunque las posiciones estén bien
total_actual_real = total_actual + max(cash_neto, 0)  # solo suma cash si es positivo
total_gp_real     = total_gp + cash_neto if cash_neto < 0 else total_gp
rend_pct = total_gp / total_invertido * 100 if total_invertido > 0 else 0

pos_abiertas = [p for p in posiciones if p["Estado"]=="Abierta"]
pos_cerradas = [p for p in posiciones if p["Estado"]=="Cerrada"]

# ══════════════════════════════════════════════════════
# HEADER + KPIs
# ══════════════════════════════════════════════════════
badge = ""
if rol != "admin":
    badge = ' <span style="font:600 9px IBM Plex Mono,mono;background:rgba(46,204,135,.12);color:#2ECC87;border:1px solid #2ECC87;padding:1px 7px;border-radius:20px">PORTAFOLIO PERSONAL</span>' \
            if modo == MODO_IND else \
            ' <span style="font:600 9px IBM Plex Mono,mono;background:rgba(155,142,196,.12);color:#9B8EC4;border:1px solid #9B8EC4;padding:1px 7px;border-radius:20px">SOLO LECTURA</span>'

st.markdown(f"""<div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:4px">
  <img src="data:image/png;base64,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" style="width:36px;height:36px;flex-shrink:0;object-fit:contain">
  <div>
    <div style="font:600 18px/1 IBM Plex Mono,mono;color:#C8A84B;letter-spacing:2px">
      {fondo.upper()}{badge}</div>
    <div style="font:400 10px/1.5 IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">
      ARKEZ · PLATAFORMA · PRECIOS EN TIEMPO REAL</div>
  </div>
  <div style="margin-left:auto;font:400 10px IBM Plex Mono,mono;color:#8BA5C8">
    {datetime.now().strftime('%d/%m/%Y %H:%M')}</div></div>
<hr style="margin:12px 0 18px">""", unsafe_allow_html=True)

# ── FILTRO DE PERIODO ──────────────────────────────────
col_per1, col_per2, col_per3 = st.columns([2,2,4])
with col_per1:
    periodo = st.selectbox("📅 Ver período",
        ["Todo el historial","Este mes","Este año",
         "Última semana","Últimos 3 meses","Personalizado"],
        key="periodo_sel")
with col_per2:
    if periodo == "Personalizado":
        fecha_desde = st.date_input("Desde", value=date(date.today().year,1,1), key="f_desde")
        fecha_hasta = st.date_input("Hasta", value=date.today(), key="f_hasta")
    else:
        fecha_desde = None
        fecha_hasta = None

# Calcular rango de fechas según periodo
hoy = pd.Timestamp.now().normalize()
if   periodo == "Este mes":        f_ini = hoy.replace(day=1);              f_fin = hoy
elif periodo == "Este año":        f_ini = hoy.replace(month=1,day=1);      f_fin = hoy
elif periodo == "Última semana":   f_ini = hoy - pd.Timedelta(days=7);      f_fin = hoy
elif periodo == "Últimos 3 meses": f_ini = hoy - pd.Timedelta(days=90);     f_fin = hoy
elif periodo == "Personalizado" and fecha_desde and fecha_hasta:
    f_ini = pd.Timestamp(fecha_desde); f_fin = pd.Timestamp(fecha_hasta)
else:
    f_ini = None; f_fin = None  # Todo el historial

# Aplicar filtro de periodo a las posiciones
def en_periodo(p):
    """
    Lógica de período:
    - Todo el historial: todo (excepto archivadas)
    - Filtros específicos:
      * Archivadas: NUNCA se muestran
      * Abiertas: SIEMPRE se incluyen (siguen activas hoy)
      * Cerradas: solo si fecha_venta cae dentro del rango
    """
    estado = p.get("Estado", "Abierta")
    if estado == "Archivada": return False
    if f_ini is None: return True   # Todo el historial
    if estado == "Abierta": return True
    try:
        fv = pd.to_datetime(p["F_Venta"]) if p["F_Venta"] else hoy
        return f_ini <= fv <= f_fin
    except: return True

def en_periodo_kpi(p):
    """Para los KPIs de ganancias: cerradas en el período."""
    estado = p.get("Estado", "Abierta")
    if estado == "Archivada": return False
    if f_ini is None: return True
    if estado == "Abierta": return True
    try:
        fv = pd.to_datetime(p["F_Venta"]) if p["F_Venta"] else hoy
        return f_ini <= fv <= f_fin
    except: return True

# Todas las posiciones visibles (abiertas siempre + cerradas del período)
pos_periodo   = [p for p in posiciones if en_periodo(p)]
pos_ab_per    = [p for p in pos_periodo if p["Estado"] == "Abierta"]
pos_cer_per   = [p for p in pos_periodo if p["Estado"] == "Cerrada"]

# Capital: todas las posiciones abiertas (independiente del período)
pos_abiertas_todas = [p for p in posiciones if p["Estado"] == "Abierta"]
inv_per   = sum(p["Invertido"]  for p in pos_abiertas_todas)
act_per   = sum(p["Val_Actual"] for p in pos_abiertas_todas)
pnl_ab    = sum(p["GP_usd"]     for p in pos_abiertas_todas)

# Ganancias/pérdidas realizadas: SOLO cerradas dentro del período seleccionado
pnl_cerradas_periodo = sum(p["GP_usd"] for p in pos_cer_per)

# G/P total del período = PnL abierto + PnL cerrado en período
gp_per  = pnl_ab + pnl_cerradas_periodo
rend_per = gp_per / inv_per * 100 if inv_per > 0 else 0

# Badge informativo del período
label_periodo = periodo if f_ini is None else f"{f_ini.strftime('%d/%m/%y')} → {f_fin.strftime('%d/%m/%y')}"

# Badge de período
per_badge = f'<span style="font:400 10px IBM Plex Mono,mono;color:#8BA5C8;margin-left:8px">{label_periodo}</span>'
st.markdown(f'<div style="margin:4px 0 12px">{per_badge}</div>', unsafe_allow_html=True)

gc = "#2ECC87" if gp_per >= 0 else "#E85555"
k1,k2,k3,k4,k5 = st.columns(5)
with k1: st.markdown(card("Portafolio actual",   money(act_per,factor)+sfx), unsafe_allow_html=True)
with k2: st.markdown(card("Total invertido",     money(inv_per,factor)+sfx, color="#8BA5C8"), unsafe_allow_html=True)
with k3: st.markdown(card("Ganancia / Pérdida",
    f"{'+'if gp_per>=0 else ''}{money(gp_per,factor)}{sfx}",
    f"{'▲' if rend_per>=0 else '▼'} {abs(rend_per):.2f}%", color=gc), unsafe_allow_html=True)
with k4: st.markdown(card("Posiciones abiertas", str(len(pos_ab_per)),
    f"{len(pos_cer_per)} cerradas en período", color="#F0C040"), unsafe_allow_html=True)
with k5:
    ganadoras_per = sum(1 for p in pos_cer_per if p["GP_usd"] > 0)
    wr = ganadoras_per/len(pos_cer_per)*100 if pos_cer_per else 0
    st.markdown(card("Win rate", f"{wr:.1f}%",
        f"{ganadoras_per}/{len(pos_cer_per)} cerradas en verde", color="#9B8EC4"), unsafe_allow_html=True)

# ── Indicadores de análisis (fila secundaria) ─────────────
ops_cerradas_calc = [p for p in posiciones if p["Estado"]=="Cerrada"]
if posiciones and ops_cerradas_calc:
    pnls = [p["GP_usd"] for p in ops_cerradas_calc]
    gans = [x for x in pnls if x > 0]
    pers = [x for x in pnls if x < 0]
    avg_g = sum(gans)/len(gans) if gans else 0
    avg_p = abs(sum(pers)/len(pers)) if pers else 0
    # R/R Ratio: ganancia promedio / pérdida promedio
    rr = avg_g / avg_p if avg_p > 0 else 0
    # Esperanza matemática: WR*AvgGan - (1-WR)*AvgPer
    wr_dec = len(gans)/len(pnls) if pnls else 0
    esperanza = wr_dec * avg_g - (1 - wr_dec) * avg_p
    # Profit Factor: suma ganancias / suma pérdidas
    pf = sum(gans)/abs(sum(pers)) if pers else 0

    ind1, ind2, ind3, ind_sep = st.columns([1,1,1,2])
    with ind1:
        rr_color = "#2ECC87" if rr >= 1 else "#E85555"
        st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);
            border-radius:8px;padding:10px 14px;border-left:3px solid {rr_color}">
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted);letter-spacing:1px">R/R RATIO</div>
          <div style="font:600 18px IBM Plex Mono,mono;color:{rr_color}">{rr:.2f}</div>
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted)">
            {'✓ Favorable' if rr>=1 else '✗ Desfavorable'} (meta: >1.0)</div>
        </div>""", unsafe_allow_html=True)
    with ind2:
        esp_color = "#2ECC87" if esperanza > 0 else "#E85555"
        st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);
            border-radius:8px;padding:10px 14px;border-left:3px solid {esp_color}">
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted);letter-spacing:1px">ESPERANZA MATEMÁTICA</div>
          <div style="font:600 18px IBM Plex Mono,mono;color:{esp_color}">
            {'+'if esperanza>=0 else ''}{money(esperanza,factor)}</div>
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted)">
            Por operación cerrada</div>
        </div>""", unsafe_allow_html=True)
    with ind3:
        pf_color = "#2ECC87" if pf >= 1 else "#E85555"
        st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);
            border-radius:8px;padding:10px 14px;border-left:3px solid {pf_color}">
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted);letter-spacing:1px">PROFIT FACTOR</div>
          <div style="font:600 18px IBM Plex Mono,mono;color:{pf_color}">{pf:.2f}x</div>
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted)">
            {'✓ Sistema rentable' if pf>=1 else '✗ Sistema no rentable'} (meta: >1.0)</div>
        </div>""", unsafe_allow_html=True)
    with ind_sep:
        st.markdown(f"""<div style="padding:10px 14px">
          <div style="font:400 9px IBM Plex Mono,mono;color:var(--muted);margin-bottom:4px">
            Basado en {len(pnls)} ops cerradas · Avg gan: +{money(avg_g,factor)} · Avg per: -{money(avg_p,factor)}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════
puede_registrar = (rol=="admin") or (modo==MODO_IND)

if rol == "admin":
    tabs = st.tabs(["⬡ Dashboard","◈ Portafolio","📌 Registrar","💵 Capital","👥 Usuarios","⚙ Admin"])
    t_dash,t_port,t_reg,t_cap,t_usr,t_adm = tabs
elif puede_registrar:
    tabs = st.tabs(["⬡ Dashboard","◈ Mi portafolio","📌 Registrar","💵 Capital"])
    t_dash,t_port,t_reg,t_cap = tabs
else:
    tabs = st.tabs(["⬡ Dashboard","◈ Portafolio"])
    t_dash,t_port = tabs

# ══════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════
with t_dash:
    cl, cr = st.columns([3,2])

    with cl:
        sec("Evolución del portafolio")
        if pos_periodo:
            # Serie de puntos: fecha_compra con valor invertido, fecha_actual/venta con valor actual
            # Para cada posición construimos dos puntos y luego interpolamos
            eventos = []
            for p in pos_periodo:
                try:
                    fc = pd.to_datetime(p["F_Compra"])
                    fv = pd.to_datetime(p["F_Venta"]) if p["F_Venta"] else pd.Timestamp.now().normalize()
                    # Punto de entrada: el día de compra el valor era = invertido
                    eventos.append({"fecha": fc, "invertido": p["Invertido"], "actual": p["Invertido"]})
                    # Punto de salida: valor actual (precio de hoy o de venta)
                    eventos.append({"fecha": fv, "invertido": p["Invertido"], "actual": p["Val_Actual"]})
                except: pass

            if eventos:
                df_ev = pd.DataFrame(eventos).sort_values("fecha")
                # Agrupar por fecha sumando todas las posiciones activas en ese momento
                df_val = df_ev.groupby("fecha").agg(
                    invertido=("invertido","sum"),
                    actual=("actual","sum")
                ).reset_index()
                df_val["invertido"] *= factor
                df_val["actual"]    *= factor

                fig = go.Figure()
                # Área de valor actual (portafolio)
                fig.add_trace(go.Scatter(
                    x=df_val["fecha"], y=df_val["actual"],
                    mode="lines+markers",
                    line=dict(color="#C8A84B", width=2.5),
                    fill="tozeroy", fillcolor="rgba(200,168,75,0.08)",
                    marker=dict(color="#C8A84B", size=7,
                                line=dict(color="#111827", width=1.5)),
                    name=f"Valor ({moneda})",
                    hovertemplate="<b>%{x|%d/%m/%Y}</b><br>Valor: %{y:$,.2f}"+sfx+"<extra></extra>"
                ))
                # Línea de capital invertido
                fig.add_trace(go.Scatter(
                    x=df_val["fecha"], y=df_val["invertido"],
                    mode="lines",
                    line=dict(color="#38BDF8", width=2, dash="dash"),
                    name=f"Invertido ({moneda})",
                    hovertemplate="Invertido: %{y:$,.2f}"+sfx+"<extra></extra>"
                ))
                # Zona verde/roja entre ambas líneas
                fig.add_trace(go.Scatter(
                    x=list(df_val["fecha"])+list(df_val["fecha"][::-1]),
                    y=list(df_val["actual"])+list(df_val["invertido"][::-1]),
                    fill="toself",
                    fillcolor="rgba(46,204,135,0.07)" if gp_per>=0 else "rgba(232,85,85,0.07)",
                    line=dict(color="rgba(0,0,0,0)"),
                    showlegend=False, hoverinfo="skip"
                ))
                fig.update_layout(**PT,
                    title=dict(text=f"Portafolio vs Capital invertido ({moneda})",
                               font=dict(size=11,color="#8BA5C8"),x=.5),
                    yaxis_title=moneda,
                    legend=dict(bgcolor="rgba(0,0,0,0)",
                                font=dict(color="#8BA5C8",size=10),
                                orientation="h", y=-0.15))
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

            # Mini resumen textual bajo la gráfica
            gp_color = "#2ECC87" if gp_per>=0 else "#E85555"
            st.markdown(f"""<div style="display:flex;gap:24px;flex-wrap:wrap;padding:8px 4px">
              <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">INVERTIDO</div>
                <div style="font:600 14px IBM Plex Mono,mono;color:var(--text)">{money(inv_per,factor)}{sfx}</div></div>
              <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">VALOR HOY</div>
                <div style="font:600 14px IBM Plex Mono,mono;color:var(--text)">{money(act_per,factor)}{sfx}</div></div>
              <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">GANANCIA TOTAL</div>
                <div style="font:600 14px IBM Plex Mono,mono;color:{gp_color}">
                  {'+'if gp_per>=0 else ''}{money(gp_per,factor)}{sfx} ({'+' if rend_per>=0 else ''}{rend_per:.2f}%)</div></div>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Registra tu primera inversión para ver la gráfica.")

    with cr:
        pos_ab_activas = [p for p in posiciones if p["Estado"]=="Abierta"]
        vista_donut = st.radio("Ver distribución por",
                               ["📊 Activo/Ticker","🏷 Categoría"],
                               horizontal=True, key="donut_vista",
                               label_visibility="collapsed")
        if pos_ab_activas:
            PALETTE = ["#C8A84B","#2ECC87","#6BA3BE","#9B8EC4","#E87844","#E85555","#F0C040","#8BA5C8","#FF9F43","#A29BFE"]
            if vista_donut == "📊 Activo/Ticker":
                labels_d = [p["Activo"] for p in pos_ab_activas]
                values_d = [p["Val_Actual"]*factor for p in pos_ab_activas]
                colors_d = [PALETTE[i%len(PALETTE)] for i in range(len(labels_d))]
                titulo_d = "% por activo (posiciones abiertas)"
            else:
                dist_cat = {}
                for p in pos_ab_activas:
                    c = p["Categoria"]
                    dist_cat[c] = dist_cat.get(c,0) + p["Val_Actual"]*factor
                labels_d = list(dist_cat.keys())
                values_d = list(dist_cat.values())
                colors_d = [CAT_CLR_MAP.get(c, "#8BA5C8") for c in labels_d]
                titulo_d = "% por categoría (posiciones abiertas)"

            fig2 = go.Figure(go.Pie(
                labels=labels_d, values=values_d, hole=.55,
                marker=dict(colors=colors_d, line=dict(color="#111827",width=2)),
                textinfo="percent+label",
                textfont=dict(color="#ffffff", size=10),
                textposition="inside",
                insidetextorientation="horizontal",
                hovertemplate="<b>%{label}</b><br>%{value:$,.2f}"+sfx+"<br>%{percent}<extra></extra>",
            ))
            fig2.update_layout(**PT,
                title=dict(text=titulo_d, font=dict(size=11,color="#8BA5C8"),x=.5),
                showlegend=True,
                legend=dict(font=dict(color="#ffffff",size=10),bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        elif posiciones:
            st.info("Todas las posiciones están cerradas.")
        else:
            st.info("Sin posiciones registradas.")

    # Precios en tiempo real
    if prices:
        sec("Precios en tiempo real")
        st.markdown('<div style="font:400 10px IBM Plex Mono,mono;color:#8BA5C8;margin:-8px 0 10px">% = variación del día (no es tu P&L total)</div>', unsafe_allow_html=True)
        cols_p = st.columns(min(len(prices),5))
        for i,(tk,d) in enumerate(list(prices.items())[:10]):
            chg=d.get("chg24",0); px=d.get("price",0)
            clr="#2ECC87" if chg>=0 else "#E85555"
            pxs=f"${px:,.4f}" if px<10 else f"${px:,.2f}"
            # Buscar P&L real de esta posición
            pnl_real = next((p["GP_pct"] for p in posiciones
                             if p["Ticker"].upper()==tk.upper() and p["Estado"]=="Abierta"), None)
            pnl_html = f'<div style="font:400 9px IBM Plex Mono,mono;color:{"#2ECC87" if pnl_real>=0 else "#E85555"}">P&L: {"+" if pnl_real>=0 else ""}{pnl_real:.2f}%</div>' if pnl_real is not None else ""
            with cols_p[i%min(len(prices),5)]:
                st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
                    border-radius:8px;padding:12px;text-align:center;margin-bottom:8px">
                  <div style="font:600 11px/1.5 IBM Plex Mono,mono;color:#C8A84B">{tk}</div>
                  <div style="font:600 15px/1.4 IBM Plex Mono,mono;color:var(--text)">{pxs}</div>
                  <div style="font:400 10px/1.3 IBM Plex Mono,mono;color:{clr}">
                    {'▲' if chg>=0 else '▼'} {abs(chg):.2f}% hoy</div>
                  {pnl_html}</div>""",
                    unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# PORTAFOLIO — posiciones con P&L en vivo
# ══════════════════════════════════════════════════════
with t_port:
    if pos_ab_per:
        sec("Posiciones abiertas — P&L en tiempo real")
        for p in pos_ab_per:
            gc2 = "#2ECC87" if p["GP_usd"]>=0 else "#E85555"
            sg  = "+" if p["GP_usd"]>=0 else ""
            pxd = prices.get(p["Ticker"].upper(), {})
            px_str = f"${p['Px_Actual']:,.4f}" if p["Px_Actual"]<10 else f"${p['Px_Actual']:,.2f}"
            chg_str = f"{'▲' if p['Chg24']>=0 else '▼'} {abs(p['Chg24']):.2f}%" if p["Chg24"]!=0 else "—"
            chg_clr = "#2ECC87" if p["Chg24"]>=0 else "#E85555"

            st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
                border-radius:10px;padding:14px 18px;margin-bottom:10px;
                display:flex;align-items:center;gap:16px;flex-wrap:wrap">
              <div style="min-width:120px">
                <div style="font:600 15px/1.3 IBM Plex Mono,mono;color:#C8A84B">{p['Activo']}</div>
                <div style="font:400 10px/1.4 IBM Plex Mono,mono;color:#8BA5C8">
                  {p['Ticker']} · {p['Categoria']}</div>
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">Compra: {p['F_Compra']}</div>
              </div>
              <div style="text-align:center;min-width:80px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">CANTIDAD</div>
                <div style="font:500 13px IBM Plex Mono,mono;color:var(--text)">{p['Cantidad']:,.4f}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">PX COMPRA</div>
                <div style="font:500 13px IBM Plex Mono,mono;color:var(--text)">${p['Px_Compra']:,.4f}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">PX ACTUAL</div>
                <div style="font:500 13px IBM Plex Mono,mono;color:var(--text)">{px_str}</div>
                <div style="font:400 9px IBM Plex Mono,mono;color:{chg_clr}">{chg_str} 24h</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">INVERTIDO</div>
                <div style="font:500 13px IBM Plex Mono,mono;color:var(--text)">{money(p['Invertido'],factor)}{sfx}</div>
              </div>
              <div style="text-align:center;min-width:100px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">VALOR HOY</div>
                <div style="font:600 14px IBM Plex Mono,mono;color:var(--text)">{money(p['Val_Actual'],factor)}{sfx}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8;letter-spacing:1px">P&L</div>
                <div style="font:600 15px IBM Plex Mono,mono;color:{gc2}">{sg}{money(p['GP_usd'],factor)}{sfx}</div>
                <div style="font:600 13px IBM Plex Mono,mono;color:{gc2}">{sg}{p['GP_pct']:.2f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)

    if pos_cer_per:
        sec("Posiciones cerradas")
        for p in pos_cer_per:
            gc3 = "#2ECC87" if p["GP_usd"]>=0 else "#E85555"
            sg3 = "+" if p["GP_usd"]>=0 else ""
            st.markdown(f"""<div style="background:#0F1A2B;border:1px solid #1E3354;
                border-radius:10px;padding:12px 18px;margin-bottom:8px;
                display:flex;align-items:center;gap:16px;flex-wrap:wrap;opacity:.9">
              <div style="min-width:120px">
                <div style="font:600 14px/1.3 IBM Plex Mono,mono;color:#8BA5C8">{p['Activo']}</div>
                <div style="font:400 10px IBM Plex Mono,mono;color:#4a6f8a">{p['Ticker']} · {p['Categoria']}</div>
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">
                  {p['F_Compra']} → {p['F_Venta']}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">PX COMPRA</div>
                <div style="font:500 12px IBM Plex Mono,mono;color:#8BA5C8">${p['Px_Compra']:,.4f}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">PX VENTA</div>
                <div style="font:500 12px IBM Plex Mono,mono;color:#8BA5C8">${p['Px_Actual']:,.4f}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">INVERTIDO</div>
                <div style="font:500 12px IBM Plex Mono,mono;color:#8BA5C8">{money(p['Invertido'],factor)}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">RECUPERADO</div>
                <div style="font:500 12px IBM Plex Mono,mono;color:#8BA5C8">{money(p['Val_Actual'],factor)}</div>
              </div>
              <div style="text-align:center;min-width:90px">
                <div style="font:400 9px IBM Plex Mono,mono;color:#4a6f8a">RESULTADO</div>
                <div style="font:600 14px IBM Plex Mono,mono;color:{gc3}">{sg3}{money(p['GP_usd'],factor)}{sfx}</div>
                <div style="font:500 10px IBM Plex Mono,mono;color:{gc3}">{sg3}{p['GP_pct']:.2f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)

    if not posiciones:
        st.info("Aún no tienes inversiones registradas.")

# ══════════════════════════════════════════════════════
# REGISTRAR INVERSIÓN
# ══════════════════════════════════════════════════════
if puede_registrar:
    with t_reg:
        sec("Registrar compra de activo")
        st.markdown(f'<div style="font:400 11px/1.5 IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:10px">'
                    f'Usuario: <strong style="color:#C8A84B">{usuario}</strong> · '
                    f'Fondo: <strong style="color:#C8A84B">{fondo}</strong></div>',
                    unsafe_allow_html=True)

        with st.form("form_compra", clear_on_submit=True):
            c1,c2,c3 = st.columns(3)
            fecha_c   = c1.date_input("📅 Fecha de compra / inversión", value=date.today())
            activo    = c2.text_input("Nombre del activo / inversión",
                placeholder="Apple, Bitcoin, Apartamento Bogotá, Finca La Esperanza…")
            categoria = c3.selectbox("Categoría", CATEGORIAS)

            # Detectar si es activo de mercado o activo real/tradicional
            es_mercado = categoria not in CATS_MANUALES
            es_cdt     = categoria in ["CDT","Cuenta Remunerada"]

            if es_mercado and not es_cdt:
                # Mercado: precio por unidad + capital → calcula cantidad
                st.markdown("""<div style="font:400 11px IBM Plex Mono,mono;color:#8BA5C8;
                    margin:-4px 0 8px;padding:8px 12px;background:var(--surface);
                    border-left:3px solid #C8A84B;border-radius:0 6px 6px 0">
                  <strong>Activo de mercado</strong> — ingresa el precio por unidad y el capital.
                  La cantidad se calcula automáticamente.</div>""", unsafe_allow_html=True)
                c4,c5,c6 = st.columns(3)
                precio_c  = c4.number_input("Precio por unidad (USD)", min_value=0.0,
                                             step=0.0001, format="%.4f")
                valor_pos = c5.number_input("Capital invertido (USD)", min_value=0.0,
                                             step=0.01, format="%.2f")
                broker    = c6.text_input("Broker / Exchange", placeholder="Schwab, Binance…")
                c7,c8     = st.columns(2)
                ticker_api= c7.text_input("Ticker para precio en vivo",
                                           placeholder="AAPL · BTC · VTI · ETH",
                                           help="Símbolo exacto para obtener precio automático")
                notas     = c8.text_input("Notas (opcional)")
                qty       = round(valor_pos / precio_c, 8) if precio_c > 0 and valor_pos > 0 else 0.0
                st.text_input("Cantidad calculada automáticamente",
                              value=f"{qty:,.8f}  =  ${valor_pos:,.2f} ÷ ${precio_c:,.4f}",
                              disabled=True)
                precio_registro = precio_c
                qty_registro    = qty

            elif es_cdt:
                # CDT/Remunerada: capital + TEA anual
                st.markdown("""<div style="font:400 11px IBM Plex Mono,mono;color:#8BA5C8;
                    margin:-4px 0 8px;padding:8px 12px;background:var(--surface);
                    border-left:3px solid #6BA3BE;border-radius:0 6px 6px 0">
                  <strong>CDT / Cuenta Remunerada</strong> — ingresa el capital y la tasa anual.
                  El valor crece automáticamente con el tiempo.</div>""", unsafe_allow_html=True)
                c4,c5,c6  = st.columns(3)
                tea_pct   = c4.number_input("Tasa anual % (TEA)", min_value=0.0,
                                             max_value=100.0, step=0.01, format="%.2f",
                                             help="Ej: 12.85 para 12.85% anual")
                valor_pos = c5.number_input("Capital invertido (USD)", min_value=0.0,
                                             step=0.01, format="%.2f")
                broker    = c6.text_input("Entidad financiera", placeholder="Bancolombia, Nubank…")
                notas     = st.text_input("Notas (opcional)")
                ticker_api= ""
                precio_registro = tea_pct / 100  # guardamos TEA como precio
                qty_registro    = valor_pos       # cantidad = capital total

            else:
                # Activos reales: inmueble, negocio, ganado, vehículo, etc.
                cat_labels = {
                    "Inmueble": "🏠 Inmueble (apartamento, casa, lote, finca…)",
                    "Negocio":  "🏢 Negocio (empresa, local, participación…)",
                    "Ganadería":"🐄 Ganadería / Criadero",
                    "Vehículo": "🚗 Vehículo en alquiler",
                    "Dividendo":"💰 Dividendo / Herencia / Fideicomiso",
                    "Seguro":   "🛡 Seguro en dólares / Póliza",
                    "Arriendo": "🏘 Ingreso por arrendamiento",
                    "Otro":     "📦 Otro activo real",
                }
                lbl = cat_labels.get(categoria, categoria)
                st.markdown(f"""<div style="font:400 11px IBM Plex Mono,mono;color:#8BA5C8;
                    margin:-4px 0 8px;padding:8px 12px;background:var(--surface);
                    border-left:3px solid #E87844;border-radius:0 6px 6px 0">
                  <strong>{lbl}</strong> — ingresa el valor total de la inversión.
                  Actualiza el valor manualmente cuando cambie.</div>""", unsafe_allow_html=True)
                c4,c5,c6  = st.columns(3)
                valor_pos = c4.number_input("Valor total invertido (USD)", min_value=0.0,
                                             step=0.01, format="%.2f",
                                             help="Ej: costo del apartamento, valor del negocio…")
                valor_act = c5.number_input("Valor actual estimado (USD)", min_value=0.0,
                                             step=0.01, format="%.2f",
                                             help="Si es diferente al de compra. Si es igual, deja en 0.")
                broker    = c6.text_input("Ubicación / Intermediario",
                                           placeholder="Ciudad, banco, corredor…")
                c7,c8     = st.columns(2)
                ingreso_m = c7.number_input("Ingreso mensual (arriendo/dividendo, USD)",
                                             min_value=0.0, step=0.01, format="%.2f",
                                             help="Si genera ingreso periódico. Opcional.")
                notas     = c8.text_input("Descripción / notas")
                ticker_api= ""
                # Para activos manuales: precio_compra = valor invertido, cantidad = 1
                precio_registro = valor_pos
                qty_registro    = 1.0
                # El valor actual se guarda en notas si es diferente
                notas_final = notas.strip()
                if valor_act > 0 and valor_act != valor_pos:
                    notas_final += f" | Valor actual: ${valor_act:,.2f}"
                if ingreso_m > 0:
                    notas_final += f" | Ingreso mensual: ${ingreso_m:,.2f}/mes"

            if st.form_submit_button("💾 REGISTRAR INVERSIÓN", use_container_width=True):
                if not activo.strip():
                    st.error("❌ El nombre es obligatorio")
                elif valor_pos <= 0:
                    st.error("❌ El capital invertido debe ser mayor a 0")
                else:
                    notas_save = notas.strip() if es_mercado or es_cdt else notas_final
                    ok, msg = fs_post("inversiones", {
                        "Fondo":         fondo,
                        "Usuario":       usuario,
                        "Fecha_Compra":  str(fecha_c),
                        "Activo":        activo.strip(),
                        "Categoria":     categoria,
                        "Cantidad":      float(qty_registro),
                        "Precio_Compra": float(precio_registro),
                        "Broker":        broker.strip(),
                        "Ticker_API":    ticker_api.strip().upper() if ticker_api else "",
                        "Fecha_Venta":   "",
                        "Precio_Venta":  0.0,
                        "Estado":        "Abierta",
                        "Notas":         notas_save,
                    })
                    if ok:
                        st.success(f"✓ {activo} registrado correctamente")
                        st.cache_data.clear(); time.sleep(0.5); st.rerun()
                    else:
                        st.error(f"❌ Error Firestore: {msg}")

        # ── REGISTRAR VENTA ──
        if posiciones:
            abiertas_lista = [p for p in posiciones if p["Estado"]=="Abierta" and p["Estado"]!="Archivada"]
            if abiertas_lista:
                st.markdown("---")
                sec("Registrar venta de activo")
                # Buscador por nombre de activo
                buscar_activo = st.text_input("🔍 Buscar activo",
                    placeholder="Escribe nombre para filtrar…",
                    key="buscar_venta")
                abiertas_filtradas = [p for p in abiertas_lista
                    if buscar_activo.strip().lower() in p["Activo"].lower()]                     if buscar_activo.strip() else abiertas_lista

                if not abiertas_filtradas:
                    st.warning(f"No se encontró '{buscar_activo}' en posiciones abiertas.")
                    abiertas_filtradas = abiertas_lista  # fallback a todas

                lbs = [f"{p['F_Compra']} — {p['Activo']} ({p['Cantidad']:,.4f} uds · ${p['Px_Compra']:,.4f})"
                       for p in abiertas_filtradas]
                sel = st.selectbox("Selecciona la posición a vender", range(len(lbs)),
                                   format_func=lambda i: lbs[i])
                pos_sel = abiertas_filtradas[sel]

                cv1,cv2 = st.columns(2)
                fecha_v  = cv1.date_input("📅 Fecha de venta", value=date.today())
                precio_v = cv2.number_input("Precio de venta (USD)", min_value=0.0,
                                             step=0.0001, format="%.4f")

                if precio_v > 0:
                    gp_venta = (precio_v - pos_sel["Px_Compra"]) * pos_sel["Cantidad"]
                    gp_pct_v = gp_venta / pos_sel["Invertido"] * 100 if pos_sel["Invertido"] else 0
                    clr_v    = "#2ECC87" if gp_venta >= 0 else "#E85555"
                    st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
                        border-radius:8px;padding:12px 16px;margin:8px 0;
                        display:flex;gap:24px;flex-wrap:wrap">
                      <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8">RESULTADO VENTA</div>
                        <div style="font:600 16px IBM Plex Mono,mono;color:{clr_v}">
                          {'+'if gp_venta>=0 else ''}{money(gp_venta,factor)}{sfx}</div></div>
                      <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8">RENTABILIDAD</div>
                        <div style="font:600 16px IBM Plex Mono,mono;color:{clr_v}">
                          {'+'if gp_pct_v>=0 else ''}{gp_pct_v:.2f}%</div></div>
                      <div><div style="font:400 9px IBM Plex Mono,mono;color:#8BA5C8">CAPITAL RECUPERADO</div>
                        <div style="font:600 16px IBM Plex Mono,mono;color:var(--text)">
                          {money(precio_v*pos_sel['Cantidad'],factor)}{sfx}</div></div>
                    </div>""", unsafe_allow_html=True)

                if st.button("💰 CONFIRMAR VENTA", use_container_width=True):
                    if precio_v <= 0:
                        st.error("❌ Ingresa el precio de venta")
                    else:
                        _id = pos_sel["_id"]
                        datos_venta = {
                            "Estado":       "Cerrada",
                            "Fecha_Venta":  str(fecha_v),
                            "Precio_Venta": float(precio_v),
                        }
                        if _id.startswith("ops_"):
                            # Viene de colección 'operaciones' — guardar como nueva inversión cerrada
                            real_id = _id.replace("ops_","",1)
                            ok2, msg2 = fs_post("inversiones", {
                                "Fondo":         pos_sel.get("Usuario","").split("@")[0] if not fondo else fondo,
                                "Usuario":       pos_sel.get("Usuario", usuario),
                                "Fecha_Compra":  pos_sel["F_Compra"],
                                "Activo":        pos_sel["Activo"],
                                "Categoria":     pos_sel["Categoria"],
                                "Cantidad":      float(pos_sel["Cantidad"]),
                                "Precio_Compra": float(pos_sel["Px_Compra"]),
                                "Broker":        pos_sel.get("Broker",""),
                                "Ticker_API":    pos_sel["Ticker"],
                                "Fecha_Venta":   str(fecha_v),
                                "Precio_Venta":  float(precio_v),
                                "Estado":        "Cerrada",
                                "Notas":         f"Migrado de operaciones/{real_id}",
                            })
                            if ok2:
                                # Actualizar también en operaciones para consistencia
                                fs_patch("operaciones", real_id, {"Resultado": "Ganadora" if precio_v > pos_sel["Px_Compra"] else "Perdedora"})
                                st.success(f"✓ Venta de {pos_sel['Activo']} registrada — guardada en historial")
                                st.cache_data.clear(); time.sleep(0.5); st.rerun()
                            else:
                                st.error(f"❌ Error: {msg2}")
                        else:
                            # Nueva colección inversiones — patch directo
                            ok = fs_patch("inversiones", _id, datos_venta)
                            if ok:
                                st.success(f"✓ Venta de {pos_sel['Activo']} registrada el {fecha_v}")
                                st.cache_data.clear(); time.sleep(0.5); st.rerun()
                            else:
                                st.error("❌ Error actualizando")

            # ── EDITAR POSICIÓN ABIERTA (compra mal ingresada) ──
            pos_abiertas_edit = [p for p in posiciones if p["Estado"]=="Abierta" and not p["_id"].startswith("ops_")]
            if pos_abiertas_edit:
                st.markdown("---")
                sec("Editar compra registrada")
                st.markdown('<div style="font:400 11px IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:8px">Corrige precio, cantidad, ticker o fecha de una posición abierta.</div>', unsafe_allow_html=True)
                buscar_edit_ab = st.text_input("🔍 Buscar activo", placeholder="Filtrar…", key="buscar_edit_ab")
                pos_ab_f = [p for p in pos_abiertas_edit
                    if buscar_edit_ab.strip().lower() in p["Activo"].lower()]                     if buscar_edit_ab.strip() else pos_abiertas_edit
                if not pos_ab_f: pos_ab_f = pos_abiertas_edit
                lbs_ab_e = [f"{p['F_Compra']} — {p['Activo']} (${p['Px_Compra']:,.4f})" for p in pos_ab_f]
                sel_ab_e = st.selectbox("Posición a editar", range(len(lbs_ab_e)),
                                        format_func=lambda i: lbs_ab_e[i], key="sel_ab_e")
                if sel_ab_e is not None:
                    p_edit = pos_ab_f[sel_ab_e]
                    ea1,ea2,ea3,ea4 = st.columns(4)
                    try:
                        fecha_edit_default = pd.to_datetime(p_edit["F_Compra"]).date()
                    except:
                        fecha_edit_default = date.today()
                    nueva_fecha_c  = ea1.date_input("Fecha compra", value=fecha_edit_default, key="ef_c")
                    nuevo_precio_c = ea2.number_input("Precio compra", value=float(p_edit["Px_Compra"]),
                                                       min_value=0.0, step=0.0001, format="%.4f", key="ep_c")
                    nuevo_ticker   = ea3.text_input("Ticker", value=p_edit["Ticker"], key="et_c")
                    # Recalcular cantidad
                    val_orig = p_edit["Val_ent"]
                    nueva_qty = round(val_orig / nuevo_precio_c, 8) if nuevo_precio_c > 0 else p_edit["Cantidad"]
                    ea4.text_input("Nueva cantidad (auto)", value=f"{nueva_qty:,.8f}", disabled=True)
                    if st.button("✏️ ACTUALIZAR COMPRA", key="btn_edit_ab"):
                        ok = fs_patch("inversiones", p_edit["_id"], {
                            "Fecha_Compra":  str(nueva_fecha_c),
                            "Precio_Compra": float(nuevo_precio_c),
                            "Cantidad":      float(nueva_qty),
                            "Ticker_API":    nuevo_ticker.strip().upper(),
                        })
                        if ok:
                            st.success("✓ Compra actualizada correctamente")
                            st.cache_data.clear(); st.rerun()
                        else:
                            st.error("❌ Error actualizando")

            # ── EDITAR POSICIÓN CERRADA ──
            pos_cerradas_todas = [p for p in posiciones if p["Estado"]=="Cerrada"]
            if pos_cerradas_todas:
                st.markdown("---")
                sec("Editar posición cerrada")
                st.markdown('<div style="font:400 11px IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:8px">Corrige fecha o precio de venta de cualquier posición ya cerrada.</div>', unsafe_allow_html=True)
                buscar_cerrada = st.text_input("🔍 Buscar activo cerrado",
                    placeholder="Escribe nombre para filtrar…", key="buscar_cerrada")
                pos_cerradas_filtradas = [p for p in pos_cerradas_todas
                    if buscar_cerrada.strip().lower() in p["Activo"].lower()]                     if buscar_cerrada.strip() else pos_cerradas_todas
                if not pos_cerradas_filtradas:
                    pos_cerradas_filtradas = pos_cerradas_todas
                lbs_c = [f"{p['F_Compra']} → {p['F_Venta']} — {p['Activo']} (a ${p['Px_Actual']:,.4f})"
                         for p in pos_cerradas_filtradas]
                sel_c = st.selectbox("Selecciona posición cerrada", range(len(lbs_c)),
                                     format_func=lambda i: lbs_c[i], key="sel_cerrada")
                pc_sel = pos_cerradas_filtradas[sel_c]
                ec1,ec2 = st.columns(2)
                nueva_fv = ec1.date_input("Nueva fecha de venta",
                                          value=pd.to_datetime(pc_sel["F_Venta"]).date()
                                          if pc_sel["F_Venta"] else date.today(),
                                          key="edit_fv")
                nuevo_pv = ec2.number_input("Nuevo precio de venta (USD)",
                                            value=float(pc_sel["Px_Actual"]) if pc_sel["Px_Actual"] else 0.0,
                                            min_value=0.0, step=0.0001, format="%.4f", key="edit_pv")
                if st.button("✏️ ACTUALIZAR POSICIÓN CERRADA"):
                    _id_c = pc_sel["_id"]
                    datos_edit = {"Fecha_Venta": str(nueva_fv), "Precio_Venta": float(nuevo_pv), "Estado": "Cerrada"}
                    if _id_c.startswith("ops_"):
                        # Legacy: crear/actualizar en inversiones
                        ok2, msg2 = fs_post("inversiones", {
                            "Fondo": fondo, "Usuario": usuario,
                            "Fecha_Compra": pc_sel["F_Compra"], "Activo": pc_sel["Activo"],
                            "Categoria": pc_sel["Categoria"], "Cantidad": float(pc_sel["Cantidad"]),
                            "Precio_Compra": float(pc_sel["Px_Compra"]), "Broker": "",
                            "Ticker_API": pc_sel["Ticker"], "Fecha_Venta": str(nueva_fv),
                            "Precio_Venta": float(nuevo_pv), "Estado": "Cerrada",
                            "Notas": f"Editado desde operaciones/{_id_c.replace('ops_','')}",
                        })
                        if ok2: st.success("✓ Posición actualizada"); st.cache_data.clear(); st.rerun()
                        else:   st.error(f"❌ {msg2}")
                    else:
                        ok = fs_patch("inversiones", _id_c, datos_edit)
                        if ok: st.success("✓ Posición actualizada"); st.cache_data.clear(); st.rerun()
                        else:  st.error("❌ Error actualizando")

            # Archivar / Desarchivar posición
            st.markdown("---")
            col_arc, col_dearc = st.columns(2)

            with col_arc:
                sec("Archivar posición")
                st.markdown('''<div style="font:400 11px IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:8px">
                  Saca la posición del fondo. No cuenta en totales.
                  Queda en historial. Nunca se borra.</div>''', unsafe_allow_html=True)
                activas_arc = [p for p in posiciones if p["Estado"] != "Archivada"]
                if activas_arc:
                    buscar_arc = st.text_input("🔍 Buscar activo",
                        placeholder="Filtrar por nombre…", key="buscar_arc")
                    activas_arc_f = [p for p in activas_arc
                        if buscar_arc.strip().lower() in p["Activo"].lower()]                         if buscar_arc.strip() else activas_arc
                    if not activas_arc_f: activas_arc_f = activas_arc
                    lbs_arc = [f"{p['F_Compra']} — {p['Activo']} ({p['Estado']})" for p in activas_arc_f]
                    arc_sel = st.selectbox("Posición a archivar", range(len(lbs_arc)),
                                           format_func=lambda i: lbs_arc[i], key="arc_pos")
                    if st.button("📦 ARCHIVAR"):
                        _id_a = activas_arc_f[arc_sel]["_id"]
                        col = "inversiones" if not _id_a.startswith("ops_") else "operaciones"
                        real_id = _id_a.replace("ops_","",1) if _id_a.startswith("ops_") else _id_a
                        fs_patch(col, real_id, {"Estado": "Archivada"})
                        st.success("✓ Archivada"); st.cache_data.clear(); st.rerun()
                else:
                    st.info("No hay posiciones para archivar.")

            with col_dearc:
                sec("Desarchivar posición")
                st.markdown('''<div style="font:400 11px IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:8px">
                  Reactiva una posición archivada. Vuelve a contar
                  en el portafolio con todos sus datos intactos.</div>''', unsafe_allow_html=True)
                archivadas = [p for p in posiciones if p["Estado"] == "Archivada"]
                if archivadas:
                    lbs_da = [f"{p['F_Compra']} — {p['Activo']}" for p in archivadas]
                    da_sel = st.selectbox("Posición a desarchivar", range(len(lbs_da)),
                                          format_func=lambda i: lbs_da[i], key="dearc_pos")
                    # Determinar si tenía fecha de venta para restaurar al estado correcto
                    p_da = archivadas[da_sel]
                    estado_restaurar = "Cerrada" if p_da.get("F_Venta") else "Abierta"
                    st.markdown(f'<div style="font:400 10px IBM Plex Mono,mono;color:#C8A84B;margin-bottom:6px">'
                                f'Se restaurará como: <strong>{estado_restaurar}</strong></div>',
                                unsafe_allow_html=True)
                    if st.button("♻️ DESARCHIVAR"):
                        _id_da = p_da["_id"]
                        col_da = "inversiones" if not _id_da.startswith("ops_") else "operaciones"
                        real_da = _id_da.replace("ops_","",1) if _id_da.startswith("ops_") else _id_da
                        fs_patch(col_da, real_da, {"Estado": estado_restaurar})
                        st.success(f"✓ Restaurada como {estado_restaurar}")
                        st.cache_data.clear(); st.rerun()
                else:
                    st.info("No hay posiciones archivadas.")

# ══════════════════════════════════════════════════════
# CAPITAL — disponible para admin y portafolio individual
# Lógica: compra → capital invertido sube automáticamente
#         depósito → cash disponible (aún no invertido)
#         retiro → baja el valor real del portafolio
# ══════════════════════════════════════════════════════
if rol == "admin" or puede_registrar:
    with t_cap:
        # Resumen de cash actual
        cap1, cap2, cap3 = st.columns(3)
        with cap1:
            st.markdown(card("Depósitos acumulados",
                money(cash_aportes, factor)+sfx, color="#2ECC87"), unsafe_allow_html=True)
        with cap2:
            st.markdown(card("Retiros acumulados",
                money(cash_retiros, factor)+sfx, color="#E85555"), unsafe_allow_html=True)
        with cap3:
            cn_color = "#2ECC87" if cash_neto >= 0 else "#E85555"
            st.markdown(card("Cash neto disponible",
                money(cash_neto, factor)+sfx,
                "Depósitos - Retiros", color=cn_color), unsafe_allow_html=True)

        st.markdown("""<div style="background:#162236;border:1px solid #1E3354;
            border-left:3px solid #C8A84B;border-radius:0 8px 8px 0;
            padding:10px 14px;margin:14px 0;font:400 11px/1.7 IBM Plex Mono,mono;color:#B0C4DC">
          <strong>Depósito:</strong> ingresaste dinero a la cuenta (aún no invertido en activos).<br>
          <strong>Retiro:</strong> sacaste dinero de la cuenta → el portafolio baja en ese monto.<br>
          Las compras de activos ya quedan registradas automáticamente al registrar una inversión.
        </div>""", unsafe_allow_html=True)

        sec("Registrar movimiento de dinero")
        with st.form("form_cap", clear_on_submit=True):
            cc1,cc2,cc3 = st.columns(3)
            tipo_mov = cc1.selectbox("Tipo de movimiento",
                ["Depósito","Retiro"],
                help="Deposito: ingresaste dinero. Retiro: sacaste dinero de la cuenta.")
            monto_cap = cc2.number_input("Monto (USD)", min_value=0.01, step=0.01, format="%.2f")
            fecha_cap = cc3.date_input("Fecha", value=date.today())

            cc4, cc5 = st.columns(2)
            concepto  = cc4.text_input("Concepto / descripción",
                placeholder="Ej: Transferencia inicial, retiro mensual…")
            broker_cap= cc5.text_input("Broker / Banco", placeholder="Schwab, Nubank, Bancolombia…")

            # Si es admin, puede registrar para un socio específico
            if rol == "admin":
                cc6,cc7 = st.columns(2)
                socio_cap = cc6.text_input("Nombre del socio", placeholder="Nombre o razón social")
                cedula_cap= cc7.text_input("Cédula / ID")
            else:
                socio_cap  = usuario.split("@")[0]
                cedula_cap = ""

            if st.form_submit_button("💾 REGISTRAR MOVIMIENTO", use_container_width=True):
                if monto_cap <= 0:
                    st.error("❌ El monto debe ser mayor a 0")
                else:
                    # Normalizamos: Depósito → Aporte, Retiro → Retiro
                    tipo_fs = "Aporte" if tipo_mov == "Depósito" else "Retiro"
                    ok, msg = fs_post("aportes", {
                        "Fondo":    fondo,
                        "Socio":    socio_cap,
                        "Cedula":   cedula_cap,
                        "Fecha":    str(fecha_cap),
                        "Tipo":     tipo_fs,
                        "Monto":    float(monto_cap),
                        "Concepto": concepto.strip(),
                        "Broker":   broker_cap.strip(),
                        "Usuario":  usuario,
                    })
                    if ok:
                        signo = "+" if tipo_fs=="Aporte" else "-"
                        st.success(f"✓ {tipo_mov} de {signo}{money(monto_cap,factor)}{sfx} registrado")
                        st.cache_data.clear(); st.rerun()
                    else:
                        st.error(f"❌ Error Firestore: {msg}")

        # Historial de movimientos
        if not df_ap.empty:
            st.markdown("---")
            sec("Historial de movimientos de capital")
            # Filtrar por usuario si no es admin
            dfh = df_ap.copy()
            if rol != "admin" and "Usuario" in dfh.columns:
                dfh = dfh[dfh["Usuario"] == usuario]
            cols_h = [c for c in ["Fecha","Socio","Tipo","Monto","Concepto","Broker"] if c in dfh.columns]
            dfh = dfh[cols_h].sort_values("Fecha", ascending=False).copy()
            if "Monto" in dfh.columns:
                dfh["Monto"] = dfh["Monto"] * factor

            def ct(v):
                if v=="Aporte":  return "color:#2ECC87;font-weight:600"
                if v=="Retiro":  return "color:#E85555;font-weight:600"
                return ""
            styled_h = dfh.style.format({"Monto":"${:,.2f}"})
            if "Tipo" in dfh.columns:
                styled_h = styled_h.map(ct, subset=["Tipo"])
            st.dataframe(styled_h, use_container_width=True, hide_index=True)

            # Resumen por tipo
            if "Tipo" in dfh.columns and len(dfh) > 0:
                total_dep = df_ap[df_ap["Tipo"]=="Aporte"]["Monto"].sum() * factor
                total_ret = df_ap[df_ap["Tipo"]=="Retiro"]["Monto"].sum() * factor
                st.markdown(f"""<div style="display:flex;gap:20px;margin-top:10px;flex-wrap:wrap">
                  <div style="font:400 10px IBM Plex Mono,mono;color:#2ECC87">
                    ▲ Total depósitos: <strong>{money(total_dep)}{sfx}</strong></div>
                  <div style="font:400 10px IBM Plex Mono,mono;color:#E85555">
                    ▼ Total retiros: <strong>{money(total_ret)}{sfx}</strong></div>
                  <div style="font:400 10px IBM Plex Mono,mono;color:#8BA5C8">
                    = Cash neto: <strong style="color:{"#2ECC87" if total_dep-total_ret>=0 else "#E85555"}">
                    {money(total_dep-total_ret)}{sfx}</strong></div>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# USUARIOS (admin)
# ══════════════════════════════════════════════════════
if rol == "admin":
    with t_usr:
        sec("Gestión de usuarios")
        st.markdown("""<div style="background:#162236;border:1px solid #1E3354;border-left:3px solid #C8A84B;
            border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:14px;
            font:400 12px/1.7 IBM Plex Mono,mono;color:#B0C4DC">
          <strong>Portafolio Individual</strong> → el usuario entra y registra sus propias inversiones.<br>
          <strong>Observador de Fondo</strong> → solo lectura. Ve el fondo asignado sin poder editar.
        </div>""", unsafe_allow_html=True)

        with st.form("form_usr", clear_on_submit=True):
            cu1,cu2 = st.columns(2)
            u_email  = cu1.text_input("Email del usuario")
            u_nombre = cu2.text_input("Nombre / Empresa")
            cu3,cu4,cu5 = st.columns(3)
            u_pwd   = cu3.text_input("Contraseña inicial", type="password", help="Mínimo 6 caracteres")
            u_modo  = cu4.selectbox("Modo de acceso", [MODO_IND, MODO_OBS])
            u_f_opts= ["(Sin fondo — portafolio personal)"] + fondos_list
            u_fsel  = cu5.selectbox("Fondo asignado (opcional)", u_f_opts)
            u_fondo = "" if u_fsel.startswith("(Sin") else u_fsel

            if st.form_submit_button("👤 CREAR USUARIO", use_container_width=True):
                if not u_email.strip() or not u_nombre.strip() or not u_pwd.strip():
                    st.error("❌ Email, nombre y contraseña obligatorios")
                elif len(u_pwd) < 6:
                    st.error("❌ Contraseña mínimo 6 caracteres")
                elif u_modo == MODO_OBS and not u_fondo:
                    st.error("❌ Observador de Fondo requiere un fondo asignado")
                else:
                    with st.spinner("Creando en Firebase…"):
                        ok_fb, msg_fb = firebase_crear(u_email.strip(), u_pwd.strip())
                    if ok_fb or "EMAIL_EXISTS" in str(msg_fb):
                        fs_post("usuarios", {
                            "Email": u_email.strip().lower(), "Nombre": u_nombre.strip(),
                            "Modo": u_modo, "Fondo": u_fondo, "Activo": "Si",
                            "CreadoPor": usuario, "Fecha": str(date.today()),
                        })
                        lbl = "EMAIL_EXISTS" in str(msg_fb) and "actualizado" or "creado"
                        st.success(f"✓ Usuario {lbl}: {u_email} → {u_modo}" +
                                   (f" · Fondo: {u_fondo}" if u_fondo else " · Portafolio personal"))
                        st.cache_data.clear()
                    else:
                        st.error(f"❌ Firebase: {msg_fb}")

        df_u2 = load_usuarios()
        if not df_u2.empty:
            st.markdown("---"); sec("Usuarios registrados")
            cols_u = [c for c in ["Email","Nombre","Modo","Fondo","Fecha"] if c in df_u2.columns]
            st.dataframe(df_u2[cols_u], use_container_width=True, hide_index=True)
            sel_del = st.selectbox("Eliminar usuario",
                                   range(len(df_u2)),
                                   format_func=lambda i: f"{df_u2.iloc[i].get('Email','?')} — {df_u2.iloc[i].get('Nombre','?')}")
            if st.button("🗑 Eliminar acceso"):
                fs_delete("usuarios", df_u2.iloc[sel_del]["_id"])
                st.success("✓ Eliminado"); st.cache_data.clear(); st.rerun()

# ══════════════════════════════════════════════════════
# ADMINISTRACIÓN (admin)
# ══════════════════════════════════════════════════════
if rol == "admin":
    with t_adm:
        sec("Panel de administración")
        ca1,ca2 = st.columns(2)
        with ca1:
            sec("Resumen por fondo")
            rows_r = []
            for f in fondos_list:
                inv_f = df_inv_all[df_inv_all["Fondo"]==f] if not df_inv_all.empty else pd.DataFrame()
                n_inv = len(inv_f)
                rows_r.append({"Fondo":f,"# Inversiones":n_inv})
            st.dataframe(pd.DataFrame(rows_r), use_container_width=True, hide_index=True)

            sec("Crear nuevo fondo")
            nf = st.text_input("Nombre del fondo", key="nf_adm")
            if st.button("➕ CREAR FONDO"):
                if nf.strip() and nf not in fondos_list:
                    fs_post("aportes",{"Fondo":nf.strip(),"Socio":"","Cedula":"",
                                       "Fecha":str(date.today()),"Tipo":"Aporte",
                                       "Monto":0.0,"Usuario":usuario})
                    st.success(f"✓ Fondo '{nf}' creado")
                    st.cache_data.clear(); st.rerun()

        with ca2:
            sec("APIs activas")
            st.markdown(f"""<div style="background:#162236;border:1px solid #1E3354;
                border-radius:8px;padding:14px;font:400 11px/2 IBM Plex Mono,mono">
              <div style="color:#8BA5C8;font-size:9px;letter-spacing:1px;margin-bottom:8px">FUENTES</div>
              <div style="color:#F0C040">● CoinMarketCap — Cripto</div>
              <div style="color:#C8A84B">● Yahoo Finance — Acciones / ETF</div>
              <div style="color:#2ECC87">● ExchangeRate-API — TRM</div>
              <div style="color:#8BA5C8;font-size:9px;margin-top:10px">
                TRM: ${trm:,.2f} · CMC: …{CMC_KEY[-6:]}</div></div>""",
                unsafe_allow_html=True)
            if st.button("🔄 Limpiar caché"):
                st.cache_data.clear(); st.success("✓ Caché limpiado")

        sec("Resumen de actividad (sin datos privados)")
        st.markdown('''<div style="font:400 11px IBM Plex Mono,mono;color:#8BA5C8;margin-bottom:10px">
          Por privacidad, los datos detallados de portafolios individuales no son visibles
          desde el panel de administración. Solo el cliente puede ver sus propias inversiones.
        </div>''', unsafe_allow_html=True)
        if not df_inv_all.empty:
            # Solo mostrar resumen agregado por fondo, sin detalles individuales
            resumen_act = []
            for f_r in fondos_list:
                inv_f = df_inv_all[df_inv_all["Fondo"] == f_r] if "Fondo" in df_inv_all.columns else pd.DataFrame()
                # Solo incluir fondos grupales (no personal_*)
                if f_r.startswith("personal_"):
                    resumen_act.append({"Fondo": f_r, "Tipo": "Personal (privado)",
                                        "# Posiciones": "🔒 Privado", "Estado": "—"})
                else:
                    n_ab  = len(inv_f[inv_f["Estado"]=="Abierta"])  if not inv_f.empty and "Estado" in inv_f.columns else 0
                    n_cer = len(inv_f[inv_f["Estado"]=="Cerrada"]) if not inv_f.empty and "Estado" in inv_f.columns else 0
                    resumen_act.append({"Fondo": f_r, "Tipo": "Grupal",
                                        "# Abiertas": n_ab, "# Cerradas": n_cer})
            st.dataframe(pd.DataFrame(resumen_act), use_container_width=True, hide_index=True)
