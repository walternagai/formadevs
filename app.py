import streamlit as st
import random
import math
import re
import pandas as pd
import io
import base64
from datetime import datetime
import time

def main():
    """
    Função principal da aplicação FormaDevs.
    Define o layout da página, o menu de navegação lateral e controla qual página será exibida.
    """
    # Configuração inicial da página
    st.set_page_config(
        page_title="FormaDevs",
        page_icon="👥",
        layout="wide"
    )
    
    # Sidebar para navegação e configurações
    with st.sidebar:
        st.title("🎓 FormaDevs")
        pagina = st.radio(
            "Navegação",
            ["Formar Grupos", "Histórico", "Configurações", "Sobre"]
        )
        
        st.divider()
        
        # Tema da aplicação com opções personalizáveis
        tema = st.selectbox(
            "Tema",
            ["Claro", "Escuro", "Azul", "Verde"]
        )
        
        # Aplicar tema selecionado usando CSS personalizado
        if tema == "Claro":
            tema_css = """
            body {background-color: #FFFFFF; color: #000000;}
            .stApp {background-color: #FFFFFF;}
            """
        elif tema == "Escuro":
            tema_css = """
            body {background-color: #262730; color: #FFFFFF;}
            .stApp {background-color: #262730;}
            """
        elif tema == "Azul":
            tema_css = """
            body {background-color: #E8F4F8; color: #0A1929;}
            .stApp {background-color: #E8F4F8;}
            .st-emotion-cache-1gulkj5 {background-color: #D1E9F5;}
            """
        else:  # Verde
            tema_css = """
            body {background-color: #E8F6EF; color: #0A291E;}
            .stApp {background-color: #E8F6EF;}
            .st-emotion-cache-1gulkj5 {background-color: #CCEADA;}
            """
            
        # Injetar CSS personalizado para o tema
        st.markdown(f"<style>{tema_css}</style>", unsafe_allow_html=True)
    
    # Navegação entre páginas baseada na seleção do usuário
    if pagina == "Formar Grupos":
        exibir_pagina_formar_grupos()
    elif pagina == "Histórico":
        exibir_pagina_historico()
    elif pagina == "Configurações":
        exibir_pagina_configuracoes()
    else:  # Sobre
        exibir_pagina_sobre()

