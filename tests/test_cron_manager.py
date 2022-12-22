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
