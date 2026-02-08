"""
Testes para o módulo de exportação.
"""

from utils.exporters import gerar_csv_grupos, gerar_excel_grupos


class TestGerarCsvGrupos:
    """Testes para a função gerar_csv_grupos."""

    def test_gerar_csv_basico(self):
        """Testa geração básica de CSV."""
        grupos = [
            [{"matricula": "1", "nome": "Ana"}, {"matricula": "2", "nome": "Bruno"}],
        ]

        csv_data, filename = gerar_csv_grupos(grupos)

        assert isinstance(csv_data, bytes)
        assert "Grupo" in csv_data.decode("utf-8")
        assert "Ana" in csv_data.decode("utf-8")
        assert filename.endswith(".csv")

    def test_gerar_csv_vazio(self):
        """Testa geração de CSV com grupos vazios."""
        csv_data, filename = gerar_csv_grupos([])

        assert isinstance(csv_data, bytes)
        assert filename.endswith(".csv")


class TestGerarExcelGrupos:
    """Testes para a função gerar_excel_grupos."""

    def test_gerar_excel_basico(self):
        """Testa geração básica de Excel."""
        grupos = [
            [{"matricula": "1", "nome": "Ana"}],
        ]

        excel_data, filename = gerar_excel_grupos(grupos)

        assert isinstance(excel_data, bytes)
        assert filename.endswith(".xlsx")

    def test_gerar_excel_vazio(self):
        """Testa geração de Excel com grupos vazios."""
        excel_data, filename = gerar_excel_grupos([])

        assert isinstance(excel_data, bytes)
        assert filename.endswith(".xlsx")
