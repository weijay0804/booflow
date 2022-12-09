'''
Author: Shawn
Date: 2022-12-09 15:15:41
LastEditors: Shawn
LastEditTime: 2022-12-09 15:21:46
FilePath: /booflow/main.py
Description: 

Copyright (c) 2022 by shianshiu shianhian327@gmail.com, All Rights Reserved. 
'''
from DAG import Booflow


commands = {
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

info = {"retry": 3, "timeout": None, "log_path": None}


bflow = Booflow(flow_id=11, task_relation=task_relation, **info)
bflow.run()
