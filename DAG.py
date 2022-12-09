'''
Author: Shawn
Date: 2022-12-09 13:20:59
LastEditors: Shawn
LastEditTime: 2022-12-09 15:32:18
FilePath: /booflow/DAG.py
Description: 

Copyright (c) 2022 by shianshiu shianhian327@gmail.com, All Rights Reserved. 
'''
from typing import List, Tuple, DICT
from collections import deque, defaultdict


class Booflow:
    def __init__(sel, config: DICT) -> None:
        pass


def transform_tasks_to_graph(tasks: List[Tuple]) -> Tuple[defaultdict, defaultdict]:
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


{
    "A": "python3 /Users/shawnshiu/shawn_side_project/booflow/DAG.py",
    "B": "python3 /Users/shawnshiu/shawn_side_project/booflow/DAG.py",
    "C": "python3 /Users/shawnshiu/shawn_side_project/booflow/DAG.py",
}


task_relation = [
    ('A', 'B'),
    ('B', 'C'),
    ('B', 'D'),
    ('C', 'E'),
    ('D', 'G'),
    ('D', 'F'),
    ('F', 'G'),
    ('J', 'E'),
    ('E', 'G'),
    ('E', 'H'),
    ('G', 'I'),
]

graph, indegree = transform_tasks_to_graph(tasks=task_relation)
breakpoint()
task_order = extract_graph_task_order(graph=graph, indegree=indegree)


# TODO:
# 部分節點掛掉，不相關的節點理應可以繼續跑下去
# 動態調整
# 存儲的方式可以利用sqlLite去更新狀態


breakpoint()
