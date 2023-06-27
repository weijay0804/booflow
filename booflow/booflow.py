"""
Author: weijay
Date: 2023-01-06 00:34:59
LastEditors: weijay
LastEditTime: 2023-01-06 00:35:00
Description: booflow 主程式
"""

import os
import subprocess
from collections import deque, defaultdict
from typing import List, Dict, Tuple


class BooFlow:
    def __init__(self, tasks: List[Dict], order: list, config: dict = None):
        task_manager = TaskManager(order)

        self.cron_manager = CronManager(tasks, task_manager)

    @staticmethod
    def get_root_path() -> str:
        """取得專案根目錄

        Returns:
            str: 專案根目錄 (絕對路徑)
        """

        return os.path.abspath(os.path.dirname(__name__))

    def run(self):
        """啟動排程"""

        self.cron_manager.run()


class Cron:
    """針對每一個 command 的類別"""

    def __init__(self, config: dict) -> None:
        """建立 Cron 實例

        Args:
            config (dict): 排程設定資訊
        """

        self.name = config.get("task_name")
        self.cmd = self.__parse_cmd(config.get("command"))
        self.timeout = config.get("timeout")

        if config.get("retry") is None:
            self.retry_time = 3
        else:
            self.retry_time = config.get("retry")

    def __repr__(self) -> str:
        return f"Cron: {self.__format__} , Name: {self.name}, Cmd: {self.cmd}"

    def __parse_cmd(self, cmd: str) -> list:
        """將指令字串解析成 list

        Args:
            cmd (str): 指令字串，例如 "python3 main.py".

        Returns:
            list: 回傳解析後的指令 => ["python3", "main.py"]
        """

        return cmd.split()

    def run(self) -> Tuple[bool, str, str]:
        """執行指令
            會分成以下幾種狀況

            1. 執行成功，則回傳 (True, None, stdout)
            2. 程式錯誤，則回傳 (False, "program error", stderr)
            3. 執行逾時，則回傳 (False, "time out", None)
            4. 未知錯誤，則回傳 (False, "unknow error", error)

        Returns:
            Tuple[bool, str]: 詳見說明
        """

        try:
            r = subprocess.run(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout,
            )

            if r.stderr:
                return (
                    False,
                    "program error",
                    r.stderr.decode("utf8").replace("\n", ""),
                )

            else:
                return (True, None, r.stdout.decode("utf8").replace("\n", ""))

        except subprocess.TimeoutExpired:
            return (False, "time out", None)

        except Exception as e:
            return (False, "unknow error", str(e))

    def retry(self) -> Tuple[bool, str, str]:
        """重新執行一次 run 函示，並將 retry_time 減 1

        Returns:
            Tuple[bool, str, str]: run 函示的回傳值
        """

        if self.retry_time == 0:
            return

        self.retry_time -= 1

        return self.run()