def exibir_pagina_formar_grupos():
    """
    Exibe a página principal para formação de grupos.
    Contém abas para diferentes métodos de entrada de dados e opções para configurar e gerar grupos.
    """
    st.title("Formador de Grupos de Estudantes")
    
    # Tabs para diferentes modos de entrada de dados
    tab1, tab2, tab3 = st.tabs(["Entrada Manual", "Importar CSV", "Carregar Salvo"])
    
    with tab1:  # Entrada Manual
        # Área para entrada de estudantes (matrícula e nome)
        st.subheader("Lista de Estudantes")
        estudantes_input = st.text_area(
            "Digite os estudantes no formato 'Matrícula, Nome' (um por linha):",
            placeholder="Exemplo:\n123456, João Silva\n789012, Maria Santos",
            height=200,
            help="Insira um estudante por linha no formato 'Matrícula, Nome'"
        )
        
        # Converter input em lista de estudantes (matrícula e nome)
        if estudantes_input:
            estudantes = processar_entrada_texto(estudantes_input)
        else:
            estudantes = []
    
    with tab2:  # Importar CSV
        st.subheader("Importar Estudantes de CSV")
        
        # Upload de arquivo CSV
        uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
        if uploaded_file is not None:
            try:
                # Leitura do arquivo CSV
                df = pd.read_csv(uploaded_file)
                
                # Interface para mapear colunas do CSV para matrícula e nome
                st.write("Selecione quais colunas correspondem à matrícula e ao nome:")
                col_matricula = st.selectbox("Coluna da Matrícula", options=df.columns)
                col_nome = st.selectbox("Coluna do Nome", options=df.columns)
                
                # Mostrar prévia dos dados importados
                st.write("Prévia dos dados:")
                st.dataframe(df[[col_matricula, col_nome]].head())
                
                # Processar os dados do CSV após confirmação
                if st.button("Confirmar Importação"):
                    estudantes = []
                    for _, row in df.iterrows():
                        matricula = str(row[col_matricula]).strip()
                        nome = str(row[col_nome]).strip()
                        estudantes.append({
                            "matricula": matricula, 
                            "nome": nome, 
                            "completo": f"{matricula}, {nome}"
                        })
                    st.success(f"{len(estudantes)} estudantes importados com sucesso!")
                    
                    # Armazenar na sessão para uso posterior
                    st.session_state.estudantes_importados = estudantes
            except Exception as e:
                # Tratamento de erro na importação
                st.error(f"Erro ao processar o arquivo: {e}")
                estudantes = []
        else:
            # Se já houver estudantes importados na sessão, usar esses
            estudantes = st.session_state.get('estudantes_importados', [])
    
    with tab3:  # Carregar Salvo
        st.subheader("Carregar Grupos Salvos")
        
        # Recuperar histórico da sessão
        historico = st.session_state.get('historico_grupos', [])
        
        if not historico:
            st.info("Nenhum grupo salvo anteriormente. Forme grupos na aba 'Entrada Manual' ou 'Importar CSV' primeiro.")
            estudantes = []
        else:
            # Mostrar opções de grupos salvos anteriormente
            opcoes = [f"{item['data']} - {item['descricao']} ({len(item['estudantes'])} estudantes)" for item in historico]
            selecao = st.selectbox("Selecione um grupo salvo:", opcoes)
            
            if selecao:
                # Carregar dados do histórico selecionado
                indice = opcoes.index(selecao)
                estudantes = historico[indice]['estudantes']
                st.success(f"Carregados {len(estudantes)} estudantes!")
    
    # Exibir número de estudantes carregados
    if "estudantes" in locals() and estudantes:
        st.write(f"Total de estudantes: {len(estudantes)}")
        
        # Configurações para formação de grupos
        col1, col2 = st.columns(2)
        
        with col1:
            # Configuração de tamanho dos grupos
            tamanho_grupo = st.slider(
                "Tamanho de cada grupo:", 
                min_value=2, 
                max_value=8, 
                value=3,
                help="Selecione um número entre 2 e 8 estudantes por grupo"
            )
        
        with col2:
            # Método de formação dos grupos
            metodo = st.radio(
                "Método de formação:",
                ["Aleatório", "Sequencial", "Balanceado"],
                help="Aleatório: grupos totalmente aleatórios\nSequencial: grupos na ordem da lista\nBalanceado: distribuição mais uniforme"
            )
        
        # Opções avançadas para formação de grupos
        with st.expander("Opções avançadas"):
            redistribuir_solitarios = st.checkbox(
                "Redistribuir estudantes sozinhos", 
                value=True,
                help="Evita que estudantes fiquem sozinhos em um grupo"
            )
            
            permitir_grupos_maiores = st.checkbox(
                "Permitir grupos maiores que o limite",
                value=True,
                help="Permite que alguns grupos excedam o tamanho máximo para acomodar todos os estudantes"
            )
            
            semente = st.number_input(
                "Semente aleatória (para reproduzir resultados)",
                min_value=0,
                value=0,
                help="Use o mesmo número para obter os mesmos grupos aleatórios"
            )
        
        # Campo para descrição do grupo
        descricao_grupo = st.text_input(
            "Descrição (opcional):",
            placeholder="Ex: Projeto de Matemática - Turma A",
            help="Uma descrição para identificar este conjunto de grupos"
        )
        
        # Botão para formar grupos
        if st.button("Formar Grupos", type="primary"):
            if len(estudantes) < tamanho_grupo:
                # Validação: garantir número mínimo de estudantes
                st.error(f"É necessário ter pelo menos {tamanho_grupo} estudantes para formar grupos.")
            else:
                # Definir semente aleatória se informada
                if semente > 0:
                    random.seed(semente)
                
                # Formar os grupos com os parâmetros selecionados
                grupos = formar_grupos(
                    estudantes, 
                    tamanho_grupo, 
                    metodo, 
                    redistribuir_solitarios,
                    permitir_grupos_maiores
                )
                
                # Salvar no histórico para referência futura
                data_formatada = datetime.now().strftime("%d/%m/%Y %H:%M")
                if not descricao_grupo:
                    descricao_grupo = f"Grupos de {tamanho_grupo}"
                
                # Inicializar o histórico se não existir
                if 'historico_grupos' not in st.session_state:
                    st.session_state.historico_grupos = []
                
                # Adicionar a nova formação ao histórico
                st.session_state.historico_grupos.append({
                    "data": data_formatada,
                    "descricao": descricao_grupo,
                    "grupos": grupos,
                    "estudantes": estudantes,
                    "tamanho_grupo": tamanho_grupo,
                    "metodo": metodo
                })
                
                # Exibir grupos formados
                exibir_grupos(grupos, tamanho_grupo, estudantes)
                
                # Resetar semente aleatória para evitar persistência não intencional
                random.seed(None)

