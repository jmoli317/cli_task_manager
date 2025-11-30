import json
from pathlib import Path


class TaskManager:

    def __init__(self, file_name: str = "task_list.json"):
        self.file_name = file_name

        if not Path(self.file_name).exists():
            with open(file_name, "w") as file:
                json.dump([], file)

        self.tasks = json.load(open(self.file_name))

    def list_tasks(self):

        index_header = "Index"
        max_index = len(self.tasks)

        width = max(len(index_header), len(str(max_index)))

        print(f"{index_header:>{width}}  Task")
        print("-" * (width + 2 + len("Task")))

        for i, task in enumerate(self.tasks):
            print(f"{i:>{width}}  {task}")

    def save_tasks(self):
        with open(self.file_name, "w") as file:
            json.dump(self.tasks, file)

    def add_task(self, task: str, index: int = None):
        if index is None:
            self.tasks.append(task)
        else:
            self.tasks.insert(index, task)
        self.save_tasks()
        return self.tasks

    def edit_task(self, task_index: int, new_task: str):
        if task_index < 0 or task_index >= len(self.tasks):
            raise ValueError("Task index out of range")
        self.tasks[task_index] = new_task
        self.save_tasks()
        return self.tasks

    def delete_task(self, task_index: int):
        if task_index < 0 or task_index >= len(self.tasks):
            raise ValueError("Task index out of range")
        del self.tasks[task_index]
        self.save_tasks()
