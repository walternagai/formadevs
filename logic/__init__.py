"""
Pacote de lógica de negócio do FormaDevs.
"""

from logic.data_processing import (
    criar_dataframe_grupos,
    filtrar_estudantes_por_grupo,
    preparar_dados_exportacao,
    processar_csv_para_estudantes,
)
from logic.group_formation import (
    calcular_estatisticas,
    formar_grupos,
    sortear_grupo_ao_vivo,
)
from logic.validation import (
    extrair_preview_dados,
    processar_entrada_com_validacao,
    validar_csv,
    validar_duplicatas,
    validar_formato_entrada,
)

__all__ = [
    # group_formation
    "formar_grupos",
    "calcular_estatisticas",
    "sortear_grupo_ao_vivo",
    # validation
    "validar_formato_entrada",
    "validar_duplicatas",
    "validar_csv",
    "processar_entrada_com_validacao",
    "extrair_preview_dados",
    # data_processing
    "processar_csv_para_estudantes",
    "preparar_dados_exportacao",
    "criar_dataframe_grupos",
    "filtrar_estudantes_por_grupo",
]
