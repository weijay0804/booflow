"""
Author: weijay
Date: 2022-12-22 13:50:37
LastEditors: weijay
LastEditTime: 2022-12-22 13:50:38
Description: Cron 模組 單元測試
"""

import unittest

from booflow.booflow import Cron

TEST_CASE_PREFIX = "./tests/test_case"


class TestCron(unittest.TestCase):
    def test_parse_cmd(self):
        test_task = {"task_name": "test", "command": "python3 main.py"}

        c = Cron(test_task)

        self.assertEqual(c.cmd, ["python3", "main.py"])

    def test_cron_run(self):
        test_task = {"task_name": "test1", "command": f"python3 {TEST_CASE_PREFIX}/case1.py"}

        cron = Cron(test_task)

        res = cron.run()

        self.assertEqual(res, (True, None, "Hello from case1"))

    def test_cron_run_with_program_error(self):
        test_task = {"task_name": "test1", "command": f"python3 {TEST_CASE_PREFIX}/case2.py"}

        cron = Cron(test_task)

        res = cron.run()

        self.assertFalse(res[0])
        self.assertEqual(res[1], "program error")

    def test_cron_run_with_timeout(self):
        test_task = {
            "task_name": "test1",
            "command": f"python3 {TEST_CASE_PREFIX}/case3.py",
            "timeout": 2,
        }

        cron = Cron(test_task)

        res = cron.run()

        self.assertFalse(res[0])
        self.assertEqual(res[1], "time out")

    def test_cron_retry(self):
        test_task = {
            "task_name": "test1",
            "command": f"python3 {TEST_CASE_PREFIX}/case2.py",
            "retry": 2,
        }

        cron = Cron(test_task)
        res = cron.run()

        res_list = []

        res_list.append(res)

        if not res[0]:
            while cron.retry_time != 0:
                res = cron.retry()
                res_list.append(res)

        self.assertEqual(len(res_list), 3)
        self.assertFalse(all(i[0] for i in res_list))

        for e in res_list:
            self.assertEqual(e[1], "program error")

    def test_cron_retry_zero(self):
        test_task = {
            "task_name": "test1",
            "command": f"python3 {TEST_CASE_PREFIX}/case2.py",
            "retry": 0,
        }

        cron = Cron(test_task)

        res = cron.run()

        res_list = []

        res_list.append(res)

        if not res[0]:
            while cron.retry_time != 0:
                res = cron.retry()

                res_list.append(res)

        self.assertEqual(len(res_list), 1)
        self.assertFalse(all(i[0] for i in res_list))

        for e in res_list:
            self.assertEqual(e[1], "program error")
