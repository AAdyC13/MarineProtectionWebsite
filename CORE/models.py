from django.db import models
from pandas import DataFrame


class cleanText(models.Model):
    """
    過濾完畢的純資訊
    """
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 自動設定建立時間

    @classmethod
    def db_update(cls, data: dict) -> bool:
        """
        寫入資訊 (如果存在則更新，不存在則創建)
        Args:
            dict: data
        Returns:
            bool: 成功則回傳True，失敗則回傳False。

        """
        try:
            cls.objects.update_or_create(
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
