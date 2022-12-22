"""
Author: weijay
Date: 2022-12-21 17:12:35
LastEditors: weijay
LastEditTime: 2022-12-21 17:13:51
Description: 主要是放跟 task manager 相關的模組
"""

from typing import List, Optional, Tuple
from collections import deque, defaultdict


class TaskManager:
    """任務管理"""

    def __init__(self, tasks: List[dict], orders: List[tuple]) -> None:
        """建立 TaskManager 實例

        Args:
            tasks (List[dict]): 排程任務清單
            orders (List[tuple]): 排程之間的順序關係
        """

        pass

    def next(self) -> Optional[str]:
        """提供下一個任務的名稱，如果當前沒有任務則回傳 None

        Returns:
            Optional[str]: 對應至 config 中的 task_name
        """

        pass

    def call(self, task_name: str, status: bool) -> bool:
        """回傳任務名稱以及完成狀態

        Args:
            task_name (str): 對應至 config 中的 task_name
            status (bool): 執行成功是 True 反之 False

        Returns:
            bool: 函示成功則回傳 True 反之 False
        """

        pass

    def progress(self):

        pass


def transform_tasks_to_graph(tasks: List[tuple]) -> Tuple[defaultdict, defaultdict]:
    graph = defaultdict(set)
    indegree = defaultdict(int)
    for start, end in tasks:
        if end not in graph[start]:
            graph[start].add(end)
            indegree[start]
            indegree[end] += 1
    print("圖：", graph)
    print("入度", indegree)
    return graph, indegree


def extract_graph_task_order(graph: defaultdict, indegree: defaultdict) -> List:
    task_order = []
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
