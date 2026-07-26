import streamlit as st
import time
import os
import json

ARQUIVO_DADOS = "ilhas_salvas.json"

# Funções para salvar e carregar os dados no computador
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def salvar_dados(lista):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)

st.set_page_config(
    page_title="Ilha de Foco",
    page_icon="🗺️",
    layout="centered"
)

# Estilização visual com o fundo azul clarinho idêntico ao app original
st.markdown("""
    <style>
    .stApp {
        background-color: #E0F2FE;
    }
    h1, h2, h3, p, label {
        color: #1E293B !important;
    }
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border-radius: 8px !important;
        border: 1px solid #CBD5E1 !important;
    }
    /* Transforma os botões da lista de ilhas em cartões claros */
    div[data-testid="stVerticalBlock"] button {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stVerticalBlock"] button:hover {
        border-color: #94A3B8 !important;
        color: #0F172A !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização de estados usando o arquivo local
if 'lista_ilhas' not in st.session_state:
    st.session_state.lista_ilhas = carregar_dados()

if 'ilha_ativa_idx' not in st.session_state:
    st.session_state.ilha_ativa_idx = None

if 'ativo' not in st.session_state:
    st.session_state.ativo = False

def formatar_tempo(total_segundos):
    hrs = total_segundos // 3600
    mins = (total_segundos % 3600) // 60
    segs = total_segundos % 60
    return f"{hrs:02d}:{mins:02d}:{segs:02d}"

# Mapeamento fiel das fases da ilha
def obter_imagem_fase(minutos_focados):
    base_path = "assets/images"
    
    if minutos_focados >= 1620: arquivo = "ilha_fase_45.png"
    elif minutos_focados >= 1560: arquivo = "ilha_fase_44.png"
    elif minutos_focados >= 1500: arquivo = "ilha_fase_43.png"
    elif minutos_focados >= 1440: arquivo = "ilha_fase_42.png"
    elif minutos_focados >= 1380: arquivo = "ilha_fase_41.png"
    elif minutos_focados >= 1320: arquivo = "ilha_fase_40.png"
    elif minutos_focados >= 1290: arquivo = "ilha_fase_39.png"
    elif minutos_focados >= 1260: arquivo = "ilha_fase_38.png"
    elif minutos_focados >= 1230: arquivo = "ilha_fase_37.png"
    elif minutos_focados >= 1200: arquivo = "ilha_fase_36.png"
    elif minutos_focados >= 1140: arquivo = "ilha_fase_35.png"
    elif minutos_focados >= 1110: arquivo = "ilha_fase_34.png"
    elif minutos_focados >= 1080: arquivo = "ilha_fase_33.png"
    elif minutos_focados >= 1050: arquivo = "ilha_fase_32.png"
    elif minutos_focados >= 1020: arquivo = "ilha_fase_31.png"
    elif minutos_focados >= 990:  arquivo = "ilha_fase_30.png"
    elif minutos_focados >= 960:  arquivo = "ilha_fase_29.png"
    elif minutos_focados >= 930:  arquivo = "ilha_fase_28.png"
    elif minutos_focados >= 900:  arquivo = "ilha_fase_27.png"
    elif minutos_focados >= 840:  arquivo = "ilha_fase_26.png"
    elif minutos_focados >= 810:  arquivo = "ilha_fase_25.png"
    elif minutos_focados >= 780:  arquivo = "ilha_fase_24.png"
    elif minutos_focados >= 750:  arquivo = "ilha_fase_23.png"
    elif minutos_focados >= 720:  arquivo = "ilha_fase_22.png"
    elif minutos_focados >= 660:  arquivo = "ilha_fase_21.png"
    elif minutos_focados >= 600:  arquivo = "ilha_fase_20.png"
    elif minutos_focados >= 570:  arquivo = "ilha_fase_19.png"
    elif minutos_focados >= 510:  arquivo = "ilha_fase_17.png"
    elif minutos_focados >= 480:  arquivo = "ilha_fase_16.png"
    elif minutos_focados >= 420:  arquivo = "ilha_fase_15.png"
    elif minutos_focados >= 360:  arquivo = "ilha_fase_14.png"
    elif minutos_focados >= 330:  arquivo = "ilha_fase_13.png"
    elif minutos_focados >= 300:  arquivo = "ilha_fase_12.png"
    elif minutos_focados >= 270:  arquivo = "ilha_fase_11.png"
    elif minutos_focados >= 240:  arquivo = "ilha_fase_10.png"
    elif minutos_focados >= 210:  arquivo = "ilha_fase_9.png"
    elif minutos_focados >= 180:  arquivo = "ilha_fase_8.png"
    elif minutos_focados >= 150:  arquivo = "ilha_fase_7.png"
    elif minutos_focados >= 120:  arquivo = "ilha_fase_6.png"
    elif minutos_focados >= 90:   arquivo = "ilha_fase_5.png"
    elif minutos_focados >= 60:   arquivo = "ilha_fase_4.png"
    elif minutos_focados >= 30:   arquivo = "ilha_fase_3.png"
    elif minutos_focados >= 10:   arquivo = "ilha_fase_2.png"
    else: arquivo = "bloco_grama_1.png"

    caminho = os.path.join(base_path, arquivo)
    return caminho if os.path.exists(caminho) else None

# --- TELA 1: MENU PRINCIPAL ---
if st.session_state.ilha_ativa_idx is None:
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>Minhas Ilhas de Foco 🗺️</h1>", unsafe_allow_html=True)
    
    with st.container():
        col_input, col_btn = st.columns([3, 1])
        with col_input:
            nome_nova = st.text_input("Criar nova ilha", label_visibility="collapsed", placeholder="Criar nova ilha (Ex: Python, TCC...)")
        with col_btn:
            if st.button("+ Criar", use_container_width=True):
                if nome_nova.strip():
                    nova_ilha = {
                        "id": str(len(st.session_state.lista_ilhas) + 1),
                        "nome": nome_nova.strip(),
                        "segundos": 0
                    }
                    st.session_state.lista_ilhas.append(nova_ilha)
                    salvar_dados(st.session_state.lista_ilhas)
                    st.success("Ilha criada!")
                    st.rerun()
                else:
                    st.warning("Digite um nome.")

    st.markdown("### Suas Ilhas")
    
    if not st.session_state.lista_ilhas:
        st.info("Nenhuma ilha criada ainda.")
    else:
        for idx, ilha in enumerate(st.session_state.lista_ilhas):
            if st.button(f"🏝️ {ilha['nome']} — Foco: {formatar_tempo(ilha['segundos'])} ➔", key=f"entrar_{idx}", use_container_width=True):
                st.session_state.ilha_ativa_idx = idx
                st.session_state.ativo = True  # Inicia o cronômetro automaticamente ao entrar
                st.rerun()

# --- TELA 2: DENTRO DA ILHA (CRONÔMETRO AUTOMÁTICO E IMAGEM) ---
else:
    idx_ativo = st.session_state.ilha_ativa_idx
    ilha = st.session_state.lista_ilhas[idx_ativo]
    
    if st.button("← Menu Principal 🗺️"):
        st.session_state.ativo = False
        st.session_state.ilha_ativa_idx = None
        st.rerun()
        
    st.markdown(f"<h1 style='text-align: center;'>{ilha['nome']}</h1>", unsafe_allow_html=True)
    
    # Exibição do Cronômetro
    placeholder_relogio = st.empty()
    placeholder_relogio.markdown(f"<h1 style='text-align: center; font-size: 48px; letter-spacing: 2px; color: #1E293B;'>{formatar_tempo(ilha['segundos'])}</h1>", unsafe_allow_html=True)
    
    # Exibição da imagem centralizada da fase
    minutos_atv = ilha['segundos'] // 60
    img_path = obter_imagem_fase(minutos_atv)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if img_path:
            st.image(img_path, use_container_width=True)
        else:
            st.warning("⚠️ Coloque a pasta 'assets/images' na raiz para exibir o desenho da ilha.")

    st.markdown("<br>", unsafe_allow_html=True)
    
 # Botões de controle de foco e zerar (apenas 2 colunas)
    c_acao, c_zerar = st.columns(2)
    with c_acao:
        texto_botao = "Pausar" if st.session_state.ativo else "Focar"
        if st.button(texto_botao, use_container_width=True, type="primary", key="btn_focar_pausar"):
            st.session_state.ativo = not st.session_state.ativo
            st.rerun()
    with c_zerar:
        if st.button("Zerar", use_container_width=True, key="btn_zerar"):
            ilha['segundos'] = 0
            st.session_state.ativo = False
            salvar_dados(st.session_state.lista_ilhas)
            st.rerun()
    # Lógica do Cronômetro Automático rodando segundo a segundo
    if st.session_state.ativo:
        time.sleep(1)
        ilha['segundos'] += 1
        salvar_dados(st.session_state.lista_ilhas)
        st.rerun()