# BooFlow

一個簡單輕量的任務執行順序控制器  

假設你有一個這樣的任務列表
![](/static/images/case1.png)

BooFlow 會自動幫你依照 `A -> B -> F -> C -> D -> E -> G` 的順序來執行任務

## 快速上手
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

from booflow import BooFlow

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
bf = BooFlow(tasks, task_order)
bf.run()
```

## 任務參數設定

在每一個任務中，可以額外設定參數，來控制任務的執行  
例如：

``` python
tasks = [
    {"task_name" : "task1", "command" : "python3 task1.py", "timeout" : 120, "retry" 2}
    ]
```

可以設定的參數： 

- `task_name` (str): 任務名稱，必須是唯一值
- `command` (str): 任務指令
- `timeout` [選填] (float): 最大任務執行時間，如果超過這個時間，任務會被強制終止 (單位為秒)
- `retry` [選填] (int): 任務執行失敗時的重新執行次數 (默認為 3)

## 排程參數設定

可以額外設定排程執行時的相關參數  
例如：

``` python

config = {"log_file_path" : "./my_log.log"}
```

可以設定的參數：
- `log_file_path` (str): log 紀錄檔存放位置 (默認會存放在 `./log/YYYY-MM-DD_HH:SS.log`)