def processar_entrada_texto(texto_input):
    """
    Processa a entrada de texto e extrai os estudantes.
    
    Args:
        texto_input (str): Texto contendo os dados dos estudantes, um por linha
        
    Returns:
        list: Lista de dicionários com as informações dos estudantes
    """
    estudantes = []
    linhas_invalidas = []
    
    for linha in texto_input.split('\n'):
        linha = linha.strip()
        if not linha:
            continue
            
        # Verificar se a linha contém o formato correto (com vírgula separando matrícula e nome)
        if ',' in linha:
            # Formato padrão: "Matrícula, Nome"
            partes = linha.split(',', 1)  # Dividir apenas na primeira vírgula
            matricula = partes[0].strip()
            nome = partes[1].strip()
            estudantes.append({"matricula": matricula, "nome": nome, "completo": f"{matricula}, {nome}"})
        else:
            # Tentar identificar a matrícula (assumindo que são números no início)
            match = re.match(r'^(\d+)\s*(.*?)$', linha)
            if match:
                # Formato alternativo: "Matrícula Nome" (sem vírgula)
                matricula = match.group(1)
                nome = match.group(2).strip()
                estudantes.append({"matricula": matricula, "nome": nome, "completo": f"{matricula}, {nome}"})
            else:
                # Formato não reconhecido
                linhas_invalidas.append(linha)
    
    # Exibir avisos sobre linhas inválidas
    if linhas_invalidas:
        st.warning(f"Foram encontradas {len(linhas_invalidas)} linhas em formato inválido. Formato esperado: 'Matrícula, Nome'")
        with st.expander("Mostrar linhas inválidas"):
            for linha in linhas_invalidas:
                st.write(f"- {linha}")
    
    return estudantes

def formar_grupos(estudantes, tamanho_grupo, metodo="Aleatório", redistribuir_solitarios=True, permitir_grupos_maiores=True):
    """
    Forma grupos com o tamanho especificado usando o método selecionado.
    
    Args:
        estudantes (list): Lista de dicionários com dados dos estudantes
        tamanho_grupo (int): Tamanho desejado para cada grupo
        metodo (str): Método de formação de grupos ("Aleatório", "Sequencial", "Balanceado")
        redistribuir_solitarios (bool): Se deve redistribuir estudantes que ficariam sozinhos
        permitir_grupos_maiores (bool): Se permite grupos maiores que o tamanho_grupo
        
    Returns:
        list: Lista de grupos, onde cada grupo é uma lista de estudantes
    """
    estudantes_copia = estudantes.copy()
    
    # Aplicar o método selecionado
    if metodo == "Aleatório":
        # Embaralhar a lista para distribuição aleatória
        random.shuffle(estudantes_copia)
    elif metodo == "Balanceado":
        # Implementação simplificada de balanceamento
        # Primeiro ordenamos por algum critério
        estudantes_copia.sort(key=lambda x: x["matricula"])
        
        # Então alternamos a ordem para distribuir de forma mais balanceada
        # Isso evita que estudantes com características similares (como matrículas próximas)
        # fiquem todos no mesmo grupo
        estudantes_balanceados = []
        meio = len(estudantes_copia) // 2
        for i in range(meio):
            estudantes_balanceados.append(estudantes_copia[i])
            if i + meio < len(estudantes_copia):
                estudantes_balanceados.append(estudantes_copia[i + meio])
        
        # Adicionar qualquer estudante restante
        if len(estudantes_copia) % 2 != 0:
            estudantes_balanceados.append(estudantes_copia[-1])
            
        estudantes_copia = estudantes_balanceados
    # Para "Sequencial" não precisamos fazer nada, usamos a ordem original
    
    # Calcular número de grupos necessários
    num_grupos = math.ceil(len(estudantes_copia) / tamanho_grupo)
    
    # Formar os grupos iniciais
    grupos = []
    for i in range(num_grupos):
        inicio = i * tamanho_grupo
        fim = min(inicio + tamanho_grupo, len(estudantes_copia))
        grupo = estudantes_copia[inicio:fim]
        grupos.append(grupo)
    
    # Verificar se há algum grupo com apenas um aluno e redistribuir se necessário
    if redistribuir_solitarios:
        for i in range(len(grupos) - 1, -1, -1):
            if len(grupos[i]) == 1:
                aluno_sozinho = grupos[i][0]
                
                # Remover o grupo do aluno sozinho
                grupos.pop(i)
                
                # Encontrar o grupo com menos alunos para adicionar este aluno
                grupo_menor = min(grupos, key=len)
                if permitir_grupos_maiores or len(grupo_menor) < tamanho_grupo + 1:
                    # Adicionar ao grupo menor se permitido ou se não exceder o limite + 1
                    grupo_menor.append(aluno_sozinho)
                else:
                    # Se não permitir grupos maiores e todos já estão no limite, criar novo grupo
                    # Isso só deve acontecer em casos específicos onde a redistribuição não é possível
                    grupos.append([aluno_sozinho])
    
    return grupos

