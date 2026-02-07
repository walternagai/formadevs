"""
Módulo de configurações.
Contém componentes para página de configurações e gerenciamento de dados.
"""

import streamlit as st
from datetime import datetime
from utils.persistence import save_config, load_config, reset_all
from ui.components import alerta_sucesso, alerta_aviso, alerta_info


def exibir_configuracoes():
    """Exibe a página de configurações completa."""
    st.title("⚙️ Configurações")
    
    # Carregar configurações atuais
    config = load_config()
    
    st.markdown("**🎨 Preferências de Formação**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Tamanho padrão
        tamanho_padrao = st.number_input(
            "Tamanho padrão dos grupos",
            min_value=2,
            max_value=10,
            value=config.get('tamanho_padrao', 3),
            help="Tamanho padrão quando nenhum é especificado"
        )
        
        # Método padrão
        metodo_padrao = st.selectbox(
            "Método padrão",
            ["Aleatório", "Sequencial", "Balanceado"],
            index=["Aleatório", "Sequencial", "Balanceado"].index(
                config.get('metodo_padrao', "Aleatório")
            ),
            help="Método padrão de formação de grupos"
        )
    
    with col2:
        # Opções avançadas padrão
        redistribuir_padrao = st.checkbox(
            "Redistribuir estudantes sozinhos",
            value=config.get('redistribuir_padrao', True),
            help="Evitar grupos com apenas 1 estudante"
        )
        
        permitir_maior_padrao = st.checkbox(
            "Permitir grupos maiores",
            value=config.get('permitir_maior_padrao', True),
            help="Permitir grupos maiores que o tamanho definido"
        )
        
        animacao_padrao = st.checkbox(
            "Mostrar animação por padrão",
            value=config.get('animacao_padrao', True),
            help="Mostrar animação de sorteio ao formar grupos"
        )
    
    st.divider()
    
    # Tema
    st.markdown("**🎨 Aparência**")
    
    tema = st.selectbox(
        "Tema da aplicação",
        ["Padrão", "Claro", "Escuro", "Azul", "Verde"],
        index=["Padrão", "Claro", "Escuro", "Azul", "Verde"].index(
            config.get('tema', "Padrão")
        )
    )
    
    st.divider()
    
    # Botão salvar
    if st.button("💾 Salvar Configurações", type="primary"):
        nova_config = {
            'tamanho_padrao': tamanho_padrao,
            'metodo_padrao': metodo_padrao,
            'redistribuir_padrao': redistribuir_padrao,
            'permitir_maior_padrao': permitir_maior_padrao,
            'animacao_padrao': animacao_padrao,
            'tema': tema,
            'data_atualizacao': datetime.now().isoformat()
        }
        
        if save_config(nova_config):
            st.session_state.update(nova_config)
            alerta_sucesso("Configurações salvas com sucesso!")
        else:
            alerta_aviso("Erro ao salvar configurações.")
    
    st.divider()
    
    # Gerenciamento de dados
    st.markdown("**🗄️ Gerenciamento de Dados**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧹 Limpar Histórico", type="secondary"):
            if st.checkbox("⚠️ Confirmar limpeza do histórico?", key="confirmar_hist"):
                from utils.persistence import clear_history
                if clear_history():
                    if 'historico_grupos' in st.session_state:
                        del st.session_state['historico_grupos']
                    alerta_sucesso("Histórico limpo!")
                    st.rerun()
    
    with col2:
        if st.button("🔄 Resetar Tudo", type="secondary"):
            if st.checkbox("⚠️ Confirmar reset completo? Isso apagará tudo!", key="confirmar_reset"):
                if reset_all():
                    # Limpar toda session_state
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    alerta_sucesso("Todas as configurações foram resetadas!")
                    st.rerun()
    
    st.divider()
    
    # Sobre
    st.markdown("**ℹ️ Sobre o FormaDevs**")
    
    st.markdown("""
    **FormaDevs** é uma aplicação para formação de grupos de estudantes.
    
    **Versão:** 2.0  
    **Desenvolvido com:** Python + Streamlit
    
    **Funcionalidades:**
    - Formação de grupos com 3 métodos (Aleatório, Sequencial, Balanceado)
    - Importação de dados via CSV
    - QR Codes para cada grupo
    - Animações de sorteio
    - Persistência de dados
    - Exportação em múltiplos formatos
    """)
    
    # Informações de debug (opcional)
    with st.expander("🔧 Informações Técnicas"):
        st.write(f"**Diretório de dados:** `./data/`")
        st.write(f"**Arquivo de configuração:** `./data/config.json`")
        st.write(f"**Arquivo de histórico:** `./data/history.json`")
        st.write(f"**Session State keys:** {list(st.session_state.keys())}")
