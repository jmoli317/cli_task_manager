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

        with open(file_name, "r") as file:
            self.tasks = json.load(open(self.file_name))

    def list_tasks(self):
        """
        Print the task list to the command line interface.

        :return: None
        """

        index_header = "Index"
        task_header = "Task"
        status_header = "Status"

        max_index = len(self.tasks) - 1 if self.tasks else 0
        index_width = max(len(index_header), len(str(max_index)))
        task_width = max(
            len(task_header),
            max((len(t[0]) for t in self.tasks), default=0)
            )
        status_width = len(status_header)

        print()  # blank line before the table

        print(
            f"{index_header:>{index_width}}  {task_header:<{task_width}}  {status_header}"
            )

        separator_len = index_width + 2 + task_width + 2 + len(status_header)
        print("-" * separator_len)

        for i, task in enumerate(self.tasks):
            title = task[0]
            status = "DONE" if task[1] else "IN PROGRESS"
            print(f"{i:>{index_width}}  {title:<{task_width}}  {status}")
        print()  # blank line after table

    def save_tasks(self):
        """
        Save the task list to the json file.

        :return: None
        """

        with open(self.file_name, "w") as file:
            json.dump(self.tasks, file)

    def add_task(
        self,
        task: str,
        is_done: bool = False,
        index: int = None
        ):
        """
        Add a new task to the task list.

        :param task: Description of the new task.
        :param is_done: Completion status of the task.
        :param index: Index to insert new task.
        :return: List of tasks (including the new task).
        """
        if index is None:
            self.tasks.append([task, is_done])
        else:
            self.tasks.insert(index, [task, is_done])
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
        self.tasks[index] = [new_task, self.tasks[index][1]]
        self.save_tasks()
        return self.tasks

    def update_task_status(self, index: int):
        """
        Update the status of an existing task.

        :param index: Index of an existing task.
        :return: List of tasks (with the updated task).
        """
        if index < 0 or index >= len(self.tasks):
            raise ValueError("Task index out of range")
        if not self.tasks[index][1]:
            self.tasks[index][1] = True
        else:
            self.tasks[index][1] = False
        self.save_tasks()
        return self.tasks

    def delete_task(self, index: int):
        """
        Delete a task from the task list.

        :param index: Index of an existing task.
        :return: List of tasks (without the deleted task).
        """

        if index < 0 or index >= len(self.tasks):
            raise ValueError("Task index out of range")
        del self.tasks[index]
        self.save_tasks()
