"""
Módulo de persistência de dados.
Implementa persistência dupla: localStorage (via JavaScript) e JSON backup.
"""

import json
from datetime import datetime
from pathlib import Path

# Caminho para o diretório de dados
DATA_DIR = Path(__file__).parent.parent / "data"
HISTORY_FILE = DATA_DIR / "history.json"
CONFIG_FILE = DATA_DIR / "config.json"
BACKUP_DIR = DATA_DIR / "backups"


def ensure_data_dir():
    """Garante que o diretório de dados existe."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def save_history(historico):
    """
    Salva o histórico de grupos em arquivo JSON.

    Args:
        historico (list): Lista de grupos formados

    Returns:
        bool: True se salvou com sucesso
    """
    try:
        ensure_data_dir()

        # Adicionar metadados
        data_to_save = {
            "last_updated": datetime.now().isoformat(),
            "version": "2.0",
            "count": len(historico),
            "historico": historico,
        }

        # Salvar no arquivo principal
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)

        # Também criar backup
        backup_filename = f"history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        backup_path = BACKUP_DIR / backup_filename
        with open(backup_path, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)

        # Limitar número de backups (manter últimos 10)
        limit_backups(10)

        return True
    except Exception as e:
        print(f"Erro ao salvar histórico: {e}")
        return False


def load_history():
    """
    Carrega o histórico de grupos do arquivo JSON.

    Returns:
        list: Lista de grupos ou lista vazia se não existir
    """
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("historico", [])
        return []
    except Exception as e:
        print(f"Erro ao carregar histórico: {e}")
        return []


def save_config(config):
    """
    Salva as configurações da aplicação.

    Args:
        config (dict): Dicionário de configurações

    Returns:
        bool: True se salvou com sucesso
    """
    try:
        ensure_data_dir()

        config_data = {
            "last_updated": datetime.now().isoformat(),
            "version": "2.0",
            "config": config,
        }

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")
        return False


def load_config():
    """
    Carrega as configurações da aplicação.

    Returns:
        dict: Configurações ou dicionário vazio
    """
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("config", {})
        return {}
    except Exception as e:
        print(f"Erro ao carregar configurações: {e}")
        return {}


def limit_backups(max_backups=10):
    """
    Limita o número de arquivos de backup.

    Args:
        max_backups (int): Número máximo de backups a manter
    """
    try:
        if BACKUP_DIR.exists():
            backups = sorted(
                BACKUP_DIR.glob("history_*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True,
            )

            for old_backup in backups[max_backups:]:
                old_backup.unlink()
    except Exception as e:
        print(f"Erro ao limitar backups: {e}")


def export_all_data(filename=None):
    """
    Exporta todos os dados da aplicação para um arquivo JSON.

    Args:
        filename (str, optional): Nome do arquivo de exportação

    Returns:
        str: Caminho do arquivo exportado ou None
    """
    try:
        ensure_data_dir()

        if filename is None:
            filename = f"formadevs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        export_path = DATA_DIR / filename

        data = {
            "export_date": datetime.now().isoformat(),
            "version": "2.0",
            "historico": load_history(),
            "config": load_config(),
        }

        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return str(export_path)
    except Exception as e:
        print(f"Erro ao exportar dados: {e}")
        return None


def import_all_data(file_path):
    """
    Importa dados de um arquivo JSON.

    Args:
        file_path (str): Caminho do arquivo a importar

    Returns:
        tuple: (bool, str) - (sucesso, mensagem)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Salvar histórico
        if "historico" in data:
            save_history(data["historico"])

        # Salvar configurações
        if "config" in data:
            save_config(data["config"])

        return True, "Dados importados com sucesso!"
    except Exception as e:
        return False, f"Erro ao importar dados: {e}"


def clear_history():
    """
    Limpa o histórico de grupos.

    Returns:
        bool: True se limpou com sucesso
    """
    try:
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
        return True
    except Exception as e:
        print(f"Erro ao limpar histórico: {e}")
        return False


def reset_all():
    """
    Reseta todos os dados da aplicação.

    Returns:
        bool: True se resetou com sucesso
    """
    try:
        clear_history()
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
        return True
    except Exception as e:
        print(f"Erro ao resetar dados: {e}")
        return False


# Código JavaScript para localStorage (para ser usado no Streamlit)
LOCALSTORAGE_JS_SAVE = """
<script>
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (e) {
        console.error('Erro ao salvar no localStorage:', e);
        return false;
    }
}
</script>
"""

LOCALSTORAGE_JS_LOAD = """
<script>
function loadFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (e) {
        console.error('Erro ao carregar do localStorage:', e);
        return null;
    }
}
</script>
"""

LOCALSTORAGE_JS_CLEAR = """
<script>
function clearLocalStorage(key) {
    try {
        localStorage.removeItem(key);
        return true;
    } catch (e) {
        console.error('Erro ao limpar localStorage:', e);
        return false;
    }
}
</script>
"""
