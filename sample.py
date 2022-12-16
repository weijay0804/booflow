'''
Author: weijay
Date: 2022-12-15 23:06:11
LastEditors: weijay
LastEditTime: 2022-12-15 23:37:38
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
                r = subprocess.run(task.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **task.config)

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

tasks = [
    {"cmd" : "python3 test1.py"},
    {"cmd" : "python3 test2.py"},
    {"cmd" : "python3 test3.py", "timeout" : 3.0}
]

boo_flow = BooFlow(tasks)
r = boo_flow.run()

assert r == ['success', 'error', 'error']
