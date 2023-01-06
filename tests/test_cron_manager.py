"""
Author: weijay
Date: 2022-12-22 13:50:37
LastEditors: weijay
LastEditTime: 2022-12-22 13:50:38
Description: 針對 cron_manager 模組的測試
"""

from booflow.cron_manager import Cron, CronManager


def test_parse_cmd():

    test_config = {"task_name": "test1", "command": "python3 main.py"}

    c = Cron(test_config)

    assert c.cmd == ["python3", "main.py"]


def test_cron_run():

    test_config = {"task_name": "test1", "command": "python3 ./tests/case1.py"}

    cron = Cron(test_config)

    cron_r = cron.run()

    assert cron_r == (True, None, "Hello from case1")


def test_cron_run_with_program_error():

    test_config = {"task_name": "test1", "command": "python3 ./tests/case2.py"}

    cron = Cron(test_config)

    cron_r = cron.run()

    assert cron_r[0] == False
    assert cron_r[1] == "program error"


def test_cron_run_with_timeout():

    test_config = {
        "task_name": "test1",
        "command": "python3 ./tests/case3.py",
        "timeout": 2,
    }

    cron = Cron(test_config)

    cron_r = cron.run()

    assert cron_r[0] == False
    assert cron_r[1] == "time out"


def test_cron_retry():

    test_config = {
        "task_name": "test1",
        "command": "python3 ./tests/case2.py",
        "retry": 2,
    }

    cron = Cron(test_config)

    result = []

    r = cron.run()

    result.append(r)

    if not r[0]:

        while cron.retry_time != 0:
            r = cron.retry()

            result.append(r)

    assert len(result) == 3
    assert not all(i[0] for i in result)

    for d in result:

        assert d[1] == "program error"


def test_cron_retry_time_zero():

    test_config = {
        "task_name": "test1",
        "command": "python3 ./tests/case2.py",
        "retry": 0,
    }

    cron = Cron(test_config)

    result = []

    r = cron.run()

    result.append(r)

    if not r[0]:

        while cron.retry_time != 0:
            r = cron.retry()

            result.append(r)

    assert len(result) == 1
    assert not all(i[0] for i in result)

    for d in result:
        assert d[1] == "program error"


def test_cron_manager_generate_map():

    tasks = [
        {"task_name": "test1", "command": "python3 ./tests/case1.py"},
        {"task_name": "test2", "command": "python3 ./tests/case2.py"},
    ]

    data_manager = FakeDataManager()

    cron_manager = CronManager(tasks, None, data_manager)

    assert isinstance(cron_manager.task_map, dict)
    assert cron_manager.task_map["test1"].name == "test1"
    assert cron_manager.task_map["test1"].cmd == ["python3", "./tests/case1.py"]
    assert cron_manager.task_map["test2"].name == "test2"
    assert cron_manager.task_map["test2"].cmd == ["python3", "./tests/case2.py"]


from queue import Queue
from typing import List, Dict
from booflow.interface import TaskManagerInterface, DataManagerInterface


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


class FakeDataManager(DataManagerInterface):
    def add_task_data(self, task_name: str, command: str, retry: int) -> None:
        pass

    def add_task_status(
        self, task_name: str, status: bool, msg: str, output_msg: str
    ) -> None:
        pass


def test_cron_manager_run():

    tasks = [
        {"task_name": "test1", "command": "python3 ./tests/case1.py"},
        {"task_name": "test2", "command": "python3 ./tests/case2.py"},
    ]

    order = ["test1", "test2"]

    task_manager = FakeTaskManager(order)
    data_manager = FakeDataManager()

    cron_manager = CronManager(tasks, task_manager, data_manager)

    r = cron_manager.run()

    assert r == {"success": ["test1"], "fail": ["test2"]}
