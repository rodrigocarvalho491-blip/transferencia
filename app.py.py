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


# --- SEÇÃO 1: DADOS DO CLIENTE ---
st.subheader("1. Identificação do Cliente")
col_c1, col_c2, col_c3 = st.columns(3)

with col_c1:
    cod_cliente = st.text_input("Código do Cliente", placeholder="Ex: 87.653", key=f"input_cod_{rc}")
    contato = st.text_input("Contato", placeholder="Ex: Nilton", key=f"input_contato_{rc}")
with col_c2:
    nome_cliente = st.text_input("Nome / Razão Social", placeholder="Ex: SABOR DA TERRA", key=f"input_nome_{rc}")
    departamento = st.text_input("Sobrenome ou Departamento", placeholder="Ex: Gerente", key=f"input_depto_{rc}")
with col_c3:
    telefone = st.text_input("Telefone", placeholder="Ex: 12-992586760", key=f"input_tel_{rc}")

st.divider()


# --- SEÇÃO 2: INFORMAÇÕES CONTRATUAIS ---
st.subheader("2. Informações Contratuais")
col_ic1, col_ic2 = st.columns(2)

with col_ic1:
    eq_contrato = st.selectbox("Equipamentos de acordo com contrato?", ["Sim", "Não"], key=f"eq_contrato_{rc}")
    desc_eq_contrato = st.text_input("Quais equipamentos disponíveis?", placeholder="Ex: 01 B190 + 01 CC...", key=f"desc_eq_contrato_{rc}")
    consumo_previsto = st.text_input("Consumo Previsto (kg)", placeholder="Ex: 250", key=f"cons_prev_{rc}")
    possui_art = st.selectbox("Possui ART?", ["Sim", "Não"], key=f"possui_art_{rc}")
    central_norma = st.selectbox("Central dentro de norma?", ["Sim", "Não"], key=f"central_norma_{rc}")

with col_ic2:
    freq_cadastrada = st.text_input("Frequência Cadastrada", placeholder="Ex: QUINZENAL", key=f"freq_cad_{rc}")
    consumo_real = st.text_input("Consumo Real/Médio (kg)", placeholder="Ex: 137", key=f"cons_real_{rc}")
    st.write(" ")
    st.write(" ")
    num_art = st.text_input("Número da ART (se possuir)", placeholder="Ex: 2620261267273002...", key=f"num_art_{rc}")
    possui_debitos = st.selectbox("Cliente possui débitos?", ["Sim", "Não"], key=f"possui_debitos_{rc}")

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


# --- SEÇÃO 4: NOVOS NEGÓCIOS / SATISFAÇÃO ---
st.subheader("4. Novos Negócios / Satisfação")
col_nn1, col_nn2 = st.columns(2)

with col_nn1:
    indica_negocios = st.selectbox("Indicou novos negócios?", ["Sim", "Não"], key=f"indica_negocios_{rc}")
    desc_negocios = st.text_input("Detalhes da indicação", placeholder="Ex: Vizinho quer instalar gás", key=f"desc_negocios_{rc}")

with col_nn2:
    cliente_satisfeito = st.selectbox("Cliente está satisfeito com a Consigaz?", ["Sim", "Não"], key=f"cliente_satisfeito_{rc}")
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

    # Renderiza as Fotos
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
                    
                    # CORREÇÃO APLICADA AQUI: Substituído x="C" por x=40 
                    # 40 é a margem centralizada exata para uma imagem w=130 em folha A4 (210mm)
                    pdf.image(temp_path, x=40, w=130)
                    pdf.ln(3)
                    
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
        # Lógica para exibição do ART
        if possui_art == "Sim":
            linha_art = f"(x) Sim ( ) Não {num_art}".strip()
        else:
            linha_art = "( ) Sim (x) Não"
            
        # Lógica de Equipamentos Contrato
        texto_eq_contrato = f"{eq_contrato}. {desc_eq_contrato.strip()}".strip() if desc_eq_contrato.strip() else eq_contrato
            
        # Lógica para Novos Negócios
        texto_negocios = indica_negocios
        if indica_negocios == "Sim" and desc_negocios.strip():
            texto_negocios += f" - {desc_negocios.strip()}"
            
        # Lógica para Satisfação
        texto_satisfacao = cliente_satisfeito
        if desc_satisfacao.strip():
            texto_satisfacao += f", {desc_satisfacao.strip()}"
            
        # Equipamentos Formatados
        lista_eq_formatada = ""
        if st.session_state.equipamentos:
            for eq in st.session_state.equipamentos:
                lista_eq_formatada += f"{eq['texto']}\n\n"
        else:
            lista_eq_formatada = "Nenhum equipamento cadastrado.\n\n"
            
        # Vazão
        vazao_total_str = f"{total_vazao:.2f}".replace(".", ",").rstrip("0").rstrip(",") if total_vazao > 0 else "0"

        # Montagem do Texto Final
        texto_final = f"""Contato: {contato}
Sobrenome ou departamento: {departamento}
Telefone: {telefone}

Equipamentos de acordo com o contrato vigente? {texto_eq_contrato}
Frequência cadastrada? {freq_cadastrada}
Consumo mensal atual de acordo com o contrato vigente? Consumo previsto: {consumo_previsto} kg | Consumo médio: {consumo_real} kg
Laudo ART emitido? {linha_art}
Central atende as normas? {central_norma}

Quais equipamentos disponíveis no cliente?

{lista_eq_formatada}VAZÃO TOTAL: {vazao_total_str} kg/h

Indicação de novos negócios do cliente: {texto_negocios}
Cliente possui débitos? {possui_debitos}
Cliente está satisfeito com o atendimento da Consigaz? {texto_satisfacao}

Obs.: {observacoes}
"""
        st.success("✅ Texto gerado com sucesso!")
        st.text_area("Copie o texto abaixo para colar no sistema:", value=texto_final, height=450)
