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
        pass

    def add_task(self):
        pass

    def edit_task(self):
        pass

    def delete_task(self):
        pass