def exibir_grupos(grupos, tamanho_grupo, estudantes_originais):
    """
    Exibe os grupos formados na interface do Streamlit.
    
    Args:
        grupos (list): Lista de grupos formados
        tamanho_grupo (int): Tamanho alvo definido para os grupos
        estudantes_originais (list): Lista original de estudantes
    """
    st.subheader("Grupos Formados")
    
    # Opção para escolher como exibir os estudantes
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Formato de exibição dos estudantes
        formato_exibicao = st.radio(
            "Formato de exibição:",
            ["Matrícula e Nome", "Apenas Nome", "Apenas Matrícula"],
            horizontal=True
        )
    
    with col3:
        # Opções para exportar os grupos
        formato_exportacao = st.selectbox(
            "Exportar como:",
            ["CSV", "PDF", "Excel"]
        )
        
        if st.button(f"📋 Exportar {formato_exportacao}"):
            if formato_exportacao == "CSV":
                gerar_csv_grupos(grupos)
            elif formato_exportacao == "PDF":
                st.warning("Funcionalidade de exportação PDF em desenvolvimento.")
                # Implementação futura para PDF
            else:  # Excel
                gerar_excel_grupos(grupos)
    
    # Criar tabs para cada grupo e uma tab para visão geral
    tabs = ["Visão Geral"] + [f"Grupo {i+1}" for i in range(len(grupos))]
    tabs_group = st.tabs(tabs)
    
    # Tab de visão geral
    with tabs_group[0]:
        # Estatísticas dos grupos
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Grupos", len(grupos))
        with col2:
            st.metric("Total de Estudantes", sum(len(g) for g in grupos))
        with col3:
            tamanhos = [len(g) for g in grupos]
            st.metric("Menor Grupo", min(tamanhos))
        with col4:
            st.metric("Maior Grupo", max(tamanhos))
        
        # Tabela com todos os grupos
        dados_tabela = []
        for i, grupo in enumerate(grupos, 1):
            for estudante in grupo:
                dados_tabela.append({
                    "Grupo": i,
                    "Matrícula": estudante["matricula"],
                    "Nome": estudante["nome"]
                })
        
        df_grupos = pd.DataFrame(dados_tabela)
        st.dataframe(df_grupos, use_container_width=True)
        
        # Distribuição visual dos tamanhos dos grupos (gráfico de barras)
        st.subheader("Distribuição dos Grupos")
        dist_dados = {}
        for i, grupo in enumerate(grupos, 1):
            dist_dados[f"Grupo {i}"] = len(grupo)
        
        chart_data = pd.DataFrame({
            "Grupo": list(dist_dados.keys()),
            "Estudantes": list(dist_dados.values())
        })
        st.bar_chart(chart_data, x="Grupo", y="Estudantes", use_container_width=True)
    
    # Tabs para cada grupo individual
    for i, grupo in enumerate(grupos):
        with tabs_group[i+1]:
            st.subheader(f"Grupo {i+1} - {len(grupo)} estudantes")
            
            # Exibir membros do grupo no formato selecionado
            for j, estudante in enumerate(grupo, 1):
                if formato_exibicao == "Matrícula e Nome":
                    st.write(f"{j}. {estudante['completo']}")
                elif formato_exibicao == "Apenas Nome":
                    st.write(f"{j}. {estudante['nome']}")
                else:  # Apenas Matrícula
                    st.write(f"{j}. {estudante['matricula']}")
            
            # Opção para copiar lista do grupo
            texto_grupo = "\n".join([estudante[formato_display(formato_exibicao)] for estudante in grupo])
            st.download_button(
                label="📋 Copiar Lista",
                data=texto_grupo,
                file_name=f"grupo_{i+1}.txt",
                mime="text/plain"
            )
    
    # Verificar se há grupos com menos ou mais membros e mostrar mensagens informativas
    tamanhos = [len(grupo) for grupo in grupos]
    
    if min(tamanhos) < tamanho_grupo:
        # Se houver grupos menores que o tamanho padrão
        st.info(f"Nota: Alguns grupos têm menos estudantes ({min(tamanhos)}) porque o número total não é divisível por {tamanho_grupo}.")
    
    if max(tamanhos) > tamanho_grupo:
        # Se houver grupos maiores que o tamanho padrão
        st.info(f"Nota: Alguns grupos têm mais estudantes ({max(tamanhos)}) para evitar que alunos fiquem sozinhos.")

