"""
Módulo de visualização de grupos.
Contém componentes para exibir grupos formados com estatísticas e exportações.
"""

import base64

import pandas as pd
import streamlit as st

from logic.group_formation import calcular_estatisticas
from ui.animations import animacao_sorteio_flip_cards
from ui.components import alerta_info, card_estatistica
from utils.exporters import gerar_csv_grupos, gerar_excel_grupos
from utils.helpers import formato_display
from utils.qr_generator import gerar_qr_code_grupo, gerar_qr_code_todos_grupos


def exibir_grupos(grupos, tamanho_grupo, estudantes_originais, show_animation=True):
    """
    Exibe os grupos formados com todas as opções de visualização.

    Args:
        grupos (list): Lista de grupos formados
        tamanho_grupo (int): Tamanho alvo dos grupos
        estudantes_originais (list): Lista original de estudantes
        show_animation (bool): Se deve mostrar animação de revelação
    """
    st.subheader("🎉 Grupos Formados")

    # Animação de sorteio (opcional)
    if show_animation:
        usar_animacao = st.checkbox("🎬 Mostrar animação de sorteio", value=True)
        if usar_animacao:
            animacao_sorteio_flip_cards(grupos)
            st.divider()

    # Estatísticas
    stats = calcular_estatisticas(grupos)

    st.markdown("**📊 Estatísticas**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card_estatistica("Total Grupos", stats["total_grupos"], "📦", "#2196F3")
    with col2:
        card_estatistica("Total Estudantes", stats["total_estudantes"], "👥", "#4CAF50")
    with col3:
        card_estatistica("Menor Grupo", stats["menor_grupo"], "📉", "#FF9800")
    with col4:
        card_estatistica("Maior Grupo", stats["maior_grupo"], "📈", "#9C27B0")

    # Opções de formato de exibição
    st.divider()

    col1, col2 = st.columns([3, 2])

    with col1:
        formato_exibicao = st.radio(
            "Formato de exibição:",
            ["Matrícula e Nome", "Apenas Nome", "Apenas Matrícula"],
            horizontal=True,
            key="formato_exibicao_grupos",
        )

    with col2:
        # Exportação
        st.markdown("**📤 Exportar**")

        exp_col1, exp_col2 = st.columns(2)

        with exp_col1:
            # CSV
            csv_data, csv_filename = gerar_csv_grupos(grupos)
            st.download_button(
                "📄 CSV",
                data=csv_data,
                file_name=csv_filename,
                mime="text/csv",
                use_container_width=True,
            )

        with exp_col2:
            # Excel
            excel_data, excel_filename = gerar_excel_grupos(grupos)
            st.download_button(
                "📊 Excel",
                data=excel_data,
                file_name=excel_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

    # QR Codes
    with st.expander("📱 QR Codes"):
        qr_option = st.radio("Gerar QR Code:", ["Por Grupo", "Todos os Grupos"], horizontal=True)

        if qr_option == "Por Grupo":
            qr_grupo_num = st.selectbox(
                "Selecione o grupo:",
                range(1, len(grupos) + 1),
                format_func=lambda x: f"Grupo {x} ({len(grupos[x - 1])} estudantes)",
            )

            if st.button("🎯 Gerar QR Code do Grupo"):
                qr_data = gerar_qr_code_grupo(grupos[qr_grupo_num - 1], qr_grupo_num)

                st.markdown(f"**QR Code - Grupo {qr_grupo_num}**")
                st.markdown(
                    f"<small>Contém dados JSON com {len(grupos[qr_grupo_num - 1])} estudantes</small>",
                    unsafe_allow_html=True,
                )

                # Exibir imagem
                st.image(f"data:image/png;base64,{qr_data['imagem_base64']}", width=300)

                # Download
                img_bytes = base64.b64decode(qr_data["imagem_base64"])
                st.download_button(
                    "⬇️ Download QR Code",
                    data=img_bytes,
                    file_name=f"qr_grupo_{qr_grupo_num}.png",
                    mime="image/png",
                )
        else:
            if st.button("🎯 Gerar QR Code de Todos os Grupos"):
                qr_data = gerar_qr_code_todos_grupos(grupos)

                st.markdown("**QR Code - Todos os Grupos**")
                st.markdown(
                    f"<small>Contém dados JSON com {len(grupos)} grupos</small>",
                    unsafe_allow_html=True,
                )

                # Exibir imagem
                st.image(f"data:image/png;base64,{qr_data['imagem_base64']}", width=400)

                # Download
                img_bytes = base64.b64decode(qr_data["imagem_base64"])
                st.download_button(
                    "⬇️ Download QR Code",
                    data=img_bytes,
                    file_name="qr_todos_grupos.png",
                    mime="image/png",
                )

    # Tabs para visualização
    st.divider()

    tabs = ["📊 Visão Geral"] + [f"👥 Grupo {i + 1}" for i in range(len(grupos))]
    tabs_group = st.tabs(tabs)

    # Tab de visão geral
    with tabs_group[0]:
        exibir_visao_geral(grupos, formato_exibicao)

    # Tabs para cada grupo
    for i, grupo in enumerate(grupos):
        with tabs_group[i + 1]:
            exibir_grupo_individual(grupo, i + 1, formato_exibicao)

    # Avisos sobre tamanhos
    if stats["menor_grupo"] < tamanho_grupo:
        alerta_info(
            f"Alguns grupos têm menos estudantes ({stats['menor_grupo']}) porque o número total não é divisível por {tamanho_grupo}."
        )

    if stats["maior_grupo"] > tamanho_grupo:
        alerta_info(
            f"Alguns grupos têm mais estudantes ({stats['maior_grupo']}) para evitar que alunos fiquem sozinhos."
        )


def exibir_visao_geral(grupos, formato_exibicao):
    """Exibe a visão geral de todos os grupos em uma tabela."""
    # Criar DataFrame
    dados_tabela = []
    for i, grupo in enumerate(grupos, 1):
        for estudante in grupo:
            dados_tabela.append(
                {
                    "Grupo": i,
                    "Matrícula": estudante.get("matricula", ""),
                    "Nome": estudante.get("nome", ""),
                }
            )

    df_grupos = pd.DataFrame(dados_tabela)
    st.dataframe(df_grupos, use_container_width=True)

    # Gráfico de distribuição
    st.markdown("**📊 Distribuição dos Grupos**")
    dist_dados = {f"Grupo {i + 1}": len(grupo) for i, grupo in enumerate(grupos)}

    chart_data = pd.DataFrame({"Grupo": list(dist_dados.keys()), "Estudantes": list(dist_dados.values())})
    st.bar_chart(chart_data, x="Grupo", y="Estudantes", use_container_width=True)


def exibir_grupo_individual(grupo, numero, formato_exibicao):
    """Exibe um grupo individual com opções de exportação."""
    st.markdown(f"**Grupo {numero}** - {len(grupo)} estudantes")

    # Lista de estudantes
    for i, estudante in enumerate(grupo, 1):
        chave = formato_display(formato_exibicao)
        st.write(f"{i}. {estudante.get(chave, '')}")

    # Opção de download individual
    texto_grupo = "\n".join([estudante.get(formato_display(formato_exibicao), "") for estudante in grupo])

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📋 Copiar Lista",
            data=texto_grupo,
            file_name=f"grupo_{numero}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col2:
        # QR Code individual
        if st.button("📱 QR Code", key=f"qr_{numero}", use_container_width=True):
            import base64

            from utils.qr_generator import gerar_qr_code_grupo

            qr_data = gerar_qr_code_grupo(grupo, numero)
            st.image(f"data:image/png;base64,{qr_data['imagem_base64']}", width=200)

            img_bytes = base64.b64decode(qr_data["imagem_base64"])
            st.download_button(
                "⬇️ Download",
                data=img_bytes,
                file_name=f"qr_grupo_{numero}.png",
                mime="image/png",
                key=f"dl_qr_{numero}",
            )
