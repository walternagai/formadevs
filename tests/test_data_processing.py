"""
Testes para o módulo de processamento de dados.
"""

import pandas as pd

from logic.data_processing import (
    criar_dataframe_grupos,
    filtrar_estudantes_por_grupo,
    preparar_dados_exportacao,
    processar_csv_para_estudantes,
)


class TestProcessarCsvParaEstudantes:
    """Testes para a função processar_csv_para_estudantes."""

    def test_processar_csv_basico(self):
        """Testa processamento básico de CSV."""
        df = pd.DataFrame({"matricula": ["123", "456"], "nome": ["Ana Silva", "Bruno Santos"]})

        estudantes = processar_csv_para_estudantes(df, "matricula", "nome")

        assert len(estudantes) == 2
        assert estudantes[0]["matricula"] == "123"
        assert estudantes[0]["nome"] == "Ana Silva"


class TestPrepararDadosExportacao:
    """Testes para a função preparar_dados_exportacao."""

    def test_preparar_dados_basico(self):
        """Testa preparação básica de dados para exportação."""
        grupos = [
            [{"matricula": "1", "nome": "Ana"}, {"matricula": "2", "nome": "Bruno"}],
        ]

        dados = preparar_dados_exportacao(grupos)

        assert len(dados) == 2
        assert dados[0]["Grupo"] == 1
        assert dados[0]["Matrícula"] == "1"
        assert dados[0]["Nome"] == "Ana"


class TestCriarDataframeGrupos:
    """Testes para a função criar_dataframe_grupos."""

    def test_criar_dataframe_basico(self):
        """Testa criação básica de DataFrame."""
        grupos = [
            [
                {"matricula": "1", "nome": "Ana"},
            ],
        ]

        df = criar_dataframe_grupos(grupos)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "Grupo" in df.columns
        assert "Matrícula" in df.columns
        assert "Nome" in df.columns


class TestFiltrarEstudantesPorGrupo:
    """Testes para a função filtrar_estudantes_por_grupo."""

    def test_filtrar_grupo_valido(self):
        """Testa filtragem de grupo válido."""
        grupos = [
            [{"matricula": "1", "nome": "Ana"}],
            [{"matricula": "2", "nome": "Bruno"}],
        ]

        estudantes = filtrar_estudantes_por_grupo(grupos, 1)

        assert len(estudantes) == 1
        assert estudantes[0]["matricula"] == "1"

    def test_filtrar_grupo_invalido(self):
        """Testa filtragem de grupo inválido."""
        grupos = [
            [{"matricula": "1", "nome": "Ana"}],
        ]

        estudantes = filtrar_estudantes_por_grupo(grupos, 5)

        assert estudantes == []
