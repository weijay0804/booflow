"""
Author: weijay
Date: 2023-01-06 00:34:59
LastEditors: weijay
LastEditTime: 2023-01-06 00:35:00
Description: booflow 主程式
"""

from .cron_manager import CronManager
from .interface import TaskManagerInterface
from .data_util import MyTxt

from typing import List, Dict, Union
from queue import Queue

import os


class FakeTaskManager(TaskManagerInterface):
    def __init__(self, order: List[str]):

        self.order = self.__init_task_queue(order)
        self.fall_tasks = list()
        self.success_tasks = list()

    def __init_task_queue(self, order: List[str]):

        q = Queue()

        for s in order:
            q.put(s)

        return q

    def is_empty(self):

        return self.order.empty()

    def next(self):

        return self.order.get()

    def call(self, task_name: str, status: bool):

        if status:
            self.success_tasks.append(task_name)

        else:
            self.fall_tasks.append(task_name)

    def get_result(self) -> Dict[str, list]:

        return {"success": self.success_tasks, "fail": self.fall_tasks}


class BooFlow:
    def __init__(self, tasks: List[Dict], order: list, config: dict):

        data_manager = BooFlow._init_data_manager(config)
        task_manager = FakeTaskManager(order)

        self.cron_manager = CronManager(tasks, task_manager, data_manager)

    @staticmethod
    def get_root_path() -> str:
        """取得專案根目錄

        Returns:
            str: 專案根目錄 (絕對路徑)
        """

        return os.path.abspath(os.path.dirname(__name__))

    @staticmethod
    def _init_data_manager(config: dict) -> MyTxt:
        """初始化 data manager 物件

        Args:
            config (dict): booflow 設定資訊

        Returns:
            MyTxt: _description_
        """

        store_type = config.get("data_store_type", "text")
        path = config.get("data_path", BooFlow.get_root_path())
        project_name = config.get("project_name")

        if not project_name:
            raise RuntimeError("config error, lost project_name value.")

        if store_type == "text":
            p = os.path.join(path, f"{project_name}.txt")
            return MyTxt(p)

    def run(self):
        """啟動排程"""

        self.cron_manager.run()
