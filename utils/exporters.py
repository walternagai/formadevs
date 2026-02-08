"""
Módulo de exportação de dados.
Contém funções para exportar grupos em diferentes formatos.
"""

import io
from datetime import datetime

import pandas as pd


def gerar_csv_grupos(grupos):
    """
    Gera dados CSV dos grupos.

    Args:
        grupos (list): Lista de grupos

    Returns:
        tuple: (bytes, filename) - Dados CSV e nome do arquivo sugerido
    """
    # Criar listas para o DataFrame
    grupo_nums = []
    matriculas = []
    nomes = []

    for i, grupo in enumerate(grupos, 1):
        for estudante in grupo:
            grupo_nums.append(i)
            matriculas.append(estudante.get("matricula", ""))
            nomes.append(estudante.get("nome", ""))

    # Criar DataFrame
    df = pd.DataFrame({"Grupo": grupo_nums, "Matrícula": matriculas, "Nome": nomes})

    # Converter para CSV
    csv = df.to_csv(index=False).encode("utf-8")

    filename = f"grupos_estudantes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

    return csv, filename


def gerar_excel_grupos(grupos):
    """
    Gera arquivo Excel dos grupos.

    Args:
        grupos (list): Lista de grupos

    Returns:
        tuple: (bytes, filename) - Dados Excel e nome do arquivo sugerido
    """
    # Criar listas para o DataFrame
    grupo_nums = []
    matriculas = []
    nomes = []

    for i, grupo in enumerate(grupos, 1):
        for estudante in grupo:
            grupo_nums.append(i)
            matriculas.append(estudante.get("matricula", ""))
            nomes.append(estudante.get("nome", ""))

    # Criar DataFrame
    df = pd.DataFrame({"Grupo": grupo_nums, "Matrícula": matriculas, "Nome": nomes})

    # Salvar em um buffer de memória
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Grupos", index=False)
        # Ajustar largura das colunas para melhor visualização
        worksheet = writer.sheets["Grupos"]
        worksheet.set_column("A:A", 10)
        worksheet.set_column("B:B", 15)
        worksheet.set_column("C:C", 30)

    # Preparar para download
    excel_data = output.getvalue()

    filename = f"grupos_estudantes_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"

    return excel_data, filename


def gerar_txt_grupos(grupos, formato_exibicao="completo"):
    """
    Gera arquivo texto simples dos grupos.

    Args:
        grupos (list): Lista de grupos
        formato_exibicao (str): Formato de exibição ('completo', 'nome', 'matricula')

    Returns:
        tuple: (str, filename) - Conteúdo texto e nome do arquivo
    """
    linhas = []

    for i, grupo in enumerate(grupos, 1):
        linhas.append(f"Grupo {i} ({len(grupo)} estudantes)")
        linhas.append("=" * 40)

        for j, estudante in enumerate(grupo, 1):
            if formato_exibicao == "nome":
                linhas.append(f"{j}. {estudante.get('nome', '')}")
            elif formato_exibicao == "matricula":
                linhas.append(f"{j}. {estudante.get('matricula', '')}")
            else:  # completo
                linhas.append(f"{j}. {estudante.get('completo', '')}")

        linhas.append("")  # Linha em branco entre grupos

    conteudo = "\n".join(linhas)
    filename = f"grupos_estudantes_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"

    return conteudo, filename


def gerar_lista_simples(grupo, formato_exibicao="completo"):
    """
    Gera uma lista simples de texto para um único grupo.

    Args:
        grupo (list): Lista de estudantes de um grupo
        formato_exibicao (str): Formato de exibição

    Returns:
        str: Texto formatado
    """
    linhas = []

    for estudante in grupo:
        if formato_exibicao == "nome":
            linhas.append(estudante.get("nome", ""))
        elif formato_exibicao == "matricula":
            linhas.append(estudante.get("matricula", ""))
        else:  # completo
            linhas.append(estudante.get("completo", ""))

    return "\n".join(linhas)
