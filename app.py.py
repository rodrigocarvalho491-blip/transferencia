import os
from PIL import Image
from fpdf import FPDF
import streamlit as st
import streamlit.components.v1 as components

# 1. Resolução de caminhos absolutos
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(DIRETORIO_ATUAL, "logo.png")
LOGO2_PATH = os.path.join(DIRETORIO_ATUAL, "logo2.png")

st.set_page_config(page_title="Relatório Fotográfico", page_icon="📷", layout="wide")

CUSTOM_CSS = """
<style>
    h1, h2, h3 { color: #004080 !important; font-family: 'Segoe UI', sans-serif; }
    
    /* Estilo padrão para os botões gerais */
    div.stButton > button:first-child {
        background-color: #004080 !important; color: #ffffff !important;
        border-radius: 8px !important; border: none !important; font-weight: bold !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Inicializa as variáveis de controle no session_state
if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

if "equipamentos" not in st.session_state:
    st.session_state.equipamentos = []

# Função MESTRE para limpar todos os dados e reiniciar o app
def resetar_dados():
    st.session_state.reset_counter += 1
    st.session_state.equipamentos = []

rc = st.session_state.reset_counter

# --- CABEÇALHO DO APP COM LOGO ---
col_logo, col_titulo = st.columns([1, 4])

with col_logo:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=150)
    else:
        st.caption("📷 *Adicione 'logo.png' na pasta do projeto*")

with col_titulo:
    st.title("Relatório Fotográfico & Equipamentos")
    st.markdown("Gerador automatizado de relatórios técnicos.")

st.divider()

# --- BOTÃO FLUTUANTE VIA JAVASCRIPT ---
st.button("🔄 Novo Cliente", on_click=resetar_dados)

JS_FLUTUANTE = """
<script>
function aplicarBotaoFlutuante() {
    const botoes = window.parent.document.querySelectorAll('button');
    botoes.forEach(btn => {
        if (btn.innerText.includes('Novo Cliente')) {
            const container = btn.closest('div[data-testid="element-container"]') || btn.closest('.element-container');
            if(container) {
                container.style.position = 'fixed';
                container.style.bottom = '40px';
                container.style.right = '40px';
                container.style.zIndex = '9999';
                container.style.width = 'auto';
            }
            btn.style.backgroundColor = '#FF4B4B';
            btn.style.color = 'white';
            btn.style.border = '2px solid white';
            btn.style.borderRadius = '30px';
            btn.style.padding = '15px 30px';
            btn.style.fontWeight = 'bold';
            btn.style.fontSize = '16px';
            btn.style.boxShadow = '0 4px 10px rgba(0,0,0,0.3)';
            btn.style.transition = 'all 0.3s ease';
            
            btn.onmouseover = function() {
                this.style.transform = 'scale(1.05)';
                this.style.backgroundColor = '#FF3333';
            }
            btn.onmouseout = function() {
                this.style.transform = 'scale(1)';
                this.style.backgroundColor = '#FF4B4B';
            }
        }
    });
}
aplicarBotaoFlutuante();
setTimeout(aplicarBotaoFlutuante, 500);
setTimeout(aplicarBotaoFlutuante, 1500);
</script>
"""
components.html(JS_FLUTUANTE, height=0, width=0)


# --- SEÇÃO 1: DADOS DO CLIENTE (Organizado Linha por Linha para o Tab ir Lateral) ---
st.subheader("1. Identificação do Cliente")

# Linha 1
s1_l1_c1, s1_l1_c2, s1_l1_c3 = st.columns(3)
with s1_l1_c1:
    cod_cliente = st.text_input("Código do Cliente *", placeholder="Ex: 87.653", key=f"input_cod_{rc}")
with s1_l1_c2:
    nome_cliente = st.text_input("Nome / Razão Social *", placeholder="Ex: SABOR DA TERRA", key=f"input_nome_{rc}")
with s1_l1_c3:
    telefone = st.text_input("Telefone *", placeholder="Ex: 12-992586760", key=f"input_tel_{rc}")

# Linha 2
s1_l2_c1, s1_l2_c2, s1_l2_c3 = st.columns(3)
with s1_l2_c1:
    contato = st.text_input("Contato *", placeholder="Ex: Nilton", key=f"input_contato_{rc}")
with s1_l2_c2:
    departamento = st.text_input("Sobrenome ou Departamento *", placeholder="Ex: Gerente", key=f"input_depto_{rc}")
with s1_l2_c3:
    st.write("")

st.divider()


# --- SEÇÃO 2: INFORMAÇÕES CONTRATUAIS (Organizado Linha por Linha com Tab Lateral) ---
st.subheader("2. Informações Contratuais")

# Linha 1 (4 colunas)
s2_l1_c1, s2_l1_c2, s2_l1_c3, s2_l1_c4 = st.columns(4)
with s2_l1_c1:
    eq_contrato = st.selectbox("Equipamentos de acordo com contrato? *", ["Sim", "Não"], index=None, placeholder="Selecione", key=f"eq_contrato_{rc}")
with s2_l1_c2:
    desc_eq_contrato = st.text_input("Quais equipamentos disponíveis? *", placeholder="Ex: 01 B190 + 01 CC...", key=f"desc_eq_contrato_{rc}")
with s2_l1_c3:
    tem_freq = st.selectbox("Possui programação cadastrada? *", ["Sim", "Não"], index=None, placeholder="Selecione", key=f"tem_freq_{rc}")
with s2_l1_c4:
    desc_freq = ""
    if tem_freq == "Sim":
        desc_freq = st.text_input("Qual a programação? *", placeholder="Ex: QUINZENAL", key=f"freq_cad_sim_{rc}")
    elif tem_freq == "Não":
        desc_freq = st.text_input("Nº OC de Cadastramento *", placeholder="Ex: [OPERACOES & LOGISTICA] SOL PROGRAMAÇÃO", key=f"freq_cad_nao_{rc}")
    else:
        st.write("")

# Linha 2
s2_l2_c1, s2_l2_c2 = st.columns(2)
with s2_l2_c1:
    consumo_previsto = st.text_input("Consumo Previsto (kg) *", placeholder="Ex: 250", key=f"cons_prev_{rc}")
with s2_l2_c2:
    consumo_real = st.text_input("Consumo Real/Médio (kg) *", placeholder="Ex: 137", key=f"cons_real_{rc}")

# Linha 3
s2_l3_c1, s2_l3_c2 = st.columns(2)
with s2_l3_c1:
    possui_art = st.selectbox("Possui ART? *", ["Sim", "Não"], index=None, placeholder="Selecione", key=f"possui_art_{rc}")
with s2_l3_c2:
    num_art = ""
    if possui_art == "Sim":
        num_art = st.text_input("Número da ART *", placeholder="Ex: 2620261267273002...", key=f"num_art_{rc}")
    else:
        st.write("")

# Linha 4
s2_l4_c1, s2_l4_c2 = st.columns(2)
with s2_l4_c1:
    possui_debitos = st.selectbox("Cliente possui débitos? *", ["Sim", "Não"], index=None, placeholder="Selecione", key=f"possui_debitos_{rc}")
with s2_l4_c2:
    desc_debitos = ""
    if possui_debitos == "Sim":
        desc_debitos = st.text_input("Detalhes dos Débitos *", placeholder="Ex: Fatura vencida de R$...", key=f"desc_debitos_{rc}")
    else:
        st.write("")

# Linha 5
s2_l5_c1, s2_l5_c2 = st.columns(2)
with s2_l5_c1:
    central_norma = st.selectbox("Central dentro de norma? *", ["Sim", "Não"], index=None, placeholder="Selecione", key=f"central_norma_{rc}")
with s2_l5_c2:
    desc_central_norma = ""
    if central_norma == "Não":
        desc_central_norma = st.text_input("Motivo da Central fora de norma *", placeholder="Ex: Falta de extintor...", key=f"desc_central_norma_{rc}")
    else:
        st.write("")

st.divider()


# --- SEÇÃO 3: CADASTRO DE EQUIPAMENTOS ---
st.subheader("3. Cadastro de Equipamentos")

col_qtd, col_eq, col_vaz, col_btn = st.columns([1, 2, 2, 1])

with col_qtd:
    qtd_input = st.number_input("Quantidade", min_value=1, value=1, step=1, key=f"eq_qtd_{rc}")
with col_eq:
    nome_eq_input = st.text_input("Equipamento", placeholder="Ex: Forno Industrial", key=f"eq_nome_{rc}")
with col_vaz:
    vazao_input = st.text_input("Vazão Unitária (kg/h)", placeholder="Ex: 1 ou 1,6", key=f"eq_vazao_{rc}")

with col_btn:
    st.write(" ")
    st.write(" ")
    if st.button("➕ Adicionar", key=f"btn_add_eq_{rc}"):
        if nome_eq_input.strip() and vazao_input.strip():
            try:
                vazao_clean_str = vazao_input.replace(",", ".").lower().replace("kg/h", "").strip()
                vazao_unit = float(vazao_clean_str)
                qtd = int(qtd_input)
                
                vazao_total_item = vazao_unit * qtd
                vazao_formatada = f"{vazao_total_item:.2f}".replace(".", ",").rstrip("0").rstrip(",")

                item_dict = {
                    "qtd": qtd,
                    "nome": nome_eq_input.strip().upper(),
                    "vazao_unit": vazao_unit,
                    "vazao_total_item": vazao_total_item,
                    "texto": f"{qtd:02d} - {nome_eq_input.strip().upper()} - {vazao_formatada} kg/h"
                }
                st.session_state.equipamentos.append(item_dict)
                st.success("Adicionado!")
            except ValueError:
                st.error("Informe um valor numérico válido para a vazão.")
        else:
            st.warning("Preencha o equipamento e a vazão.")

total_vazao = 0.0
if st.session_state.equipamentos:
    st.write("**Lista de Equipamentos Cadastrados:**")
    
    for idx, item in enumerate(st.session_state.equipamentos):
        total_vazao += item["vazao_total_item"]
        
        c_txt, c_del = st.columns([5, 1])
        c_txt.text(item["texto"])
        if c_del.button("❌", key=f"del_{idx}_{rc}"):
            st.session_state.equipamentos.pop(idx)
            st.rerun()

    vazao_total_str = f"{total_vazao:.2f}".replace(".", ",").rstrip("0").rstrip(",")
    st.markdown(f"**VAZÃO TOTAL: {vazao_total_str} kg/h**")

st.divider()


# --- SEÇÃO 4: NOVOS NEGÓCIOS / SATISFAÇÃO (Organizado Linha por Linha) ---
st.subheader("4. Novos Negócios / Satisfação")

# Linha 1
s4_l1_c1, s4_l1_c2 = st.columns(2)
with s4_l1_c1:
    indica_negocios = st.selectbox("Indicou novos negócios? *", ["Sim", "Não"], index=None, placeholder="Selecione", key=f"indica_negocios_{rc}")
with s4_l1_c2:
    cliente_satisfeito = st.selectbox("Cliente está satisfeito com a Consigaz? *", ["Sim", "Não"], index=None, placeholder="Selecione", key=f"cliente_satisfeito_{rc}")

# Linha 2
s4_l2_c1, s4_l2_c2 = st.columns(2)
with s4_l2_c1:
    desc_negocios = st.text_input("Detalhes da indicação", placeholder="Ex: Vizinho quer instalar gás", key=f"desc_negocios_{rc}")
with s4_l2_c2:
    desc_satisfacao = st.text_input("Motivo ou observação da satisfação", placeholder="Ex: Bom atendimento", key=f"desc_satisfacao_{rc}")

st.divider()


# --- SEÇÃO 5: OBSERVAÇÕES GERAIS ---
st.subheader("5. Observações Gerais")
observacoes = st.text_area("Digite as observações", placeholder="Ex: Cliente está satisfeito com os serviços prestados...", key=f"observacoes_{rc}")

st.divider()


# --- SEÇÃO 6: RELATÓRIO FOTOGRÁFICO ---
def carregar_fotos(label, max_arquivos=None):
    fotos = st.file_uploader(label, type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"uploader_{label}_{rc}")
    if max_arquivos and fotos and len(fotos) > max_arquivos:
        st.error(f"⚠️ Limite excedido para {label}. Serão considerados apenas os primeiros {max_arquivos} arquivos.")
        return fotos[:max_arquivos]
    return fotos

st.subheader("6. Relatório Fotográfico")
col_f1, col_f2 = st.columns(2)
with col_f1:
    fotos_fachada = carregar_fotos("FACHADA", max_arquivos=2)
    fotos_central = carregar_fotos("CENTRAL", max_arquivos=5)
    fotos_cilindros = carregar_fotos("CILINDROS", max_arquivos=5)
with col_f2:
    fotos_abrigo = carregar_fotos("ABRIGO", max_arquivos=10)
    fotos_equipamentos = carregar_fotos("EQUIPAMENTOS", max_arquivos=None)

st.divider()


# --- SEÇÃO 7: AÇÕES E GERAÇÃO DE RELATÓRIO ---
def validar_campos_pdf():
    campos_faltantes = []
    # Para o PDF, a exigência é mínima (apenas Código e Nome)
    if not cod_cliente.strip(): campos_faltantes.append("Código do Cliente")
    if not nome_cliente.strip(): campos_faltantes.append("Nome / Razão Social")
    return campos_faltantes

def validar_campos_texto():
    campos_faltantes = []
    # Para o Texto do Sistema, as exigências de formulário continuam
    if not cod_cliente.strip(): campos_faltantes.append("Código do Cliente")
    if not contato.strip(): campos_faltantes.append("Contato")
    if not nome_cliente.strip(): campos_faltantes.append("Nome / Razão Social")
    if not departamento.strip(): campos_faltantes.append("Sobrenome ou Departamento")
    if not telefone.strip(): campos_faltantes.append("Telefone")
    
    if not eq_contrato: campos_faltantes.append("Equipamentos de acordo com contrato?")
    if not desc_eq_contrato.strip(): campos_faltantes.append("Quais equipamentos disponíveis (Contrato)")
    
    if not tem_freq: campos_faltantes.append("Possui programação cadastrada?")
    if tem_freq == "Sim" and not desc_freq.strip(): campos_faltantes.append("Qual a programação? (Pois marcou 'Sim')")
    if tem_freq == "Não" and not desc_freq.strip(): campos_faltantes.append("Nº OC de Cadastramento (Pois marcou 'Não')")
    
    if not consumo_previsto.strip(): campos_faltantes.append("Consumo Previsto")
    if not consumo_real.strip(): campos_faltantes.append("Consumo Real/Médio")
    if not possui_art: campos_faltantes.append("Possui ART?")
    if possui_art == "Sim" and not num_art.strip(): campos_faltantes.append("Número da ART (Pois marcou que possui)")
    if not possui_debitos: campos_faltantes.append("Cliente possui débitos?")
    if possui_debitos == "Sim" and not desc_debitos.strip(): campos_faltantes.append("Detalhes dos Débitos (Pois marcou que possui)")
    if not central_norma: campos_faltantes.append("Central dentro de norma?")
    if central_norma == "Não" and not desc_central_norma.strip(): campos_faltantes.append("Motivo da Central fora de norma (Pois marcou que não está)")
    
    if not indica_negocios: campos_faltantes.append("Indicou novos negócios?")
    if not cliente_satisfeito: campos_faltantes.append("Cliente está satisfeito com a Consigaz?")
    
    return campos_faltantes


class RelatorioPDF(FPDF):
    def __init__(self, cod_cliente="", nome_cliente=""):
        super().__init__()
        self.cod_cliente = cod_cliente.replace(".", "").strip().upper() if cod_cliente else ""
        self.nome_cliente = nome_cliente.strip().upper() if nome_cliente else ""

    def header(self):
        if os.path.exists(LOGO2_PATH):
            self.image(LOGO2_PATH, x=10, y=8, w=45)

        if self.page_no() == 1:
            self.set_y(10)
            self.set_font("Arial", "B", 15)
            self.cell(0, 8, "RELATÓRIO DE FOTOS", align="C", ln=1)
            
            info_cabecalho = f"{self.cod_cliente} | {self.nome_cliente}".strip(" |")
            if info_cabecalho:
                self.set_font("Arial", "B", 11)
                self.cell(0, 6, info_cabecalho, align="C", ln=1)
            
            self.set_y(35)
        else:
            self.set_y(35)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def gerar_pdf(equipamentos, dic_fotos, cod_cliente, nome_cliente):
    pdf = RelatorioPDF(cod_cliente, nome_cliente)
    pdf.set_margins(10, 35, 10)
    pdf.set_auto_page_break(auto=True, margin=20)

    # Renderiza as Fotos com Centralização Garantida
    for categoria, arquivos in dic_fotos.items():
        if arquivos:
            pdf.add_page()
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 6, categoria.upper(), ln=1, align="L")
            pdf.ln(2)
            
            for idx, arq in enumerate(arquivos):
                try:
                    img = Image.open(arq)
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    
                    temp_path = f"temp_{categoria}_{idx}.jpg"
                    img.save(temp_path)
                    
                    img_w_px, img_h_px = img.size
                    proporcao = img_h_px / img_w_px
                    
                    w_alvo = 130
                    h_alvo = w_alvo * proporcao
                    
                    if h_alvo > 110:
                        h_alvo = 110
                        w_alvo = h_alvo / proporcao
                    
                    pos_x_centro = (210 - w_alvo) / 2
                    
                    if pdf.get_y() + h_alvo > 270:
                        pdf.add_page()
                    
                    pdf.image(temp_path, x=pos_x_centro, y=pdf.get_y(), w=w_alvo, h=h_alvo)
                    pdf.set_y(pdf.get_y() + h_alvo + 5)
                    
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                except Exception as e:
                    pdf.cell(0, 6, f"Erro ao processar imagem: {e}", ln=1, align="L")

    # Renderiza a Tabela de Equipamentos
    if equipamentos:
        pdf.add_page()
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, "LISTA DE EQUIPAMENTOS E VAZÕES", ln=1, align="L")
        pdf.ln(2)
        
        pdf.set_font("Arial", "B", 10)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(20, 7, "QTD", border=1, align="C", fill=True)
        pdf.cell(120, 7, "EQUIPAMENTO", border=1, align="C", fill=True)
        pdf.cell(50, 7, "VAZÃO TOTAL (KG/H)", border=1, align="C", fill=True, ln=1)
        
        pdf.set_font("Arial", "", 10)
        total_vazao_pdf = 0.0
        for item in equipamentos:
            total_vazao_pdf += item["vazao_total_item"]
            vazao_item_str = f"{item['vazao_total_item']:.2f}".replace(".", ",").rstrip("0").rstrip(",")
            if not vazao_item_str or vazao_item_str == ",":
                vazao_item_str = "0"
            
            pdf.cell(20, 6, f"{item['qtd']:02d}", border=1, align="C")
            pdf.cell(120, 6, f"{item['nome']}", border=1, align="L")
            pdf.cell(50, 6, f"{vazao_item_str} kg/h", border=1, align="C", ln=1)
        
        vazao_total_str = f"{total_vazao_pdf:.2f}".replace(".", ",").rstrip("0").rstrip(",")
        if not vazao_total_str or vazao_total_str == ",":
            vazao_total_str = "0"

        pdf.set_font("Arial", "B", 10)
        pdf.cell(140, 7, "VAZÃO TOTAL:", border=1, align="R", fill=True)
        pdf.cell(50, 7, f"{vazao_total_str} kg/h", border=1, align="C", fill=True, ln=1)

    if pdf.page_no() == 0:
        pdf.add_page()

    return pdf.output(dest="S").encode("latin-1")


st.subheader("7. Ações Finais")
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("📄 Gerar Relatório PDF"):
        erros_pdf = validar_campos_pdf()
        
        if erros_pdf:
            st.error(f"⚠️ **Para o PDF, preencha pelo menos os seguintes campos:**\n\n" + "\n".join([f"- {erro}" for erro in erros_pdf]))
        else:
            dicionario_fotos = {
                "FACHADA": fotos_fachada,
                "ABRIGO": fotos_abrigo,
                "CENTRAL": fotos_central,
                "CILINDROS": fotos_cilindros,
                "EQUIPAMENTOS": fotos_equipamentos
            }
            
            pdf_out = gerar_pdf(
                st.session_state.equipamentos,
                dicionario_fotos,
                cod_cliente,
                nome_cliente
            )
            
            cod_formatado = cod_cliente.replace(".", "").strip().upper() if cod_cliente else ""
            nome_arquivo_pdf = f"fotos_{cod_formatado}.pdf" if cod_formatado else "fotos.pdf"

            st.success("✅ Relatório PDF gerado com sucesso!")
            st.download_button(
                label="📥 Baixar Relatório (PDF)",
                data=pdf_out,
                file_name=nome_arquivo_pdf,
                mime="application/pdf"
            )

with col_btn2:
    if st.button("📝 Gerar Texto para Sistema"):
        erros_texto = validar_campos_texto()
        
        if erros_texto:
            st.error(f"⚠️ **Preencha os campos obrigatórios antes de gerar:**\n\n" + "\n".join([f"- {erro}" for erro in erros_texto]))
        else:
            if possui_art == "Sim":
                linha_art = f"(x) Sim ( ) Não {num_art}".strip()
            else:
                linha_art = "( ) Sim (x) Não"
                
            texto_eq_contrato = f"{eq_contrato}. {desc_eq_contrato.strip()}".strip() if desc_eq_contrato.strip() else eq_contrato
            
            texto_freq = tem_freq
            if tem_freq in ["Sim", "Não"] and desc_freq.strip():
                texto_freq += f" - {desc_freq.strip()}"
                
            texto_debitos = possui_debitos
            if possui_debitos == "Sim" and desc_debitos.strip():
                texto_debitos += f" - {desc_debitos.strip()}"

            texto_central_norma = central_norma
            if central_norma == "Não" and desc_central_norma.strip():
                texto_central_norma += f" - {desc_central_norma.strip()}"

            texto_negocios = indica_negocios
            if indica_negocios == "Sim" and desc_negocios.strip():
                texto_negocios += f" - {desc_negocios.strip()}"
                
            texto_satisfacao = cliente_satisfeito
            if desc_satisfacao.strip():
                texto_satisfacao += f", {desc_satisfacao.strip()}"
                
            lista_eq_formatada = ""
            if st.session_state.equipamentos:
                for eq in st.session_state.equipamentos:
                    lista_eq_formatada += f"{eq['texto']}\n"
            else:
                lista_eq_formatada = "Nenhum equipamento cadastrado.\n"
                
            vazao_total_str = f"{total_vazao:.2f}".replace(".", ",").rstrip("0").rstrip(",") if total_vazao > 0 else "0"

            texto_final = f"""Contato: {contato}
Sobrenome ou departamento: {departamento}
Telefone: {telefone}

Equipamentos de acordo com o contrato vigente? {texto_eq_contrato}
Possui programação cadastrada? {texto_freq}
Consumo mensal atual de acordo com o contrato vigente? Consumo previsto: {consumo_previsto} kg | Consumo médio: {consumo_real} kg
Laudo ART emitido? {linha_art}
Central atende as normas? {texto_central_norma}

Quais equipamentos disponíveis no cliente?

{lista_eq_formatada}VAZÃO TOTAL: {vazao_total_str} kg/h

Indicação de novos negócios do cliente: {texto_negocios}
Cliente possui débitos? {texto_debitos}
Cliente está satisfeito com o atendimento da Consigaz? {texto_satisfacao}

Obs.: {observacoes}
"""
            st.success("✅ Texto gerado com sucesso! Utilize o botão de copiar no canto superior direito do bloco abaixo:")
            st.code(texto_final, language="text")
