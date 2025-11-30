import json
from pathlib import Path


class TaskManager:
    """
    A class to manage CRUD operations for a task list.
    """
    def __init__(self, file_name: str = "task_list.json"):
        """
        Initialize the class and verify that the json file exists.

        :param file_name: JSON file name for task list storage.
        """

        self.file_name = file_name

        if not Path(self.file_name).exists():
            with open(file_name, "w") as file:
                json.dump([], file)

        self.tasks = json.load(open(self.file_name))

    def list_tasks(self):
        """
        Print the task list to the command line interface.

        :return: None
        """

        index_header = "Index"
        max_index = len(self.tasks)

        width = max(len(index_header), len(str(max_index)))

        print(f"{index_header:>{width}}  Task")
        print("-" * (width + 2 + len("Task")))

        for i, task in enumerate(self.tasks):
            print(f"{i:>{width}}  {task}")

    def save_tasks(self):
        """
        Save the task list to the json file.

        :return: None
        """

        with open(self.file_name, "w") as file:
            json.dump(self.tasks, file)

    def add_task(self, task: str, index: int = None):
        """
        Add a new task to the task list.

        :param task: Description of the new task.
        :param index: Index to insert new task.
        :return: List of tasks (including the new task).
        """
        if index is None:
            self.tasks.append(task)
        else:
            self.tasks.insert(index, task)
        self.save_tasks()
        return self.tasks

    def edit_task(self, index: int, new_task: str):
        """
        Edit a task from the task list.

        :param index: Index of an existing task.
        :param new_task: Updated description of the task.
        :return: List of tasks (with the updated task).
        """
        if index < 0 or index >= len(self.tasks):
            raise ValueError("Task index out of range")
        self.tasks[index] = new_task
        self.save_tasks()
        return self.tasks

    def delete_task(self, task_index: int):
        """
        Delete a task from the task list.

        :param task_index: Index of an existing task.
        :return: List of tasks (without the deleted task).
        """
        if task_index < 0 or task_index >= len(self.tasks):
            raise ValueError("Task index out of range")
        del self.tasks[task_index]
        self.save_tasks()
