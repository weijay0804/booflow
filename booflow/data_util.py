"""
Author: weijay
Date: 2023-01-05 17:51:05
LastEditors: weijay
LastEditTime: 2023-01-05 17:54:49
Description: 定義有關存儲資料的物件
"""

from .interface import DataManagerInterface


class MyTxt(DataManagerInterface):
    """使用 txt 檔的方式儲存"""

    def __init__(self, path: str):
        self.path = path

    def add_task_data(self, task_name: str, command: str, retry: int) -> None:

        with open(self.path, "a", encoding="utf8") as f:
            f.write(f"task_name : {task_name}, command: {command}, retry: {retry}")
            f.write("\n")

    def add_task_status(
        self, task_name: str, status: bool, msg: str, output_msg: str
    ) -> None:

        ff = "success" if status else "fail"

        with open(self.path, "a", encoding="utf8") as f:
            f.write(
                f"task_name : {task_name}, status : {ff}, message: {msg}, stdout : {output_msg}"
            )
            f.write("\n")
