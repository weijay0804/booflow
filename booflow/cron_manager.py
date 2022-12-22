"""
Author: weijay
Date: 2022-12-21 23:05:00
LastEditors: weijay
LastEditTime: 2022-12-21 23:05:05
Description: 主要放管理 cron 任務的模組
"""

from typing import List, Dict


class Cron:
    """針對每一個 command 的類別"""

    def __init__(self, config: dict) -> None:
        """建立 Cron 實例

        Args:
            config (dict): 排程設定資訊
        """

        self.name = config.get("task_name")
        self.cmd = self.__parse_cmd(config.get("command"))
        self.timeout = config.get("timeout")
        self.retry = config.get("retry") or 3

    def __repr__(self) -> str:

        return f"Cron: {self.__format__} , Name: {self.name}, Cmd: {self.cmd}"

    def __parse_cmd(self, cmd: str) -> list:
        """將指令字串解析成 list

        Args:
            cmd (str): 指令字串，例如 "python3 main.py"

        Returns:
            list: 回傳解析後的指令 => ["python3", "main.py"]
        """

        return cmd.split()

    def run(self) -> bool:
        """執行指令

        Returns:
            bool: 如果成功，回傳 True 反之 False
        """

        # TODO 執行指令
        print(f"{self.name} is running")


class CronManager:
    """管理排程"""

    def __init__(self, tasks: List[dict], order: List[tuple]) -> None:
        """建立 CronManager 實例

        Args:
            tasks (List[dict]): 排程任務清單
            order (List[tuple]): 排程之間的順序關係
        """

        pass

    def generate_cron_dict(self, tasks: List[dict]) -> Dict[str, Cron]:
        """建立 task_name 與 Cron 物件之間的映射表

        Args:
            tasks (List[dict]): 排程任務清單

        Returns:
            List[dict]: {"task_name1" : "Cron1", "task_name2" : "Cron2", ....}
        """

        return {i["task_name"]: Cron(i) for i in tasks}