class Task:
    """任務佇列 (被 :class:`TaskManager` 使用)

    通常會一個 :class:`Task` 會被一個 :class:`TaskManager` 管理，
    :class:`Task` 類別只是方便被 :class:`TaskManager` 管理建立的。

    Args:
        - tasks_orders (List[tuple]): 任務順序清單

    Attribute:

        - tasks_order_queue (dequeu): 任務執行佇列。

        - next (str): 回傳一個在目前狀態可以執行的任務名稱 (也就是說這個任務的依賴任務已經完成)。

        - is_empty (bool): 檢查目前的任務佇列是否為空的，如果是空的回傳 `True` ，反之回傳 `False`。

        - success_task (set): 順利執行完成的任務集合。

        - faile_task (defaultidict(set)): 執行失敗的任務字典 ( 其中 `key` 為失敗的任務名稱，而 `value` 為因為依賴這個任務而無法執行的任務集合) 。

    Usage:
        - 初始化物件時會自動產生任務有向圖等相關屬性。
        - 使用 :meth:`Task.next` 取得一個目前狀態下可以開始執行的任務名。
        - 使用 :meth:`Task.is_empty` 來檢查任務佇列是否為空。
        - 使用 :meth:`Task.remove_faile_task()` 移除一個失敗的任務，如果有其他任務依賴這個任務，也會被移除，並將相關訊息記錄到 `faile_task` 中，並且會自動更新 `graph` 、 `tasks_order` 等。
        - 使用 :meth:`Task.remove_success_task()` 移除一個成功的任務，並且將訊息記錄到 `success_tasks` 中，並且會自動更新 `graph` 、 `tasks_order` 等。
    """

    def __init__(self, tasks_order: List[tuple]):
        self._tasks_order = tasks_order

        # 獨立的任務佇列 ( 沒有依賴其他任務 )
        self._independent_tasks_queue = deque()

        # 先把 tasks_order 轉換成 graph
        self._graph, self._indegree, self._reverse_dependencies_graph = self._tasks_order_to_graph(
            self._tasks_order
        )

        self.tasks_order_queue = self._gen_tasks_queue(self._graph, self._indegree)
        self.success_tasks = set()
        self.faile_tasks = defaultdict(set)

    def _tasks_order_to_graph(
        self, tasks_order: List[tuple]
    ) -> Tuple[defaultdict, defaultdict, defaultdict]:
        """將任務順序列表轉換成有向圖，前兩個回傳的值可以給 :meth:`Task._gen_tasks_queue` 當參數傳入

        Args:
            tasks_order (List[tuple]): 任務順序清單

        Returns:
            Tuple[defaultdict, defaultdict, defaultdict]: ( 有向圖資料結構 (`graph`), 入度字典 (`indegree`), 反向關聯有向圖 (`reverse_dependencies_graph`) )
        """
        graph = defaultdict(set)
        indegree = defaultdict(int)
        # 加入反向關聯
        reverse_dependencies = defaultdict(set)

        for start, end in tasks_order:
            if end not in graph[start]:
                graph[start].add(end)
                indegree[start]
                indegree[end] += 1
                reverse_dependencies[end].add(start)

        return graph, indegree, reverse_dependencies

    def _gen_tasks_queue(self, graph: defaultdict, indegree: defaultdict) -> deque:
        """生成 tasks 執行順序佇列，在使用這個方法前，應該執行 :meth:`Task._tasks_order_to_graph` 方法

        Args:
            graph (defaultdict): 經由 :meth:`Task._tasks_order_to_graph` 生成的 graph.

            indegree (defaultdict): 經由 :meth:`Task._tasks_order_to_graph` 生成的 indegree.

        Returns:
            deque: 任務執行順序佇列
        """

        task_queue = deque()
        queue = deque()

        for idx, item in indegree.items():
            if item == 0:
                queue.append(idx)

        while queue:
            current_task = queue.popleft()
            task_queue.append(current_task)
            for next_task in graph[current_task]:
                indegree[next_task] -= 1
                if indegree[next_task] == 0:
                    queue.append(next_task)

        return task_queue

    def _remove_faile_task(self, graph: defaultdict, target: str, root_target: str):
        """輔助 :meth:`Task.remove_faile_task` 方法，使用遞迴的方式刪除跟 `target` 相關的節點，並將刪除的任務加入 `faile_tasks`

        Args:
            graph (defaultdict): 要從哪個 graph 中刪除節點

            target (str): 要刪除的任務名 (節點)
        """

        if graph.get(target):
            target_items = graph[target]

            del graph[target]

            for item in target_items:
                self.faile_tasks[root_target].add(item)
                self._remove_faile_task(graph, item, root_target=root_target)

    def remove_faile_task(self, target):
        """從 graph 中移除失敗的任務，如果有其他任務依賴這個任務，也會一起刪除"""

        self.faile_tasks[target]

        self._remove_faile_task(self._graph, target, root_target=target)

    def remove_success_task(self, target: str):
        """從 graph 中除成功的任務，並將任務加入至 `success_tasks`

        Args:
            target (str): 要移除的 task name
        """

        self.success_tasks.add(target)

        # target 是獨立任務
        if not self._graph.get(target):
            return

        del self._graph[target]

        # 檢查任務中是否有獨立的任務，如果有就加入到 independent_tasks_queue 中
        # 先使用反向關聯圖檢查依賴的任務
        for end, start_set in self._reverse_dependencies_graph.items():
            # 如果 start_set 長度是 1 就代表此時任務只依賴一個任務
            # 如果又剛好依賴的任務是要刪除的任務，那麼該任務就有可能會變成獨立任務
            if len(start_set) == 1 and target in start_set:
                # 如果在 graph 中該任務不是一個 key 的話，就表示該任務是獨立任務
                # 可以想成因為該節點沒有指向下一個節點
                if not self._graph.get(end):
                    self._independent_tasks_queue.append(end)

    def _graph_to_tasks_order(self, graph: defaultdict) -> List[tuple]:
        """將 graph 轉換成 tasks_orders

        Args:
            graph (defaultdict(set)): 要轉換的 graph

        Returns:
            List[tuple]: 將傳入的 `graph` 轉換後的任務順序清單

        """

        new_tasks = []
        for start, end_set in graph.items():
            for end in end_set:
                new_tasks.append((start, end))

        return new_tasks

    def update_tasks_order_queue(self):
        """在使用 `remove_success_task` 或 `remove_faile_task` 需要使用這個函示

        會根據目前的 `self_graph` 重新生成新的 `tasks_order`，在由 `tasks_order` 重新生成 `graph` 等相關屬性
        最後再重新生成新的 `tasks_order_queue`

        """

        # 如果使用了 `remove_success_task` 或 `remove_faile_task` 更新了 graph
        # 要依序更新 graph -> tasks_orders -> graph -> tasks_order_queue
        # 先把新的 graph 轉換成 tasks_order
        self._tasks_order = self._graph_to_tasks_order(self._graph)

        # 更新相關屬性
        self._graph, self._indegree, self._reverse_dependencies_graph = self._tasks_order_to_graph(
            self._tasks_order
        )
        self.tasks_order_queue = self._gen_tasks_queue(self._graph, self._indegree)

    def is_task_can_be_execute(self, task_name: str) -> bool:
        """判斷傳入的 task 在目前的狀態是否可以執行 (有可能依賴任務還沒完成)

        Args:
            task_name (str): 要判斷的任務名

        Returns:
            bool: 如果可以執行，回傳 `True` ，反之 `False`
        """

        if self._reverse_dependencies_graph.get(task_name):
            for dependen_task in self._reverse_dependencies_graph.get(task_name):
                if dependen_task not in self.success_tasks:
                    return False

        return True

    @property
    def next(self) -> str:
        """取得在目前狀態下，可以開始執行的任務名稱 (也就是這個任務依賴的任務已經完成，或是這個任務是獨立的任務)

        Returns:
            str: 回傳一個任務名稱
        """

        if self.tasks_order_queue:
            first_task = self.tasks_order_queue[0]

            if self.is_task_can_be_execute(first_task):
                return self.tasks_order_queue.popleft()

        if self._independent_tasks_queue:
            return self._independent_tasks_queue.popleft()

        return None

    @property
    def is_empty(self) -> bool:
        """檢查任務佇列或是獨立任務佇列是否為空的，可以用來檢查排程是否要繼續執行

        Returns:
            bool: 如果佇列中還有東西則會傳 `True`，反之回傳 `False`
        """

        return len(self.tasks_order_queue) == 0 and len(self._independent_tasks_queue) == 0


