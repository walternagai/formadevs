"""
Módulo de processamento e formação de grupos.
Contém todas as funções relacionadas à lógica de formação de grupos.
"""

import random
import math


def formar_grupos(estudantes, tamanho_grupo, metodo="Aleatório", 
                  redistribuir_solitarios=True, permitir_grupos_maiores=True, semente=None):
    """
    Forma grupos com o tamanho especificado usando o método selecionado.
    
    Args:
        estudantes (list): Lista de dicionários com dados dos estudantes
        tamanho_grupo (int): Tamanho desejado para cada grupo
        metodo (str): Método de formação de grupos ("Aleatório", "Sequencial", "Balanceado")
        redistribuir_solitarios (bool): Se deve redistribuir estudantes que ficariam sozinhos
        permitir_grupos_maiores (bool): Se permite grupos maiores que o tamanho_grupo
        semente (int, optional): Semente para reprodutibilidade do sorteio aleatório
        
    Returns:
        list: Lista de grupos, onde cada grupo é uma lista de estudantes
    """
    if not estudantes:
        return []
    
    estudantes_copia = estudantes.copy()
    
    # Aplicar o método selecionado
    if metodo == "Aleatório":
        if semente is not None:
            random.seed(semente)
        random.shuffle(estudantes_copia)
        if semente is not None:
            random.seed(None)  # Resetar para evitar afetar outros sorteios
    elif metodo == "Balanceado":
        # Ordenar por matrícula para distribuição balanceada
        estudantes_copia.sort(key=lambda x: x.get("matricula", ""))
        
        # Alternar ordem para distribuir de forma mais balanceada
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
        grupos = redistribuir_solitarios_func(grupos, tamanho_grupo, permitir_grupos_maiores)
    
    return grupos


def redistribuir_solitarios_func(grupos, tamanho_grupo, permitir_grupos_maiores):
    """
    Redistribui estudantes que ficariam sozinhos em grupos.
    
    Args:
        grupos (list): Lista de grupos atuais
        tamanho_grupo (int): Tamanho alvo dos grupos
        permitir_grupos_maiores (bool): Se permite grupos maiores que o tamanho_grupo
        
    Returns:
        list: Lista de grupos redistribuídos
    """
    if not grupos:
        return grupos
    
    # Encontrar grupos com apenas 1 estudante
    i = len(grupos) - 1
    while i >= 0:
        if len(grupos[i]) == 1:
            aluno_sozinho = grupos[i][0]
            grupos.pop(i)
            
            if grupos:  # Se ainda há outros grupos
                # Encontrar o grupo com menos alunos
                grupo_menor = min(grupos, key=len)
                if permitir_grupos_maiores or len(grupo_menor) < tamanho_grupo:
                    grupo_menor.append(aluno_sozinho)
                else:
                    # Se não permitir grupos maiores, criar novo grupo
                    grupos.append([aluno_sozinho])
            else:
                # Se não há mais grupos, recriar o grupo com o aluno solitário
                grupos.append([aluno_sozinho])
        i -= 1
    
    return grupos


def calcular_estatisticas(grupos):
    """
    Calcula estatísticas dos grupos formados.
    
    Args:
        grupos (list): Lista de grupos
        
    Returns:
        dict: Dicionário com estatísticas
    """
    if not grupos:
        return {
            "total_grupos": 0,
            "total_estudantes": 0,
            "menor_grupo": 0,
            "maior_grupo": 0,
            "media": 0,
            "tamanhos": []
        }
    
    tamanhos = [len(grupo) for grupo in grupos]
    total_estudantes = sum(tamanhos)
    
    return {
        "total_grupos": len(grupos),
        "total_estudantes": total_estudantes,
        "menor_grupo": min(tamanhos),
        "maior_grupo": max(tamanhos),
        "media": total_estudantes / len(grupos),
        "tamanhos": tamanhos
    }


def sortear_grupo_ao_vivo(estudantes, tamanho_grupo, callback=None):
    """
    Prepara dados para sorteio ao vivo com animação.
    Retorna lista de grupos já formados, mas prepara estrutura para animação.
    
    Args:
        estudantes (list): Lista de estudantes
        tamanho_grupo (int): Tamanho de cada grupo
        callback (callable, optional): Função a ser chamada durante o sorteio
        
    Returns:
        list: Grupos formados no formato para animação
    """
    import random
    
    estudantes_copia = estudantes.copy()
    random.shuffle(estudantes_copia)
    
    num_grupos = math.ceil(len(estudantes_copia) / tamanho_grupo)
    
    # Preparar estrutura para animação
    grupos_animacao = []
    for i in range(num_grupos):
        inicio = i * tamanho_grupo
        fim = min(inicio + tamanho_grupo, len(estudantes_copia))
        grupo = estudantes_copia[inicio:fim]
        
        grupos_animacao.append({
            "numero": i + 1,
            "estudantes": grupo,
            "revelado": False
        })
    
    return grupos_animacao
