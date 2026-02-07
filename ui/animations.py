"""
Módulo de animações.
Contém funções para animações visuais, incluindo sorteio ao vivo com flip cards.
"""

import time
import streamlit as st


def animacao_sorteio_flip_cards(grupos, delay=1.5):
    """
    Exibe animação de sorteio com efeito de cards virando (flip cards).
    
    Args:
        grupos (list): Lista de grupos a serem revelados
        delay (float): Delay entre revelações em segundos
    """
    # CSS para o efeito de flip card
    flip_css = """
    <style>
    .flip-card {
        background-color: transparent;
        width: 100%;
        height: 200px;
        perspective: 1000px;
        margin: 10px 0;
    }
    
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.8s;
        transform-style: preserve-3d;
    }
    
    .flip-card.flipped .flip-card-inner {
        transform: rotateY(180deg);
    }
    
    .flip-card-front, .flip-card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    
    .flip-card-front {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 24px;
        font-weight: bold;
    }
    
    .flip-card-back {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        transform: rotateY(180deg);
        text-align: left;
    }
    
    .grupo-revelado {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background-color: #f0f;
        animation: confetti-fall 3s ease-out forwards;
        z-index: 9999;
    }
    
    @keyframes confetti-fall {
        0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
    </style>
    """
    
    st.markdown(flip_css, unsafe_allow_html=True)
    
    # Container para os cards
    cards_container = st.container()
    
    # Placeholders para cada card
    cards_placeholders = []
    with cards_container:
        cols = st.columns(min(3, len(grupos)))
        for i in range(len(grupos)):
            with cols[i % 3]:
                cards_placeholders.append(st.empty())
    
    # Revelar grupos um por um
    for i, grupo in enumerate(grupos):
        # Mostrar card fechado
        cards_placeholders[i].markdown(f"""
        <div class="flip-card" id="card-{i}">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <h2>?</h2>
                    <p>Grupo {i+1}</p>
                </div>
                <div class="flip-card-back">
                    <h3>Grupo {i+1}</h3>
                    <p>{len(grupo)} estudantes</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Pausa inicial
    time.sleep(1)
    
    # Revelar cada grupo com animação
    for i, grupo in enumerate(grupos):
        # Aguardar delay
        time.sleep(delay)
        
        # Criar conteúdo do card revelado
        estudantes_html = ""
        for j, estudante in enumerate(grupo[:5], 1):  # Mostrar até 5 estudantes
            estudantes_html += f"<p>{j}. {estudante.get('completo', '')}</p>"
        
        if len(grupo) > 5:
            estudantes_html += f"<p><em>... e mais {len(grupo) - 5} estudantes</em></p>"
        
        # Atualizar card com efeito de virada
        cards_placeholders[i].markdown(f"""
        <div class="flip-card flipped grupo-revelado" id="card-{i}-revealed">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <h2>?</h2>
                    <p>Grupo {i+1}</p>
                </div>
                <div class="flip-card-back">
                    <h3>Grupo {i+1}</h3>
                    <p>{len(grupo)} estudantes</p>
                    <div style="font-size: 12px; text-align: left; margin-top: 10px;">
                        {estudantes_html}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Efeito de confete ao final
    time.sleep(0.5)
    adicionar_confete()


def adicionar_confete():
    """Adiciona efeito de confete caindo."""
    confete_js = """
    <script>
    function criarConfete() {
        const confete = document.createElement('div');
        confete.className = 'confetti';
        confete.style.left = Math.random() * 100 + 'vw';
        confete.style.backgroundColor = ['#ff0', '#f0f', '#0ff', '#0f0', '#f00'][Math.floor(Math.random() * 5)];
        confete.style.animationDuration = (Math.random() * 2 + 2) + 's';
        document.body.appendChild(confete);
        
        setTimeout(() => confete.remove(), 4000);
    }
    
    // Criar múltiplos confetes
    for(let i = 0; i < 50; i++) {
        setTimeout(criarConfete, i * 50);
    }
    </script>
    """
    st.markdown(confete_js, unsafe_allow_html=True)


def animacao_progresso(etapa, total, mensagem=""):
    """
    Exibe uma barra de progresso animada.
    
    Args:
        etapa (int): Etapa atual
        total (int): Total de etapas
        mensagem (str): Mensagem opcional
    """
    progresso = etapa / total
    
    progress_html = f"""
    <style>
    .progress-container {
        width: 100%;
        background-color: #f0f0f0;
        border-radius: 10px;
        padding: 3px;
        margin: 10px 0;
    }
    
    .progress-bar {
        width: {progresso * 100}%;
        height: 20px;
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        border-radius: 7px;
        transition: width 0.5s ease-in-out;
        text-align: center;
        line-height: 20px;
        color: white;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
    
    <div class="progress-container">
        <div class="progress-bar">{int(progresso * 100)}%</div>
    </div>
    <p style="text-align: center; color: #666;">{mensagem} ({etapa}/{total})</p>
    """
    
    st.markdown(progress_html, unsafe_allow_html=True)


def animacao_contador(numero, duracao=2.0):
    """
    Exibe animação de contador crescente.
    
    Args:
        numero (int): Número final
        duracao (float): Duração da animação em segundos
    """
    placeholder = st.empty()
    
    steps = 30
    for i in range(steps + 1):
        valor_atual = int(numero * (i / steps))
        placeholder.markdown(f"""
        <div style="text-align: center; font-size: 48px; font-weight: bold; color: #4CAF50;">
            {valor_atual}
        </div>
        """, unsafe_allow_html=True)
        time.sleep(duracao / steps)
    
    # Mostrar valor final
    placeholder.markdown(f"""
    <div style="text-align: center; font-size: 48px; font-weight: bold; color: #4CAF50;">
        {numero}
    </div>
    <div style="text-align: center; color: #666;">
        estudantes carregados
    </div>
    """, unsafe_allow_html=True)


def efeito_pulso(elemento_id="info"):
    """
    Adiciona efeito de pulso a um elemento.
    
    Args:
        elemento_id (str): ID do elemento CSS
    """
    pulso_css = """
    <style>
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
    
    .pulse-effect {
        animation: pulse 2s infinite;
    }
    </style>
    """
    st.markdown(pulso_css, unsafe_allow_html=True)
