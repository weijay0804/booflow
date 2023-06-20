# BooFlow

一個簡單輕量的任務執行順序控制器  

假設你有一個這樣的任務列表
![](/static/images/case1.png)

BooFlow 會自動幫你依照 `A -> B -> F -> C -> D -> E -> G` 的順序來執行任務

## Useage
> 每個任務需要是一個可以執行的檔案，或是一個指令 

例如：  
Task A 是執行一個 Python 檔案，那就要寫成
```bash
$ python <path_to_your_python file>
```

Task B 是一個 bash 指令，那就要寫成
``` bash
$ mkdir test_dir
```

> 使用範例

```python

from booflow import booflow

# 定義任務
# 注意! 任務名稱不能重複
tasks = [
    {"task_name" : "task_a", "command" : "python test.py"},
    {"task_name" : "task_b", "command" : "mkdir test_dir"},
    {"task_name" : "task_c", "command" : "python test2.py"},
    {"task_name" : "task_d", "command" : "python test3.py"},
    {"task_name" : "task_e", "command" : "python test4.py"},
    {"task_name" : "task_f", "command" : "python test5.py"},
    {"task_name" : "task_g", "command" : "python test6.py"}
]

# 定義任務順序
# start -> end
taks_order = [
    ("task_a", "task_b"),
    ("task_b", "task_c"),
    ("task_b", "task_d"),
    ("task_b", "task_f"),
    ("task_d", "task_e"),
    ("task_f", "task_g"),
    ("task_e", "task_g")
]

# 執行
booflow.run(tasks, task_order)