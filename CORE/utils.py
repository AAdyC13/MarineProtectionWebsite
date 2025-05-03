
from .models import system_config as sys
# from .models import cleanText as ct


def reset_loaded_corpus() -> bool:
    """初始化 loaded_corpus
    """

    data = {
        "loaded_corpus": []
    }

    return sys.sysdb_update("loaded_corpus", data)


def add_loaded_corpus(name: str) -> bool:
    """修改 loaded_corpus
    """
    data = get_loaded_corpus()
    data["loaded_corpus"].append(name)

    return sys.sysdb_update("loaded_corpus", data)


def del_loaded_corpus(name: str) -> bool:
    """修改 loaded_corpus
    """
    data = get_loaded_corpus()
    data["loaded_corpus"].remove(name)

    return sys.sysdb_update("loaded_corpus", data)


def get_loaded_corpus() -> dict:
    """回傳 loaded_corpus
    """
    return sys.sysdb_get("loaded_corpus")
