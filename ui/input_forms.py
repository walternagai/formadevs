"""
Módulo de formulários de entrada.
Contém componentes para entrada manual e importação de dados.
"""

import streamlit as st
import pandas as pd
from logic.validation import processar_entrada_com_validacao, extrair_preview_dados, validar_csv
from logic.data_processing import processar_csv_para_estudantes
from ui.components import alerta_info, alerta_aviso, alerta_erro, alerta_sucesso


def entrada_manual_com_preview():
    """
    Formulário de entrada manual com preview e validação em tempo real.
    
    Returns:
        list: Lista de estudantes processados ou lista vazia
    """
    st.subheader("📋 Lista de Estudantes")
    
    # Área de texto para entrada
    estudantes_input = st.text_area(
        "Digite os estudantes no formato 'Matrícula, Nome' (um por linha):",
        placeholder="Exemplo:\n123456, João Silva\n789012, Maria Santos\n345678, Pedro Oliveira",
        height=200,
        help="Insira um estudante por linha no formato 'Matrícula, Nome'",
        key="entrada_manual_texto"
    )
    
    estudantes = []
    
    if estudantes_input:
        # Extrair preview
        preview = extrair_preview_dados(estudantes_input, limite=5)
        
        # Mostrar contadores
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Linhas", preview["total_linhas"])
        with col2:
            st.metric("Válidas no Preview", preview["validas_preview"])
        with col3:
            st.metric("Inválidas no Preview", preview["invalidas_preview"])
        
        # Mostrar preview
        with st.expander("👁️ Preview dos dados", expanded=True):
            for item in preview["preview"]:
                status = "✅" if item["valido"] else "❌"
                st.write(f"{status} Linha {item['linha']}: {item['conteudo'][:50]}")
            
            if preview["total_linhas"] > preview["mostradas"]:
                st.info(f"... e mais {preview['total_linhas'] - preview['mostradas']} linhas")
        
        # Processar completamente
        resultado = processar_entrada_com_validacao(estudantes_input)
        estudantes = resultado["estudantes"]
        
        # Mostrar alertas
        if resultado["erros"]:
            alerta_aviso(f"Foram encontradas {len(resultado['erros'])} linhas com formato inválido.")
            with st.expander("Ver detalhes dos erros"):
                for erro in resultado["erros"][:10]:  # Mostrar até 10 erros
                    st.write(f"Linha {erro['linha']}: {erro['conteudo'][:30]}... - {erro['erro']}")
                if len(resultado["erros"]) > 10:
                    st.write(f"... e mais {len(resultado['erros']) - 10} erros")
        
        if resultado["duplicatas"]:
            num_dup = len(resultado["duplicatas"])
            alerta_aviso(f"Detectadas {num_dup} matrículas duplicadas!")
            with st.expander("Ver duplicatas"):
                for matricula, info in resultado["duplicatas"].items():
                    st.write(f"Matrícula **{matricula}** aparece {info['count']} vezes:")
                    for nome in info["nomes"]:
                        st.write(f"  - {nome}")
        
        if estudantes:
            alerta_sucesso(f"{len(estudantes)} estudantes carregados com sucesso!")
    
    return estudantes


def importar_csv_com_mapeamento():
    """
    Formulário de importação de CSV com mapeamento de colunas.
    
    Returns:
        list: Lista de estudantes importados ou lista vazia
    """
    st.subheader("📁 Importar de CSV")
    
    estudantes = []
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "Escolha um arquivo CSV",
        type="csv",
        help="Arquivo CSV com colunas de matrícula e nome"
    )
    
    if uploaded_file is not None:
        try:
            # Ler CSV
            df = pd.read_csv(uploaded_file)
            
            st.write(f"**Arquivo carregado:** {len(df)} registros, {len(df.columns)} colunas")
            
            # Preview dos dados
            with st.expander("👁️ Visualizar dados brutos"):
                st.dataframe(df.head(10), use_container_width=True)
            
            # Seleção de colunas
            st.markdown("**Mapeamento de Colunas**")
            
            col1, col2 = st.columns(2)
            with col1:
                col_matricula = st.selectbox(
                    "Coluna da Matrícula",
                    options=df.columns,
                    help="Selecione a coluna que contém as matrículas"
                )
            with col2:
                col_nome = st.selectbox(
                    "Coluna do Nome",
                    options=df.columns,
                    help="Selecione a coluna que contém os nomes"
                )
            
            # Validar
            valido, erros = validar_csv(df, col_matricula, col_nome)
            
            if not valido:
                alerta_erro("Problemas encontrados no CSV:")
                for erro in erros:
                    st.write(f"- {erro}")
            
            # Preview dos dados mapeados
            st.markdown("**Preview dos dados selecionados:**")
            preview_df = df[[col_matricula, col_nome]].head(10)
            st.dataframe(preview_df, use_container_width=True)
            
            # Botão de confirmação
            if st.button("✅ Confirmar Importação", type="primary"):
                estudantes = processar_csv_para_estudantes(df, col_matricula, col_nome)
                
                if estudantes:
                    st.session_state['estudantes_importados'] = estudantes
                    alerta_sucesso(f"{len(estudantes)} estudantes importados com sucesso!")
                else:
                    alerta_erro("Nenhum estudante válido encontrado no arquivo.")
        
        except Exception as e:
            alerta_erro(f"Erro ao processar arquivo: {str(e)}")
    
    # Verificar se há estudantes já importados na sessão
    elif 'estudantes_importados' in st.session_state:
        estudantes = st.session_state['estudantes_importados']
        alerta_info(f"Usando {len(estudantes)} estudantes importados anteriormente.")
        if st.button("🗑️ Limpar importação anterior"):
            del st.session_state['estudantes_importados']
            st.rerun()
    
    return estudantes


def carregar_grupos_salvos():
    """
    Permite carregar grupos do histórico salvo.
    
    Returns:
        list: Lista de estudantes ou lista vazia
    """
    st.subheader("💾 Carregar do Histórico")
    
    estudantes = []
    
    # Verificar histórico na sessão
    historico = st.session_state.get('historico_grupos', [])
    
    if not historico:
        alerta_info("Nenhum grupo salvo no histórico. Forme grupos primeiro!")
        return estudantes
    
    # Opções de seleção
    opcoes = [
        f"{item['data']} - {item['descricao']} ({len(item['estudantes'])} estudantes)"
        for item in historico
    ]
    
    selecao = st.selectbox("Selecione um grupo salvo:", opcoes)
    
    if selecao:
        indice = opcoes.index(selecao)
        item = historico[indice]
        
        # Mostrar detalhes
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Estudantes", len(item['estudantes']))
        with col2:
            st.metric("Grupos Formados", len(item['grupos']))
        with col3:
            st.metric("Método Usado", item['metodo'])
        
        if st.button("📥 Carregar Estudantes", type="primary"):
            estudantes = item['estudantes']
            st.session_state['estudantes_carregados'] = estudantes
            alerta_sucesso(f"{len(estudantes)} estudantes carregados!")
    
    # Verificar se há estudantes carregados na sessão
    elif 'estudantes_carregados' in st.session_state:
        estudantes = st.session_state['estudantes_carregados']
        alerta_info(f"Usando {len(estudantes)} estudantes carregados.")
    
    return estudantes
