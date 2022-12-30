"""
Author: weijay
Date: 2022-12-30 00:38:12
LastEditors: weijay
LastEditTime: 2022-12-30 00:38:13
Description: 定義一些 interface
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict


class TaskManagerInterface(ABC):
    """Task Manager Interface"""

    @abstractmethod
    def is_empty(self) -> bool:
        """是否還有任務要執行

        Returns:
            bool: 如果有則回傳 True 反之 False
        """

        pass

    @abstractmethod
    def next(self) -> Optional[str]:
        """提供下一個任務的名稱，如果當前沒有任務則回傳 None

        Returns:
            Optional[str]: 對應至 config 中的 task_name
        """

        pass

    @abstractmethod
    def call(self, task_name: str, status: bool) -> bool:
        """回傳任務名稱以及完成狀態

        Args:
            task_name (str): 對應至 config 中的 task_name
            status (bool): 執行成功是 True 反之 False

        Returns:
            bool: 函示成功則回傳 True 反之 False
        """

        pass

    @abstractmethod
    def get_result(self) -> Dict[str, list]:
        """取得成功執行和執行失敗的任務

        Returns:
            Dict[str, list]: {"success" : ["task1", "task2"], "fail" : ["task3"]}
        """

        pass
