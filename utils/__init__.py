"""
Pacote de utilitários do FormaDevs.
"""

from utils.exporters import (
    gerar_csv_grupos,
    gerar_excel_grupos,
    gerar_lista_simples,
    gerar_txt_grupos,
)
from utils.helpers import (
    calcular_duracao_formatada,
    contar_estudantes_unicos,
    formatar_data,
    formatar_numero_grupo,
    formato_display,
    sanitize_filename,
    truncar_texto,
)
from utils.persistence import (
    clear_history,
    export_all_data,
    import_all_data,
    load_config,
    load_history,
    reset_all,
    save_config,
    save_history,
)
from utils.qr_generator import (
    gerar_qr_batch,
    gerar_qr_code_grupo,
    gerar_qr_code_simples,
    gerar_qr_code_todos_grupos,
    verificar_dados_qr,
)

__all__ = [
    # persistence
    "save_history",
    "load_history",
    "save_config",
    "load_config",
    "export_all_data",
    "import_all_data",
    "clear_history",
    "reset_all",
    # exporters
    "gerar_csv_grupos",
    "gerar_excel_grupos",
    "gerar_txt_grupos",
    "gerar_lista_simples",
    # qr_generator
    "gerar_qr_code_grupo",
    "gerar_qr_code_todos_grupos",
    "gerar_qr_code_simples",
    "gerar_qr_batch",
    "verificar_dados_qr",
    # helpers
    "formato_display",
    "formatar_data",
    "sanitize_filename",
    "contar_estudantes_unicos",
    "formatar_numero_grupo",
    "calcular_duracao_formatada",
    "truncar_texto",
]