class TaskManager:
    """任務管理"""

    pass


class CronManager:
    """管理排程"""

    def __init__(
        self,
        tasks: List[dict],
        task_manager: "TaskManager",
    ) -> None:
        """建立 CronManager 實例

        Args:
            tasks (List[dict]): 排程任務清單
            task_manager (TaskManagerInterface): implement TaskManagerInterface 的實例
        """

        self.task_manager = task_manager
        self.task_map = self.generate_cron_dict(tasks)

    def generate_cron_dict(self, tasks: List[dict]) -> Dict[str, Cron]:
        """建立 task_name 與 Cron 物件之間的映射表

        Args:
            tasks (List[dict]): 排程任務清單

        Returns:
            List[dict]: {"task_name1" : "Cron1", "task_name2" : "Cron2", ....}
        """

        return {i["task_name"]: Cron(i) for i in tasks}

    def run(self) -> Dict[str, list]:
        """開始執行排程

        Returns:
            Dict[str, list]: 執行成功和失敗的任務
        """

        while not self.task_manager.is_empty():
            task_name = self.task_manager.get_next()

            result = self.task_map[task_name].run()

            if not result[0]:
                while self.task_map[task_name].retry_time != 0:
                    result = self.task_map[task_name].retry()

            self.task_manager.call(task_name, result[0])

        return "OK"