def formato_display(formato_exibicao):
    """
    Retorna a chave do dicionário a ser usada com base no formato de exibição.
    
    Args:
        formato_exibicao (str): Formato selecionado para exibição
        
    Returns:
        str: Chave correspondente no dicionário de estudante
    """
    if formato_exibicao == "Matrícula e Nome":
        return "completo"
    elif formato_exibicao == "Apenas Nome":
        return "nome"
    else:  # Apenas Matrícula
        return "matricula"

def gerar_csv_grupos(grupos):
    """
    Gera um arquivo CSV com os grupos e permite o download.
    
    Args:
        grupos (list): Lista de grupos formados
    """
    # Criar listas para o DataFrame
    grupo_nums = []
    matriculas = []
    nomes = []
    
    for i, grupo in enumerate(grupos, 1):
        for estudante in grupo:
            grupo_nums.append(i)
            matriculas.append(estudante['matricula'])
            nomes.append(estudante['nome'])
    
    # Criar DataFrame
    df = pd.DataFrame({
        'Grupo': grupo_nums,
        'Matrícula': matriculas,
        'Nome': nomes
    })
    
    # Converter para CSV
    csv = df.to_csv(index=False).encode('utf-8')
    
    # Criar um botão de download
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"grupos_estudantes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
    )

