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
        pass

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

    def edit_task(self):
        pass

    def delete_task(self):
        pass
