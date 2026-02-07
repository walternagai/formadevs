"""
Módulo de componentes reutilizáveis.
Contém componentes UI padronizados para uso em toda a aplicação.
"""

import streamlit as st


def card_estudante(estudante, numero=None, destacar=False):
    """
    Exibe um card de estudante.
    
    Args:
        estudante (dict): Dados do estudante
        numero (int, optional): Número de exibição
        destacar (bool): Se deve destacar o card
    """
    matricula = estudante.get('matricula', '')
    nome = estudante.get('nome', '')
    completo = estudante.get('completo', f"{matricula}, {nome}")
    
    bg_color = "#e3f2fd" if destacar else "#f5f5f5"
    border_color = "#2196F3" if destacar else "#ddd"
    
    st.markdown(f"""
    <div style="
        background-color: {bg_color};
        border-left: 4px solid {border_color};
        padding: 10px;
        margin: 5px 0;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    ">
        <span style="font-weight: bold; color: #333;">
            {f"{numero}. " if numero else ""}{completo}
        </span>
    </div>
    """, unsafe_allow_html=True)


def card_grupo(grupo, numero, expandido=False):
    """
    Exibe um card de grupo com estatísticas.
    
    Args:
        grupo (list): Lista de estudantes
        numero (int): Número do grupo
        expandido (bool): Se deve mostrar expandido por padrão
    """
    with st.expander(f"Grupo {numero} - {len(grupo)} estudantes", expanded=expandido):
        for i, estudante in enumerate(grupo, 1):
            st.write(f"{i}. {estudante.get('completo', '')}")


def card_estatistica(titulo, valor, icone="📊", cor="#4CAF50"):
    """
    Exibe um card de estatística.
    
    Args:
        titulo (str): Título da estatística
        valor: Valor a ser exibido
        icone (str): Ícone emoji
        cor (str): Cor do card (hex)
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {cor}22, {cor}11);
        border: 1px solid {cor}44;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 5px;
    ">
        <div style="font-size: 32px; margin-bottom: 5px;">{icone}</div>
        <div style="font-size: 24px; font-weight: bold; color: {cor};">{valor}</div>
        <div style="font-size: 12px; color: #666; text-transform: uppercase;">{titulo}</div>
    </div>
    """, unsafe_allow_html=True)


def alerta_info(mensagem):
    """Exibe um alerta de informação estilizado."""
    st.markdown(f"""
    <div style="
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
        color: #1565C0;
    ">
        ℹ️ {mensagem}
    </div>
    """, unsafe_allow_html=True)


def alerta_sucesso(mensagem):
    """Exibe um alerta de sucesso estilizado."""
    st.markdown(f"""
    <div style="
        background-color: #e8f5e9;
        border-left: 4px solid #4CAF50;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
        color: #2E7D32;
    ">
        ✅ {mensagem}
    </div>
    """, unsafe_allow_html=True)


def alerta_aviso(mensagem):
    """Exibe um alerta de aviso estilizado."""
    st.markdown(f"""
    <div style="
        background-color: #fff3e0;
        border-left: 4px solid #FF9800;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
        color: #E65100;
    ">
        ⚠️ {mensagem}
    </div>
    """, unsafe_allow_html=True)


def alerta_erro(mensagem):
    """Exibe um alerta de erro estilizado."""
    st.markdown(f"""
    <div style="
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
        color: #c62828;
    ">
        ❌ {mensagem}
    </div>
    """, unsafe_allow_html=True)


def botao_acao(label, tipo="primario", icone="", key=None):
    """
    Cria um botão de ação padronizado.
    
    Args:
        label (str): Texto do botão
        tipo (str): Tipo do botão ('primario', 'secundario', 'perigo')
        icone (str): Ícone emoji
        key (str): Chave única do botão
        
    Returns:
        bool: True se o botão foi clicado
    """
    cores = {
        "primario": "#4CAF50",
        "secundario": "#757575",
        "perigo": "#f44336"
    }
    
    cor = cores.get(tipo, "#4CAF50")
    
    # Usar st.button nativo mas com estilo customizado
    css = f"""
    <style>
    div[data-testid="stButton"] > button:first-child {{
        background-color: {cor};
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s;
    }}
    div[data-testid="stButton"] > button:first-child:hover {{
        opacity: 0.8;
        transform: translateY(-2px);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    
    return st.button(f"{icone} {label}" if icone else label, key=key, type="primary" if tipo == "primario" else "secondary")


def badge(texto, cor="blue"):
    """
    Exibe um badge estilizado.
    
    Args:
        texto (str): Texto do badge
        cor (str): Cor do badge ('blue', 'green', 'red', 'yellow', 'gray')
    """
    cores = {
        "blue": "#2196F3",
        "green": "#4CAF50",
        "red": "#f44336",
        "yellow": "#FF9800",
        "gray": "#757575"
    }
    
    cor_hex = cores.get(cor, "#757575")
    
    st.markdown(f"""
    <span style="
        background-color: {cor_hex}22;
        color: {cor_hex};
        border: 1px solid {cor_hex};
        border-radius: 12px;
        padding: 2px 8px;
        font-size: 12px;
        font-weight: bold;
    ">{texto}</span>
    """, unsafe_allow_html=True)


def divisoria(titulo=None):
    """Exibe uma divisória visual opcionalmente com título."""
    if titulo:
        st.markdown(f"""
        <div style="
            border-bottom: 2px solid #e0e0e0;
            margin: 20px 0 15px 0;
            padding-bottom: 5px;
        ">
            <span style="
                font-weight: bold;
                color: #666;
                font-size: 14px;
                text-transform: uppercase;
            ">{titulo}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.divider()
