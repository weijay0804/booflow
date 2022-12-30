"""
Author: weijay
Date: 2022-12-21 23:05:00
LastEditors: weijay
LastEditTime: 2022-12-21 23:05:05
Description: 主要放管理 cron 任務的模組
"""

import subprocess
from typing import List, Dict, Tuple

from .interface import TaskManagerInterface


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

        # FIXME 如果 retry 次數設為 0 時，也會自動設為 3
        self.retry_time = config.get("retry") or 3

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

    def run(self) -> Tuple[bool, str, str]:
        """執行指令
            會分成以下幾種狀況

            1. 執行成功，則回傳 (True, None, stdout)
            2. 程式錯誤，則回傳 (False, "program error", stderr)
            3. 執行逾時，則回傳 (False, "time out", None)
            4. 未知錯誤，則回傳 (False, "unknow error", error)

        Returns:
            Tuple[bool, str]: 詳見說明
        """

        try:
            r = subprocess.run(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout,
            )

            if r.stderr:

                return (
                    False,
                    "program error",
                    r.stderr.decode("utf8").replace("\n", ""),
                )

            else:

                return (True, None, r.stdout.decode("utf8").replace("\n", ""))

        except subprocess.TimeoutExpired:

            return (False, "time out", None)

        except Exception as e:

            return (False, "unknow error", str(e))

    def retry(self) -> Tuple[bool, str, str]:
        """重新執行一次 run 函示，並將 retry_time 減 1

        Returns:
            Tuple[bool, str, str]: run 函示的回傳值
        """

        if self.retry_time == 0:
            return

        self.retry_time -= 1

        return self.run()


class CronManager:
    """管理排程"""

    def __init__(self, tasks: List[dict], task_manager: TaskManagerInterface) -> None:
        """建立 CronManager 實例

        Args:
            tasks (List[dict]): 排程任務清單
            task_manager (TaskManagerInterface): implement TaskManagerInterface 的實例
        """

        self.task_manager = task_manager
        self.task_map = self.generate_cron_dict(tasks)

    def generate_cron_dict(self, tasks: List[dict]) -> Dict[str, Cron]:
        """建立 task_name 與 Cron 物件之間的映射表

        Args:
            tasks (List[dict]): 排程任務清單

        Returns:
            List[dict]: {"task_name1" : "Cron1", "task_name2" : "Cron2", ....}
        """

        return {i["task_name"]: Cron(i) for i in tasks}

    def run(self) -> Dict[str, list]:
        """開始執行排程

        Returns:
            Dict[str, list]: 執行成功和失敗的任務
        """

        while not self.task_manager.is_empty():

            task_name = self.task_manager.next()

            result = self.task_map[task_name].run()

            if not result[0]:

                while self.task_map[task_name].retry_time != 0:

                    result = self.task_map[task_name].retry()

                    print("Retry.....")

            self.task_manager.call(task_name, result[0])

        return self.task_manager.get_result()
