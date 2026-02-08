"""
Testes para o módulo de formação de grupos.
"""

from logic.group_formation import (
    calcular_estatisticas,
    formar_grupos,
    redistribuir_solitarios_func,
)


class TestFormarGrupos:
    """Testes para a função formar_grupos."""

    def test_formar_grupos_aleatorio(self):
        """Testa formação aleatória de grupos."""
        estudantes = [
            {"matricula": "1", "nome": "Ana"},
            {"matricula": "2", "nome": "Bruno"},
            {"matricula": "3", "nome": "Carlos"},
            {"matricula": "4", "nome": "Daniela"},
        ]

        grupos = formar_grupos(estudantes, 2, "Aleatório", semente=42)

        assert len(grupos) == 2
        assert len(grupos[0]) == 2
        assert len(grupos[1]) == 2

    def test_formar_grupos_sequencial(self):
        """Testa formação sequencial de grupos."""
        estudantes = [
            {"matricula": "1", "nome": "Ana"},
            {"matricula": "2", "nome": "Bruno"},
            {"matricula": "3", "nome": "Carlos"},
            {"matricula": "4", "nome": "Daniela"},
        ]

        grupos = formar_grupos(estudantes, 2, "Sequencial")

        assert grupos[0][0]["matricula"] == "1"
        assert grupos[0][1]["matricula"] == "2"
        assert grupos[1][0]["matricula"] == "3"
        assert grupos[1][1]["matricula"] == "4"

    def test_formar_grupos_balanceado(self):
        """Testa formação balanceada de grupos."""
        estudantes = [
            {"matricula": "1", "nome": "Ana"},
            {"matricula": "2", "nome": "Bruno"},
            {"matricula": "3", "nome": "Carlos"},
            {"matricula": "4", "nome": "Daniela"},
        ]

        grupos = formar_grupos(estudantes, 2, "Balanceado")

        assert len(grupos) == 2

    def test_formar_grupos_com_sozinho(self):
        """Testa formação com redistribution de estudantes sozinhos."""
        estudantes = [
            {"matricula": "1", "nome": "Ana"},
            {"matricula": "2", "nome": "Bruno"},
            {"matricula": "3", "nome": "Carlos"},
        ]

        grupos = formar_grupos(estudantes, 2, "Sequencial", redistribuir_solitarios=True)

        # O estudante solitário deve ser redistribuído para outro grupo
        assert len(grupos) == 1
        assert len(grupos[0]) == 3

    def test_formar_grupos_vazio(self):
        """Testa formação com lista vazia."""
        grupos = formar_grupos([], 3)
        assert grupos == []


class TestCalcularEstatisticas:
    """Testes para a função calcular_estatisticas."""

    def test_calcular_estatisticas_basico(self):
        """Testa cálculo básico de estatísticas."""
        grupos = [
            [{"matricula": "1"}, {"matricula": "2"}],
            [{"matricula": "3"}, {"matricula": "4"}],
        ]

        stats = calcular_estatisticas(grupos)

        assert stats["total_grupos"] == 2
        assert stats["total_estudantes"] == 4
        assert stats["menor_grupo"] == 2
        assert stats["maior_grupo"] == 2
        assert stats["media"] == 2.0

    def test_calcular_estatisticas_vazio(self):
        """Testa cálculo com grupos vazios."""
        stats = calcular_estatisticas([])

        assert stats["total_grupos"] == 0
        assert stats["total_estudantes"] == 0


class TestRedistribuirSolitarios:
    """Testes para a função redistribuir_solitarios_func."""

    def test_redistribuir_solitarios_basico(self):
        """Testa redistribuição básica de estudantes sozinhos."""
        grupos = [
            [{"matricula": "1"}, {"matricula": "2"}],
            [{"matricula": "3"}, {"matricula": "4"}],
            [{"matricula": "5"}],  # Estudante solitário
        ]

        novos_grupos = redistribuir_solitarios_func(grupos, 2, permitir_grupos_maiores=True)

        # O estudante solitário deve ter sido redistribuído
        assert len(novos_grupos) == 2
        assert any(len(g) == 3 for g in novos_grupos)

    def test_redistribuir_sem_permitir_maior(self):
        """Testa redistribuição sem permitir grupos maiores."""
        grupos = [
            [{"matricula": "1"}, {"matricula": "2"}],
            [{"matricula": "3"}, {"matricula": "4"}],
            [{"matricula": "5"}],  # Estudante solitário
        ]

        novos_grupos = redistribuir_solitarios_func(grupos, 2, permitir_grupos_maiores=False)

        # O estudante solitário deve formar novo grupo
        assert len(novos_grupos) == 3
