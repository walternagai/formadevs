"""
Módulo de visualização do histórico.
Contém componentes para exibir e gerenciar grupos salvos.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.persistence import load_history, save_history, clear_history
from ui.components import card_estatistica, alerta_info, alerta_sucesso, alerta_aviso


def exibir_historico():
    """Exibe a página de histórico completa."""
    st.title("📚 Histórico de Grupos")
    
    # Carregar histórico
    historico = st.session_state.get('historico_grupos', [])
    
    # Se vazio, tentar carregar do arquivo
    if not historico:
        historico_arquivo = load_history()
        if historico_arquivo:
            st.session_state['historico_grupos'] = historico_arquivo
            historico = historico_arquivo
    
    if not historico:
        alerta_info("Nenhum histórico encontrado. Use a página 'Formar Grupos' para criar novos grupos.")
        return
    
    # Estatísticas do histórico
    st.markdown("**📊 Resumo do Histórico**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        card_estatistica("Total Formações", len(historico), "📝", "#2196F3")
    with col2:
        total_grupos = sum(len(item.get('grupos', [])) for item in historico)
        card_estatistica("Total Grupos", total_grupos, "📦", "#4CAF50")
    with col3:
        total_estudantes = sum(len(item.get('estudantes', [])) for item in historico)
        card_estatistica("Total Estudantes", total_estudantes, "👥", "#9C27B0")
    
    st.divider()
    
    # Ações em massa
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🗑️ Limpar Histórico", type="secondary"):
            if st.checkbox("⚠️ Confirmar exclusão de todo o histórico?", key="confirmar_limpar"):
                clear_history()
                st.session_state['historico_grupos'] = []
                alerta_sucesso("Histórico limpo com sucesso!")
                st.rerun()
    
    with col2:
        # Exportar histórico
        from utils.persistence import export_all_data
        if st.button("📤 Exportar Dados", type="secondary"):
            caminho = export_all_data()
            if caminho:
                with open(caminho, 'rb') as f:
                    st.download_button(
                        "⬇️ Download JSON",
                        data=f.read(),
                        file_name="formadevs_backup.json",
                        mime="application/json",
                        use_container_width=True
                    )
    
    with col3:
        # Importar histórico
        arquivo_import = st.file_uploader("📥 Importar JSON", type="json", label_visibility="collapsed")
        if arquivo_import:
            from utils.persistence import import_all_data
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
                tmp.write(arquivo_import.read())
                tmp_path = tmp.name
            
            sucesso, msg = import_all_data(tmp_path)
            os.unlink(tmp_path)
            
            if sucesso:
                alerta_sucesso(msg)
                st.rerun()
            else:
                alerta_aviso(msg)
    
    st.divider()
    
    # Lista de itens do histórico
    st.markdown("**📋 Formações Salvas**")
    
    for i, item in enumerate(historico):
        with st.expander(
            f"🕐 {item['data']} - {item['descricao']} ({len(item['grupos'])} grupos, {len(item['estudantes'])} estudantes)",
            expanded=False
        ):
            exibir_item_historico(item, i)


def exibir_item_historico(item, indice):
    """Exibe os detalhes de um item do histórico."""
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown("**📋 Informações**")
        st.write(f"**Data:** {item['data']}")
        st.write(f"**Método:** {item['metodo']}")
        st.write(f"**Tamanho alvo:** {item['tamanho_grupo']} estudantes/grupo")
    
    with col2:
        st.markdown("**📊 Estatísticas**")
        grupos = item['grupos']
        tamanhos = [len(g) for g in grupos]
        
        st.write(f"**Total estudantes:** {sum(tamanhos)}")
        st.write(f"**Menor grupo:** {min(tamanhos)}")
        st.write(f"**Maior grupo:** {max(tamanhos)}")
    
    with col3:
        st.markdown("**⚙️ Ações**")
        
        if st.button("📥 Recarregar", key=f"recarregar_{indice}", use_container_width=True):
            st.session_state['estudantes_carregados'] = item['estudantes']
            st.session_state['config_rapida'] = {
                'tamanho_grupo': item['tamanho_grupo'],
                'metodo': item['metodo']
            }
            alerta_sucesso("Dados carregados! Vá para 'Formar Grupos' para usá-los.")
        
        if st.button("🗑️ Excluir", key=f"excluir_{indice}", use_container_width=True):
            # Remover do histórico
            historico = st.session_state['historico_grupos']
            historico.pop(indice)
            st.session_state['historico_grupos'] = historico
            
            # Salvar no arquivo
            save_history(historico)
            
            alerta_sucesso("Item removido do histórico!")
            st.rerun()
        
        # Exportar este item
        csv_data = preparar_csv_item(item)
        st.download_button(
            "📄 CSV",
            data=csv_data,
            file_name=f"historico_{indice+1}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key=f"csv_{indice}",
            use_container_width=True
        )
    
    # Tabela com os grupos
    st.markdown("**👥 Grupos**")
    
    df_grupos = pd.DataFrame([
        {
            'Grupo': g_i + 1,
            'Estudante': e.get('completo', f"{e.get('matricula', '')}, {e.get('nome', '')}")
        }
        for g_i, grupo in enumerate(item['grupos'])
        for e in grupo
    ])
    
    st.dataframe(df_grupos, use_container_width=True)


def preparar_csv_item(item):
    """Prepara dados CSV de um item do histórico."""
    dados = []
    for g_i, grupo in enumerate(item['grupos'], 1):
        for estudante in grupo:
            dados.append({
                'Grupo': g_i,
                'Matricula': estudante.get('matricula', ''),
                'Nome': estudante.get('nome', '')
            })
    
    df = pd.DataFrame(dados)
    return df.to_csv(index=False).encode('utf-8')