def gerar_excel_grupos(grupos):
    """
    Gera um arquivo Excel com os grupos e permite o download.
    
    Args:
        grupos (list): Lista de grupos formados
    """
    # Criar listas para o DataFrame
    grupo_nums = []
    matriculas = []
    nomes = []
    
    for i, grupo in enumerate(grupos, 1):
        for estudante in grupo:
            grupo_nums.append(i)
            matriculas.append(estudante['matricula'])
            nomes.append(estudante['nome'])
    
    # Criar DataFrame
    df = pd.DataFrame({
        'Grupo': grupo_nums,
        'Matrícula': matriculas,
        'Nome': nomes
    })
    
    # Salvar em um buffer de memória
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Grupos', index=False)
        # Ajustar largura das colunas para melhor visualização
        worksheet = writer.sheets['Grupos']
        worksheet.set_column('A:A', 10)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 30)
    
    # Preparar para download
    excel_data = output.getvalue()
    
    # Criar um botão de download
    st.download_button(
        label="Download Excel",
        data=excel_data,
        file_name=f"grupos_estudantes_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

def exibir_pagina_historico():
    """
    Exibe a página de histórico de grupos formados anteriormente.
    Permite visualizar, carregar e gerenciar grupos salvos.
    """
    st.title("Histórico de Grupos Formados")
    
    # Recuperar histórico da sessão
    historico = st.session_state.get('historico_grupos', [])
    
    if not historico:
        st.info("Nenhum histórico de grupos formados encontrado. Use a página 'Formar Grupos' para criar novos grupos.")
        return
    
    # Exibir cards para cada conjunto de grupos no histórico
    for i, item in enumerate(historico):
        with st.expander(f"{item['data']} - {item['descricao']} ({len(item['grupos'])} grupos)"):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                # Mostrar informações básicas do histórico
                st.write(f"**Data:** {item['data']}")
                st.write(f"**Método:** {item['metodo']}")
                st.write(f"**Tamanho alvo:** {item['tamanho_grupo']} estudantes por grupo")
            
            with col2:
                # Estatísticas deste conjunto de grupos
                grupos = item['grupos']
                tamanhos = [len(g) for g in grupos]
                st.write(f"**Total de estudantes:** {sum(tamanhos)}")
                st.write(f"**Tamanho do menor grupo:** {min(tamanhos)}")
                st.write(f"**Tamanho do maior grupo:** {max(tamanhos)}")
            
            with col3:
                # Opções para carregar ou excluir este histórico
                if st.button(f"Recarregar", key=f"recarregar_{i}"):
                    st.session_state.estudantes_carregados = item['estudantes']
                    st.success("Estudantes carregados! Vá para a aba 'Formar Grupos' para usá-los.")
                    
                if st.button(f"Excluir", key=f"excluir_{i}"):
                    st.session_state.historico_grupos.pop(i)
                    st.experimental_rerun()
            
            # Exibir tabela com os grupos deste histórico
            df_grupos = pd.DataFrame([(g_i+1, e['completo']) 
                                     for g_i, grupo in enumerate(grupos) 
                                     for e in grupo], 
                                     columns=['Grupo', 'Estudante'])
            st.dataframe(df_grupos, use_container_width=True)

def exibir_pagina_configuracoes():
    """
    Exibe a página de configurações da aplicação.
    Permite ajustar preferências e gerenciar dados salvos.
    """
    st.title("Configurações")
    
    st.subheader("Configurações da Aplicação")
    
    # Preferências para formação de grupos
    st.markdown("### Preferências de Formação de Grupos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Configurações padrão para tamanho e método
        tamanho_padrao = st.number_input(
            "Tamanho padrão dos grupos", 
            min_value=2, 
            max_value=10, 
            value=st.session_state.get('tamanho_padrao', 3)
        )
        
        metodo_padrao = st.selectbox(
            "Método padrão",
            ["Aleatório", "Sequencial", "Balanceado"],
            index=["Aleatório", "Sequencial", "Balanceado"].index(
                st.session_state.get('metodo_padrao', "Aleatório")
            )
        )
    
    with col2:
        # Preferências para redistribuição e tamanho dos grupos
        redistribuir_padrao = st.checkbox(
            "Redistribuir estudantes sozinhos por padrão",
            value=st.session_state.get('redistribuir_padrao', True)
        )
        
        permitir_maior_padrao = st.checkbox(
            "Permitir grupos maiores por padrão",
            value=st.session_state.get('permitir_maior_padrao', True)
        )
    
    # Salvar configurações na sessão
    if st.button("Salvar Configurações"):
        st.session_state.tamanho_padrao = tamanho_padrao
        st.session_state.metodo_padrao = metodo_padrao
        st.session_state.redistribuir_padrao = redistribuir_padrao
        st.session_state.permitir_maior_padrao = permitir_maior_padrao
        
        st.success("Configurações salvas com sucesso!")
    
    # Opções para limpar dados da aplicação
    st.markdown("### Gerenciamento de Dados")
    
    if st.button("Limpar Histórico", type="secondary"):
        if 'historico_grupos' in st.session_state:
            st.session_state.pop('historico_grupos')
            st.success("Histórico limpo com sucesso!")
            time.sleep(1)
            st.experimental_rerun()
    
    if st.button("Resetar Todas as Configurações", type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Todas as configurações foram resetadas!")
        time.sleep(1)
        st.experimental_rerun()
