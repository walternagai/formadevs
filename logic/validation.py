"""
Módulo de validação de dados de estudantes.
Contém funções para validar e detectar problemas nos dados de entrada.
"""

import re


def validar_formato_entrada(linha):
    """
    Valida se uma linha de entrada está no formato correto.
    
    Args:
        linha (str): Linha de texto a ser validada
        
    Returns:
        tuple: (bool, dict or str) - (válido, dados ou mensagem de erro)
    """
    linha = linha.strip()
    
    if not linha:
        return True, None  # Linhas vazias são ignoradas
    
    # Formato padrão: "Matrícula, Nome"
    if ',' in linha:
        partes = linha.split(',', 1)
        matricula = partes[0].strip()
        nome = partes[1].strip()
        
        if not matricula or not nome:
            return False, "Matrícula ou nome vazio"
        
        return True, {
            "matricula": matricula,
            "nome": nome,
            "completo": f"{matricula}, {nome}"
        }
    
    # Formato alternativo: "Matrícula Nome" (sem vírgula)
    match = re.match(r'^(\d+)\s*(.*?)$', linha)
    if match:
        matricula = match.group(1)
        nome = match.group(2).strip()
        
        if not nome:
            return False, "Nome não encontrado após matrícula"
        
        return True, {
            "matricula": matricula,
            "nome": nome,
            "completo": f"{matricula}, {nome}"
        }
    
    return False, "Formato não reconhecido. Use 'Matrícula, Nome' ou 'Matrícula Nome'"


def validar_duplicatas(estudantes):
    """
    Detecta matrículas duplicadas na lista de estudantes.
    
    Args:
        estudantes (list): Lista de dicionários de estudantes
        
    Returns:
        dict: Dicionário com matrículas duplicadas e suas ocorrências
    """
    matriculas_count = {}
    
    for i, estudante in enumerate(estudantes):
        matricula = str(estudante.get("matricula", "")).strip()
        if matricula:
            if matricula not in matriculas_count:
                matriculas_count[matricula] = {
                    "count": 0,
                    "indices": [],
                    "nomes": []
                }
            matriculas_count[matricula]["count"] += 1
            matriculas_count[matricula]["indices"].append(i)
            matriculas_count[matricula]["nomes"].append(estudante.get("nome", ""))
    
    # Filtrar apenas duplicatas
    duplicatas = {
        matricula: info 
        for matricula, info in matriculas_count.items() 
        if info["count"] > 1
    }
    
    return duplicatas


def validar_csv(df, col_matricula, col_nome):
    """
    Valida um DataFrame importado de CSV.
    
    Args:
        df (DataFrame): DataFrame do pandas
        col_matricula (str): Nome da coluna de matrícula
        col_nome (str): Nome da coluna de nome
        
    Returns:
        tuple: (bool, list or str) - (válido, lista de erros)
    """
    erros = []
    
    # Verificar se as colunas existem
    if col_matricula not in df.columns:
        erros.append(f"Coluna '{col_matricula}' não encontrada")
    if col_nome not in df.columns:
        erros.append(f"Coluna '{col_nome}' não encontrada")
    
    if erros:
        return False, erros
    
    # Verificar valores vazios
    matriculas_vazias = df[col_matricula].isna().sum()
    nomes_vazios = df[col_nome].isna().sum()
    
    if matriculas_vazias > 0:
        erros.append(f"{matriculas_vazias} matrículas vazias encontradas")
    if nomes_vazios > 0:
        erros.append(f"{nomes_vazios} nomes vazios encontrados")
    
    # Verificar duplicatas
    matriculas = df[col_matricula].dropna().astype(str).str.strip()
    duplicatas = matriculas[matriculas.duplicated(keep=False)]
    
    if not duplicatas.empty:
        valores_dup = duplicatas.unique()
        erros.append(f"Matrículas duplicadas: {', '.join(valores_dup[:5])}")
    
    return len(erros) == 0, erros


def processar_entrada_com_validacao(texto_input):
    """
    Processa entrada de texto com validação completa.
    
    Args:
        texto_input (str): Texto contendo dados dos estudantes
        
    Returns:
        dict: Resultado do processamento com estudantes, erros e duplicatas
    """
    estudantes = []
    erros_linhas = []
    
    for num_linha, linha in enumerate(texto_input.split('\n'), 1):
        valido, resultado = validar_formato_entrada(linha)
        
        if resultado is None:
            continue  # Linha vazia
        
        if valido:
            estudantes.append(resultado)
        else:
            erros_linhas.append({
                "linha": num_linha,
                "conteudo": linha.strip(),
                "erro": resultado
            })
    
    # Verificar duplicatas
    duplicatas = validar_duplicatas(estudantes)
    
    return {
        "estudantes": estudantes,
        "total": len(estudantes),
        "erros": erros_linhas,
        "duplicatas": duplicatas,
        "valido": len(erros_linhas) == 0
    }


def extrair_preview_dados(texto_input, limite=5):
    """
    Extrai um preview dos dados para exibição antes do processamento completo.
    
    Args:
        texto_input (str): Texto de entrada
        limite (int): Número máximo de linhas para preview
        
    Returns:
        dict: Preview dos dados com estatísticas
    """
    linhas = [l.strip() for l in texto_input.split('\n') if l.strip()]
    total_linhas = len(linhas)
    
    preview = []
    for i, linha in enumerate(linhas[:limite]):
        valido, resultado = validar_formato_entrada(linha)
        preview.append({
            "linha": i + 1,
            "conteudo": linha,
            "valido": valido,
            "dados": resultado if valido else None
        })
    
    # Contar linhas válidas e inválidas no preview
    validas = sum(1 for p in preview if p["valido"])
    
    return {
        "total_linhas": total_linhas,
        "mostradas": len(preview),
        "preview": preview,
        "validas_preview": validas,
        "invalidas_preview": len(preview) - validas
    }
