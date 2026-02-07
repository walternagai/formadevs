"""
FormaDevs - Formador de Grupos de Estudantes v2.0
Aplicação Streamlit para formação de grupos com recursos avançados.

Autor: Equipe FormaDevs
Versão: 2.0
"""

try:
    import streamlit as st
except ImportError:
    pass
from datetime import datetime

# Importar módulos de UI
from ui.input_forms import entrada_manual_com_preview, importar_csv_com_mapeamento, carregar_grupos_salvos
from ui.group_display import exibir_grupos
from ui.history_view import exibir_historico
from ui.settings_view import exibir_configuracoes
from ui.components import alerta_info, alerta_sucesso, alerta_aviso, alerta_erro
from ui.animations import animacao_contador

# Importar módulos de lógica
from logic.group_formation import formar_grupos
from logic.validation import processar_entrada_com_validacao

# Importar utilitários
from utils.persistence import load_config, load_history, save_history


def inicializar_sessao():
    """Inicializa as variáveis de sessão necessárias."""
    # Carregar configurações salvas
    config = load_config()
    
    defaults = {
        'estudantes_importados': [],
        'estudantes_carregados': [],
        'historico_grupos': [],
        'tamanho_padrao': config.get('tamanho_padrao', 3),
        'metodo_padrao': config.get('metodo_padrao', 'Aleatório'),
        'redistribuir_padrao': config.get('redistribuir_padrao', True),
        'permitir_maior_padrao': config.get('permitir_maior_padrao', True),
        'animacao_padrao': config.get('animacao_padrao', True),
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Carregar histórico do arquivo
    if not st.session_state['historico_grupos']:
        historico = load_history()
        if historico:
            st.session_state['historico_grupos'] = historico


def main():
    """Função principal da aplicação."""
    # Configuração da página
    st.set_page_config(
        page_title="FormaDevs v2.0",
        page_icon="👥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inicializar sessão
    inicializar_sessao()
    
    # Sidebar
    with st.sidebar:
        st.title("🎓 FormaDevs")
        st.markdown("**v2.0** - Formador de Grupos")
        st.divider()
        
        # Navegação
        pagina = st.radio(
            "Navegação",
            ["🏠 Formar Grupos", "📚 Histórico", "⚙️ Configurações"],
            index=0
        )
        
        st.divider()
        
        # Resumo rápido
        if st.session_state.get('historico_grupos'):
            total = len(st.session_state['historico_grupos'])
            st.metric("Formações Salvas", total)
    
    # Roteamento de páginas
    if "Formar Grupos" in pagina:
        exibir_pagina_formar_grupos()
    elif "Histórico" in pagina:
        exibir_historico()
    elif "Configurações" in pagina:
        exibir_configuracoes()


def exibir_pagina_formar_grupos():
    """Exibe a página principal para formação de grupos."""
    st.title("👥 Formador de Grupos de Estudantes")
    
    # Tabs para diferentes modos de entrada
    tab1, tab2, tab3 = st.tabs(["✏️ Entrada Manual", "📁 Importar CSV", "💾 Carregar Salvo"])
    
    estudantes = []
    
    with tab1:
        estudantes = entrada_manual_com_preview()
    
    with tab2:
        estudantes_csv = importar_csv_com_mapeamento()
        if estudantes_csv:
            estudantes = estudantes_csv
    
    with tab3:
        estudantes_salvos = carregar_grupos_salvos()
        if estudantes_salvos:
            estudantes = estudantes_salvos
    
    # Seção de configuração e formação
    st.divider()
    
    if estudantes:
        st.markdown(f"**📊 Total de estudantes carregados:** {len(estudantes)}")
        
        # Configurações
        st.markdown("**⚙️ Configurações de Formação**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Usar configurações da sessão ou config rápida
            tamanho_default = st.session_state.get('config_rapida', {}).get('tamanho_grupo', 
                            st.session_state.get('tamanho_padrao', 3))
            
            tamanho_grupo = st.slider(
                "Tamanho de cada grupo:",
                min_value=2,
                max_value=10,
                value=tamanho_default,
                help="Número de estudantes por grupo"
            )
        
        with col2:
            metodo_default = st.session_state.get('config_rapida', {}).get('metodo',
                           st.session_state.get('metodo_padrao', 'Aleatório'))
            
            metodo = st.radio(
                "Método de formação:",
                ["Aleatório", "Sequencial", "Balanceado"],
                index=["Aleatório", "Sequencial", "Balanceado"].index(metodo_default),
                help="Como os grupos serão formados"
            )
        
        # Opções avançadas
        with st.expander("🔧 Opções Avançadas"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                redistribuir = st.checkbox(
                    "Redistribuir solitários",
                    value=st.session_state.get('redistribuir_padrao', True)
                )
            
            with col2:
                permitir_maior = st.checkbox(
                    "Permitir grupos maiores",
                    value=st.session_state.get('permitir_maior_padrao', True)
                )
            
            with col3:
                usar_animacao = st.checkbox(
                    "Mostrar animação",
                    value=st.session_state.get('animacao_padrao', True)
                )
            
            # Semente aleatória
            semente = st.number_input(
                "Semente aleatória (0 = aleatório)",
                min_value=0,
                value=0,
                help="Use um número > 0 para resultados reproduzíveis"
            )
        
        # Descrição
        descricao = st.text_input(
            "📝 Descrição (opcional):",
            placeholder="Ex: Projeto Final - Turma A",
            help="Identificação para este conjunto de grupos"
        )
        
        # Botão formar grupos
        if st.button("🎯 FORMAR GRUPOS", type="primary", use_container_width=True):
            if len(estudantes) < tamanho_grupo:
                alerta_erro(f"É necessário pelo menos {tamanho_grupo} estudantes para formar grupos!")
            else:
                # Formar grupos
                semente_val = semente if semente > 0 else None
                
                grupos = formar_grupos(
                    estudantes,
                    tamanho_grupo,
                    metodo,
                    redistribuir,
                    permitir_maior,
                    semente_val
                )
                
                # Salvar no histórico
                data_formatada = datetime.now().strftime("%d/%m/%Y %H:%M")
                descricao_final = descricao if descricao else f"Grupos de {tamanho_grupo}"
                
                novo_item = {
                    "data": data_formatada,
                    "descricao": descricao_final,
                    "grupos": grupos,
                    "estudantes": estudantes,
                    "tamanho_grupo": tamanho_grupo,
                    "metodo": metodo
                }
                
                if 'historico_grupos' not in st.session_state:
                    st.session_state['historico_grupos'] = []
                
                st.session_state['historico_grupos'].insert(0, novo_item)  # Adicionar no início
                
                # Salvar no arquivo
                save_history(st.session_state['historico_grupos'])
                
                # Limpar config rápida se existir
                if 'config_rapida' in st.session_state:
                    del st.session_state['config_rapida']
                
                # Exibir grupos
                exibir_grupos(grupos, tamanho_grupo, estudantes, usar_animacao)
    else:
        # Estado vazio
        st.info("👆 Selecione uma aba acima para carregar estudantes e formar grupos!")
        
        # Dicas rápidas
        with st.expander("💡 Dicas Rápidas"):
            st.markdown("""
            **Como usar:**
            1. **Entrada Manual**: Cole a lista de estudantes no formato 'Matrícula, Nome'
            2. **Importar CSV**: Carregue um arquivo CSV com colunas de matrícula e nome
            3. **Carregar Salvo**: Use grupos anteriormente salvos no histórico
            
            **Recursos Novos v2.0:**
            - 🎬 Animação de sorteio com cards
            - 📱 QR Codes para cada grupo
            - 🔍 Validação de duplicatas
            - 💾 Persistência automática
            - 📊 Estatísticas visuais
            """)


if __name__ == "__main__":
    main()
