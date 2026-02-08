"""
Módulo de funções utilitárias auxiliares.
"""

import re
from datetime import datetime


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
    else:
        return "matricula"


def formatar_data(data_str, formato_entrada="%d/%m/%Y %H:%M", formato_saida="%d/%m/%Y %H:%M"):
    """
    Formata uma data de um formato para outro.

    Args:
        data_str (str): String da data
        formato_entrada (str): Formato da data de entrada
        formato_saida (str): Formato desejado de saída

    Returns:
        str: Data formatada ou string original se erro
    """
    try:
        data = datetime.strptime(data_str, formato_entrada)
        return data.strftime(formato_saida)
    except ValueError:
        return data_str


def sanitize_filename(filename):
    """
    Sanitiza um nome de arquivo removendo caracteres inválidos.

    Args:
        filename (str): Nome do arquivo original

    Returns:
        str: Nome do arquivo sanitizado
    """
    filename = re.sub(r'[<>:"/\\|?*]', "", filename)
    if len(filename) > 200:
        if "." in filename:
            name, ext = filename.rsplit(".", 1)
            filename = name[:195] + "." + ext
        else:
            filename = filename[:200]
    return filename


def contar_estudantes_unicos(historico):
    """
    Conta estudantes únicos em todo o histórico.

    Args:
        historico (list): Lista de itens do histórico

    Returns:
        int: Número de estudantes únicos
    """
    matriculas_unicas = set()

    for item in historico:
        for estudante in item.get("estudantes", []):
            matricula = str(estudante.get("matricula", ""))
            if matricula:
                matriculas_unicas.add(matricula)

    return len(matriculas_unicas)


def formatar_numero_grupo(numero, total):
    """
    Formata o número do grupo com padding para ordenação.

    Args:
        numero (int): Número do grupo
        total (int): Total de grupos

    Returns:
        str: Número formatado
    """
    digits = len(str(total))
    return f"Grupo {str(numero).zfill(digits)}"


def calcular_duracao_formatada(data_inicio, data_fim=None):
    """
    Calcula a duração formatada entre duas datas.

    Args:
        data_inicio (str): Data de início
        data_fim (str, optional): Data de fim (usa atual se não fornecida)

    Returns:
        str: Duração formatada
    """
    try:
        fmt = "%d/%m/%Y %H:%M"
        inicio = datetime.strptime(data_inicio, fmt)

        if data_fim:
            fim = datetime.strptime(data_fim, fmt)
        else:
            fim = datetime.now()

        diff = fim - inicio

        if diff.days > 0:
            return f"{diff.days} dia(s) atrás"
        elif diff.seconds >= 3600:
            horas = diff.seconds // 3600
            return f"{horas} hora(s) atrás"
        elif diff.seconds >= 60:
            minutos = diff.seconds // 60
            return f"{minutos} minuto(s) atrás"
        else:
            return "Agora mesmo"
    except ValueError:
        return "Data desconhecida"


def truncar_texto(texto, max_len=50, sufixo="..."):
    """
    Trunca um texto para um tamanho máximo.

    Args:
        texto (str): Texto original
        max_len (int): Tamanho máximo
        sufixo (str): Sufixo para indicar truncamento

    Returns:
        str: Texto truncado
    """
    if len(texto) <= max_len:
        return texto
    return texto[: max_len - len(sufixo)] + sufixo
