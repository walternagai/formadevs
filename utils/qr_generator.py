"""
Módulo de geração de QR Codes.
Gera QR Codes com dados estruturados em JSON.
"""

import base64
import io
import json
from datetime import datetime

import qrcode


def gerar_qr_code_grupo(grupo, numero_grupo, formato="PNG"):
    """
    Gera um QR Code contendo dados estruturados JSON do grupo.

    Args:
        grupo (list): Lista de estudantes do grupo
        numero_grupo (int): Número identificador do grupo
        formato (str): Formato da imagem ('PNG', 'JPEG', 'SVG')

    Returns:
        dict: Dicionário com a imagem em base64 e os dados
    """
    # Estruturar dados em JSON
    dados_qr = {
        "tipo": "grupo_individual",
        "grupo_id": numero_grupo,
        "total_estudantes": len(grupo),
        "data_geracao": datetime.now().isoformat(),
        "versao": "2.0",
        "estudantes": [{"matricula": e.get("matricula", ""), "nome": e.get("nome", "")} for e in grupo],
    }

    # Converter para JSON string
    json_data = json.dumps(dados_qr, ensure_ascii=False, indent=None)

    # Gerar QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(json_data)
    qr.make(fit=True)

    # Criar imagem
    img = qr.make_image(fill_color="black", back_color="white")

    # Converter para bytes
    buffer = io.BytesIO()
    if formato.upper() == "PNG":
        img.save(buffer, format="PNG")
    elif formato.upper() == "JPEG":
        img = img.convert("RGB")  # JPEG não suporta transparência
        img.save(buffer, format="JPEG")

    # Converter para base64
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return {
        "imagem_base64": img_str,
        "formato": formato.upper(),
        "dados": dados_qr,
        "json_string": json_data,
    }


def gerar_qr_code_todos_grupos(grupos):
    """
    Gera um QR Code contendo todos os grupos.

    Args:
        grupos (list): Lista de todos os grupos

    Returns:
        dict: Dicionário com a imagem em base64 e os dados
    """
    # Estruturar todos os grupos
    dados_qr = {
        "tipo": "todos_grupos",
        "total_grupos": len(grupos),
        "total_estudantes": sum(len(g) for g in grupos),
        "data_geracao": datetime.now().isoformat(),
        "versao": "2.0",
        "grupos": [
            {
                "grupo_id": i + 1,
                "total_estudantes": len(grupo),
                "estudantes": [{"matricula": e.get("matricula", ""), "nome": e.get("nome", "")} for e in grupo],
            }
            for i, grupo in enumerate(grupos)
        ],
    }

    # Compactar JSON (sem indentação para economizar espaço no QR)
    json_data = json.dumps(dados_qr, ensure_ascii=False, separators=(",", ":"))

    # Gerar QR Code com maior capacidade
    qr = qrcode.QRCode(
        version=None,  # Auto-determinar versão
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(json_data)
    qr.make(fit=True)

    # Criar imagem
    img = qr.make_image(fill_color="black", back_color="white")

    # Converter para bytes
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    # Converter para base64
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return {
        "imagem_base64": img_str,
        "formato": "PNG",
        "dados": dados_qr,
        "json_string": json_data,
    }


def gerar_qr_code_simples(texto):
    """
    Gera um QR Code simples com texto puro.

    Args:
        texto (str): Texto a ser codificado

    Returns:
        dict: Dicionário com a imagem em base64
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(texto)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return {"imagem_base64": img_str, "formato": "PNG", "texto": texto}


def gerar_qr_batch(grupos):
    """
    Gera QR Codes para todos os grupos em lote.

    Args:
        grupos (list): Lista de grupos

    Returns:
        list: Lista de dicionários com QR Codes individuais
    """
    resultados = []

    for i, grupo in enumerate(grupos, 1):
        qr_data = gerar_qr_code_grupo(grupo, i)
        resultados.append({"grupo_numero": i, "qr_data": qr_data})

    return resultados


def verificar_dados_qr(json_string):
    """
    Verifica e decodifica dados de um QR Code.

    Args:
        json_string (str): String JSON do QR Code

    Returns:
        dict: Dados decodificados ou None se inválido
    """
    try:
        dados = json.loads(json_string)
        return dados
    except json.JSONDecodeError:
        return None
