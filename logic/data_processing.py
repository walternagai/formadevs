"""
Módulo de processamento de dados.
Funções auxiliares para processar diferentes formatos de entrada.
"""

import pandas as pd


def processar_csv_para_estudantes(df, col_matricula, col_nome):
    """
    Converte um DataFrame CSV em lista de estudantes.

    Args:
        df (DataFrame): DataFrame do pandas
        col_matricula (str): Nome da coluna de matrícula
        col_nome (str): Nome da coluna de nome

    Returns:
        list: Lista de dicionários de estudantes
    """
    estudantes = []

    for _, row in df.iterrows():
        matricula = str(row[col_matricula]).strip() if pd.notna(row[col_matricula]) else ""
        nome = str(row[col_nome]).strip() if pd.notna(row[col_nome]) else ""

        if matricula and nome:
            estudantes.append(
                {
                    "matricula": matricula,
                    "nome": nome,
                    "completo": f"{matricula}, {nome}",
                }
            )

    return estudantes


def preparar_dados_exportacao(grupos):
    """
    Prepara dados dos grupos para exportação em diferentes formatos.

    Args:
        grupos (list): Lista de grupos

    Returns:
        list: Lista de dicionários prontos para exportação
    """
    dados = []

    for i, grupo in enumerate(grupos, 1):
        for estudante in grupo:
            dados.append(
                {
                    "Grupo": i,
                    "Matrícula": estudante.get("matricula", ""),
                    "Nome": estudante.get("nome", ""),
                    "Completo": estudante.get("completo", ""),
                }
            )

    return dados


def criar_dataframe_grupos(grupos):
    """
    Cria um DataFrame pandas a partir dos grupos.

    Args:
        grupos (list): Lista de grupos

    Returns:
        DataFrame: DataFrame com os dados dos grupos
    """
    dados = preparar_dados_exportacao(grupos)
    return pd.DataFrame(dados)


def filtrar_estudantes_por_grupo(grupos, numero_grupo):
    """
    Retorna os estudantes de um grupo específico.

    Args:
        grupos (list): Lista de todos os grupos
        numero_grupo (int): Número do grupo desejado (1-indexed)

    Returns:
        list: Lista de estudantes do grupo ou lista vazia
    """
    if 1 <= numero_grupo <= len(grupos):
        return grupos[numero_grupo - 1]
    return []
