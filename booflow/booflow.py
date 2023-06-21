"""
Author: weijay
Date: 2023-01-06 00:34:59
LastEditors: weijay
LastEditTime: 2023-01-06 00:35:00
Description: booflow 主程式
"""

import os
import subprocess
from collections import deque, defaultdict
from typing import List, Dict, Tuple


class BooFlow:
    def __init__(self, tasks: List[Dict], order: list, config: dict = None):
        task_manager = TaskManager(order)

        self.cron_manager = CronManager(tasks, task_manager)

    @staticmethod
    def get_root_path() -> str:
        """取得專案根目錄

        Returns:
            str: 專案根目錄 (絕對路徑)
        """

        return os.path.abspath(os.path.dirname(__name__))

    def run(self):
        """啟動排程"""

        self.cron_manager.run()


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

        if config.get("retry") is None:
            self.retry_time = 3
        else:
            self.retry_time = config.get("retry")

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


class TaskManager:
    """任務管理"""

    def __init__(self, order):
        task_graph, indegree = self.transform_tasks_to_graph(order)
        self.order_list = self.extract_graph_task_order(task_graph, indegree)

    def transform_tasks_to_graph(self, tasks: List[tuple]) -> Tuple[defaultdict, defaultdict]:
        graph = defaultdict(set)
        indegree = defaultdict(int)
        for start, end in tasks:
            if end not in graph[start]:
                graph[start].add(end)
                indegree[start]
                indegree[end] += 1

        return graph, indegree

    def extract_graph_task_order(self, graph: defaultdict, indegree: defaultdict) -> deque:
        task_order = deque()
        queue = deque()
        for idx, item in indegree.items():
            if item == 0:
                queue.append(idx)

        while queue:
            current_task = queue.popleft()
            task_order.append(current_task)
            for next_task in graph[current_task]:
                indegree[next_task] -= 1
                if indegree[next_task] == 0:
                    queue.append(next_task)

        return task_order

    def get_next(self):
        return self.order_list.popleft()

    def is_empty(self):
        return len(self.order_list) == 0

    def call(self, task_name, status):
        pass


class CronManager:
    """管理排程"""

    def __init__(
        self,
        tasks: List[dict],
        task_manager: "TaskManager",
    ) -> None:
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
            task_name = self.task_manager.get_next()

            result = self.task_map[task_name].run()

            if not result[0]:
                while self.task_map[task_name].retry_time != 0:
                    result = self.task_map[task_name].retry()

            self.task_manager.call(task_name, result[0])

        return "OK"
