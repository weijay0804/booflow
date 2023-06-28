'''
Author: weijay
Date: 2023-06-22 22:27:41
LastEditors: weijay
LastEditTime: 2023-06-28 23:59:15
Description: Task 單元測試
'''

import unittest
from collections import defaultdict, deque

from booflow import Task


class TestTask(unittest.TestCase):
    def test_tasks_order_to_graph(self):
        test_tasks_order = [("A", "B"), ("A", "C"), ("B", "D")]

        task_obj = Task([])

        graph, indegree, reverse_depne_graph = task_obj._tasks_order_to_graph(test_tasks_order)

        test_graph = defaultdict(set)
        test_graph["A"].add("B")
        test_graph["A"].add("C")
        test_graph["B"].add("D")

        test_indegree = defaultdict(int)
        test_indegree["A"] = 0
        test_indegree["B"] = 1
        test_indegree["C"] = 1
        test_indegree["D"] = 1

        test_rever_depen_graph = defaultdict(set)
        test_rever_depen_graph["B"].add("A")
        test_rever_depen_graph["C"].add("A")
        test_rever_depen_graph["D"].add("B")

        self.assertEqual(graph, test_graph)
        self.assertEqual(indegree, test_indegree)
        self.assertEqual(reverse_depne_graph, test_rever_depen_graph)

    def test_gen_tasks_queue(self):
        task_obj = Task([])

        test_graph = defaultdict(set)
        test_graph["A"].add("B")
        test_graph["A"].add("C")
        test_graph["B"].add("D")

        test_indegree = defaultdict(int)
        test_indegree["A"] = 0
        test_indegree["B"] = 1
        test_indegree["C"] = 1
        test_indegree["D"] = 1

        task_queue = task_obj._gen_tasks_queue(test_graph, test_indegree)

        test_task_queue_list = []
        test_task_queue_list.append(["A", "B", "C", "D"])
        test_task_queue_list.append(["A", "C", "B", "D"])

        self.assertIn(list(task_queue), test_task_queue_list)

    def test_remove_faile_task(self):
        test_tasks_order = [("A", "B"), ("A", "C"), ("B", "D")]

        task_obj = Task(test_tasks_order)

        test_graph = defaultdict(set)
        test_graph["A"].add("B")
        test_graph["A"].add("C")
        test_graph["B"].add("D")
        test_graph["C"]
        test_graph["D"]

        self.assertTrue(len(task_obj.faile_tasks) == 0)
        self.assertEqual(task_obj._graph, test_graph)

        task_obj.remove_faile_task("A")

        test_faile_tasks = defaultdict(set)
        test_faile_tasks["A"].add("B")
        test_faile_tasks["A"].add("C")
        test_faile_tasks["A"].add("D")

        self.assertEqual(task_obj.faile_tasks, test_faile_tasks)

        test_graph = defaultdict(set)
        test_graph["C"]
        test_graph["D"]

        self.assertEqual(task_obj._graph, test_graph)

    def test_remove_success_task(self):
        test_task_order = [("A", "B"), ("A", "C"), ("B", "D")]

        task_obj = Task(test_task_order)

        test_graph = defaultdict(set)
        test_graph["A"].add("B")
        test_graph["A"].add("C")
        test_graph["B"].add("D")
        test_graph["C"]
        test_graph["D"]

        self.assertTrue(len(task_obj.faile_tasks) == 0)
        self.assertEqual(task_obj._graph, test_graph)

        task_obj.remove_success_task("A")

        test_success_tasks = set()
        test_success_tasks.add("A")

        self.assertEqual(test_success_tasks, task_obj.success_tasks)

        test_graph = defaultdict(set)
        test_graph["B"].add("D")
        test_graph["D"]
        test_graph["C"]

        test_indepndent_tasks = deque()
        test_indepndent_tasks.append("C")

        self.assertEqual(task_obj._graph, test_graph)
        self.assertEqual(task_obj._independent_tasks_queue, test_indepndent_tasks)

    def test_graph_to_tasks_order(self):
        task_obj = Task([])

        test_graph = defaultdict(set)
        test_graph["A"].add("B")
        test_graph["A"].add("C")
        test_graph["B"].add("D")
        test_graph["C"]
        test_graph["D"]

        test_tasks_order_queue_list = []
        test_tasks_order_queue_list.append([("A", "B"), ("A", "C"), ("B", "D")])
        test_tasks_order_queue_list.append([("A", "C"), ("A", "B"), ("B", "D")])

        self.assertIn(task_obj._graph_to_tasks_order(test_graph), test_tasks_order_queue_list)

    def test_update_tasks_order_queue(self):
        test_tasks_order = [("A", "B"), ("A", "C"), ("B", "D")]

        task_obj = Task(test_tasks_order)

        task_obj.remove_success_task("A")

        test_tasks_order_queue_list = []
        test_tasks_order_queue_list.append(deque(["A", "B", "C", "D"]))
        test_tasks_order_queue_list.append(deque(["A", "C", "B", "D"]))

        self.assertIn(task_obj.tasks_order_queue, test_tasks_order_queue_list)

        task_obj.update_tasks_order_queue()

        self.assertEqual(task_obj.tasks_order_queue, deque(["B", "D"]))

    def test_is_task_can_be_execute(self):
        test_tasks_order = [("A", "B"), ("A", "C"), ("B", "D")]

        task_obj = Task(test_tasks_order)

        self.assertTrue(task_obj.is_task_can_be_execute("A"))
        self.assertFalse(task_obj.is_task_can_be_execute("B"))
        self.assertFalse(task_obj.is_task_can_be_execute("C"))
        self.assertFalse(task_obj.is_task_can_be_execute("D"))

        task_obj.remove_success_task("A")
        task_obj.update_tasks_order_queue()

        self.assertTrue(task_obj.is_task_can_be_execute("B"))
        self.assertTrue(task_obj.is_task_can_be_execute("C"))
        self.assertFalse(task_obj.is_task_can_be_execute("D"))

    def test_next_with_remove_success_task(self):
        test_tasks_order = [("A", "B"), ("A", "C"), ("B", "D")]

        task_obj = Task(test_tasks_order)

        self.assertEqual(task_obj.next, "A")
        self.assertIsNone(task_obj.next)

        # 回報任務
        task_obj.remove_success_task("A")
        task_obj.update_tasks_order_queue()

        self.assertEqual(task_obj.next, "B")
        self.assertEqual(task_obj.next, "C")
        self.assertIsNone(task_obj.next)

    def test_next_with_remove_faile_task(self):
        test_tasks_order = [("A", "B"), ("A", "C"), ("B", "D")]

        task_obj = Task(test_tasks_order)

        self.assertEqual(task_obj.next, "A")
        self.assertIsNone(task_obj.next)

        # 回報任務
        task_obj.remove_faile_task("A")
        task_obj.update_tasks_order_queue()

        self.assertIsNone(task_obj.next)

    def test_is_empty_with_remove_success_task(self):
        test_tasks_order = [("A", "B"), ("A", "C"), ("B", "D")]

        task_obj = Task(test_tasks_order)

        self.assertFalse(task_obj.is_empty)

        task_obj.remove_success_task("A")
        task_obj.update_tasks_order_queue()

        self.assertFalse(task_obj.is_empty)

        task_obj.remove_success_task("B")
        task_obj.update_tasks_order_queue()

        self.assertFalse(task_obj.is_empty)

        task_obj.remove_success_task("D")
        task_obj.update_tasks_order_queue()

        self.assertFalse(task_obj.is_empty)

    def test_is_empty_with_remove_faile_task(self):
        test_tasks_order = [("A", "B"), ("A", "C"), ("B", "D")]

        task_obj = Task(test_tasks_order)

        self.assertFalse(task_obj.is_empty)

        task_obj.remove_faile_task("A")
        task_obj.update_tasks_order_queue()

        self.assertTrue(task_obj.is_empty)
