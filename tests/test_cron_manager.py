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
