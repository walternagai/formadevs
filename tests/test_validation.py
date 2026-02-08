"""
Testes para o módulo de validação.
"""

from logic.validation import (
    processar_entrada_com_validacao,
    validar_duplicatas,
    validar_formato_entrada,
)


class TestValidarFormatoEntrada:
    """Testes para a função validar_formato_entrada."""

    def test_formato_com_virgula(self):
        """Testa formato válido com vírgula."""
        linha = "123456, João Silva"
        valido, dados = validar_formato_entrada(linha)

        assert valido is True
        assert dados["matricula"] == "123456"
        assert dados["nome"] == "João Silva"

    def test_formato_sem_virgula(self):
        """Testa formato válido sem vírgula."""
        linha = "123456 João Silva"
        valido, dados = validar_formato_entrada(linha)

        assert valido is True
        assert dados["matricula"] == "123456"
        assert dados["nome"] == "João Silva"

    def test_linha_vazia(self):
        """Testa linha vazia."""
        linha = ""
        valido, dados = validar_formato_entrada(linha)

        assert valido is True
        assert dados is None

    def test_formato_invalido(self):
        """Testa formato inválido."""
        linha = "linha invalida sem formato correto"
        valido, erro = validar_formato_entrada(linha)

        assert valido is False
        assert erro == "Formato não reconhecido. Use 'Matrícula, Nome' ou 'Matrícula Nome'"


class TestValidarDuplicatas:
    """Testes para a função validar_duplicatas."""

    def test_sem_duplicatas(self):
        """Testa lista sem duplicatas."""
        estudantes = [
            {"matricula": "1", "nome": "Ana"},
            {"matricula": "2", "nome": "Bruno"},
        ]

        duplicatas = validar_duplicatas(estudantes)

        assert duplicatas == {}

    def test_com_duplicatas(self):
        """Testa lista com duplicatas."""
        estudantes = [
            {"matricula": "1", "nome": "Ana"},
            {"matricula": "2", "nome": "Bruno"},
            {"matricula": "1", "nome": "Ana Nova"},
        ]

        duplicatas = validar_duplicatas(estudantes)

        assert "1" in duplicatas
        assert duplicatas["1"]["count"] == 2


class TestProcessarEntradaComValidacao:
    """Testes para a função processar_entrada_com_validacao."""

    def test_entrada_valida(self):
        """Testa entrada totalmente válida."""
        entrada = "123, João\n456, Maria"
        resultado = processar_entrada_com_validacao(entrada)

        assert resultado["valido"] is True
        assert resultado["total"] == 2
        assert resultado["erros"] == []
        assert resultado["duplicatas"] == {}

    def test_entrada_com_erro(self):
        """Testa entrada com erros."""
        entrada = "123, João\nlinha invalida"
        resultado = processar_entrada_com_validacao(entrada)

        assert resultado["valido"] is False
        assert len(resultado["erros"]) == 1
