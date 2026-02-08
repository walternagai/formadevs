"""
Testes para o módulo de utilitários.
"""

from utils.helpers import (
    formatar_data,
    formato_display,
    sanitize_filename,
    truncar_texto,
)


class TestFormatoDisplay:
    """Testes para a função formato_display."""

    def test_formato_completo(self):
        """Testa formato 'Matrícula e Nome'."""
        assert formato_display("Matrícula e Nome") == "completo"

    def test_formato_apenas_nome(self):
        """Testa formato 'Apenas Nome'."""
        assert formato_display("Apenas Nome") == "nome"

    def test_formato_apenas_matricula(self):
        """Testa formato 'Apenas Matrícula'."""
        assert formato_display("Apenas Matrícula") == "matricula"


class TestTruncarTexto:
    """Testes para a função truncar_texto."""

    def test_texto_curto(self):
        """Testa texto que não precisa ser truncado."""
        assert truncar_texto("Olá", 10) == "Olá"

    def test_texto_longo(self):
        """Testa texto que precisa ser truncado."""
        texto = "Este é um texto muito longo"
        resultado = truncar_texto(texto, 10)
        assert len(resultado) <= 10
        assert resultado.endswith("...")


class TestFormatarData:
    """Testes para a função formatar_data."""

    def test_formatar_data_basico(self):
        """Testa formatação básica de data."""
        data = "01/01/2023 10:30"
        resultado = formatar_data(data)
        assert resultado == "01/01/2023 10:30"

    def test_data_invalida(self):
        """Testa formatação com data inválida."""
        assert formatar_data("data invalida") == "data invalida"


class TestSanitizeFilename:
    """Testes para a função sanitize_filename."""

    def test_filename_valido(self):
        """Testa filename já válido."""
        assert sanitize_filename("arquivo.txt") == "arquivo.txt"

    def test_filename_com_caracteres_invalidos(self):
        """Testa filename com caracteres inválidos."""
        resultado = sanitize_filename("arquivo<test>.txt")
        assert "<" not in resultado
        assert ">" not in resultado

    def test_filename_muito_longo(self):
        """Testa filename muito longo."""
        LONG_NAME = "a" * 300 + ".txt"
        resultado = sanitize_filename(LONG_NAME)
        assert len(resultado) <= 200
