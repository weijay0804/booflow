'''
Author: weijay
Date: 2022-12-15 23:06:11
LastEditors: Shawn
LastEditTime: 2022-12-20 21:39:11
FilePath: /booflow/sample.py
Description: booflow 基本架構測試
'''

from typing import List
import subprocess


class Cron:
    ''' 排程物件 '''

    def __init__(self, config: dict):

        self.cmd = config['cmd'].split()

        config.pop('cmd')

        self.config = config


class CronRunner:
    ''' 啟動排程 '''

    def __init__(self) -> None:

        self.tasks: List[Cron] = []

    def add_cron(self, cron: Cron):

        self.tasks.append(cron)

    def run(self):

        task_info = []

        for task in self.tasks:

            try:
                r = subprocess.run(
                    task.cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    **task.config
                )

                if r.stderr:
                    task_info.append("error")

                else:
                    task_info.append('success')

            except subprocess.TimeoutExpired:
                task_info.append("error")

        return task_info


class BooFlow:
    def __init__(self, tasks) -> None:

        self.cron_runner = CronRunner()

        for task in tasks:
            self.cron_runner.add_cron(Cron(task))

    def run(self):
        r = self.cron_runner.run()

        return r


from typing import List, Dict, Tuple, Optional


class TaskManager:
    def __init__(self, tasks: List[Dict], orders: List[Tuple]) -> None:
        pass

    def next(self) -> Optional[str]:
        """提供下一個任務的名稱，如果當前沒有任務則回傳 None

        Returns:
            str: _description_
        """
        pass

    def call(self, task_name: str, status: bool) -> bool:
        """回傳任務名稱以及完成狀態

        Args:
            task_name (str): _description_
            status (bool): _description_
        """
        pass

    def progress():
        pass


configs = {
    "database_type": "mysql",
    "connection_info": {"host": "", "password": "",},
}

tasks = [
    {"task_name": "task_1", 'command': "python3 test1.py"},
    {"task_name": "task_2", 'command': "python3 test2.py"},
    {"task_name": "task_3", 'command': "python3 test2.py"},
    {"task_name": "task_4", 'command': "python3 test3.py", "timeout": 3.0, "retry": 5},
    {"task_name": "task_5", 'command': "python3 test3.py", "timeout": 3.0, "retry": 5},
]

orders = [
    ("task_1", "task_2"),
    ("task_2", "task_3"),
    ("task_4"),
    ("task_2", "task_5"),
]

booflow = BooFlow(tasks=tasks, orders=orders, project_name="test", **configs)
r = booflow.run()

assert r == ['success', 'error', 'error']
