
from .models import system_config as sys
# from .models import cleanText as ct


def reset_loaded_corpus() -> bool:
    """初始化 loaded_corpus
    """

    data = {
    }

    return sys.sysdb_update("loaded_corpus", data)


def add_loaded_corpus(name: str, seed: list) -> bool:
    """修改 loaded_corpus
    """
    data = get_loaded_corpus()
    data[name] = seed

    return sys.sysdb_update("loaded_corpus", data)


def del_loaded_corpus(name: str) -> bool:
    """修改 loaded_corpus
    """
    data = get_loaded_corpus()
    if name in data:
        del data[name]
        print(f"⚠️ 已刪除 {name} 語料庫的讀取紀錄(其內容沒有被刪除)")
    else:
        print(f"⚠️ 未刪除 {name} ，紀錄中不存在")

    return sys.sysdb_update("loaded_corpus", data)


def get_loaded_corpus() -> dict:
    """回傳 loaded_corpus
    """
    return sys.sysdb_get("loaded_corpus")
