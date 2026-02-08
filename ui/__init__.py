"""
Pacote de interface do usuário do FormaDevs.
"""

from ui.animations import (
    adicionar_confete,
    animacao_contador,
    animacao_progresso,
    animacao_sorteio_flip_cards,
    efeito_pulso,
)
from ui.components import (
    alerta_aviso,
    alerta_erro,
    alerta_info,
    alerta_sucesso,
    badge,
    botao_acao,
    card_estatistica,
    card_estudante,
    card_grupo,
    divisoria,
)
from ui.group_display import exibir_grupos
from ui.history_view import exibir_historico
from ui.input_forms import (
    carregar_grupos_salvos,
    entrada_manual_com_preview,
    importar_csv_com_mapeamento,
)
from ui.settings_view import exibir_configuracoes

__all__ = [
    # input_forms
    "entrada_manual_com_preview",
    "importar_csv_com_mapeamento",
    "carregar_grupos_salvos",
    # group_display
    "exibir_grupos",
    # history_view
    "exibir_historico",
    # settings_view
    "exibir_configuracoes",
    # components
    "card_estudante",
    "card_grupo",
    "card_estatistica",
    "alerta_info",
    "alerta_sucesso",
    "alerta_aviso",
    "alerta_erro",
    "botao_acao",
    "badge",
    "divisoria",
    # animations
    "animacao_sorteio_flip_cards",
    "adicionar_confete",
    "animacao_progresso",
    "animacao_contador",
    "efeito_pulso",
]
