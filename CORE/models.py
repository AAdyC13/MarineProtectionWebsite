from django.db import models
from pandas import DataFrame


class cleanText(models.Model):
    """
    過濾完畢的純資訊
    """
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 自動設定建立時間

    @classmethod
    def db_update(cls, data: dict) -> bool:
        """
        寫入資訊 (如果存在則更新，不存在則創建)
        """
        try:
            cls.objects.update_or_create(
                url=data.get("url"),        # ← 用 URL 當作查詢條件
                defaults=data
            )
            return True
        except Exception as e:
            print(f"❗core/models/db_update 發生錯誤: {e}")
            return False

    @classmethod
    def db_delete(cls, id: int) -> bool:
        """
        刪除資訊
        Args:
            int: id
        Returns:
            bool: 成功則回傳True，失敗則回傳False。

        """
        try:
            data = cls.objects.get(
                id=id)
            data.delete()
            return True
        except cls.DoesNotExist as e:
            print(f"❗core/models/db_delete 發生錯誤: {e}")
            return False


class system_config(models.Model):
    """系統資料\n
    """
    sysdb_id = models.IntegerField(primary_key=True)
    sysdb_name: str = models.CharField(max_length=50, blank=True, null=True)
    sysdb_data = models.JSONField(default=dict)

    def __str__(self) -> str:

        return (
            f"{self.sysdb_id}.{self.sysdb_name}：{self.sysdb_data}"
        )

    def get_data(self) -> dict:

        return self.sysdb_data

    @classmethod
    def sysdb_get(cls, sysdb_name: str) -> dict:
        """回傳指定的sysdb_data

        Returns:
            dict: 指定的sysdb_data
        """
        try:
            return cls.objects.get(sysdb_name=sysdb_name).get_data()
        except cls.DoesNotExist:
            print(f"❗core/models/sysdb_get 找不到資料，回傳空字典")
            return {}
        except Exception as e:
            print(f"❗core/models/sysdb_get 發生錯誤，回傳空字典: {e}")
        return {}

    @classmethod
    def sysdb_update(cls, sysdb_name: str, sysdb_data: dict) -> bool:
        """
        設定指定sysdb_name的sysdb_data

        Returns:
            bool: 是否成功
        """
        try:
            cls.objects.update_or_create(
                sysdb_name=sysdb_name,
                defaults={"sysdb_data": sysdb_data}
            )
            return True
        except Exception as e:
            print(f"❗core/models/sysdb_update 發生錯誤: {e}")
            return False
