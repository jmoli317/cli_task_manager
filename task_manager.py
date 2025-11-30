import json
from pathlib import Path


class TaskManager:
    """
    Manage a JSON-backed list of tasks with convenience helpers.

    :param file_name: JSON file path used to save tasks.
    :type file_name: str
    """

    def __init__(self, file_name: str = "task_list.json"):
        """
        Initialize storage and load tasks.

        :param file_name: JSON file path used to save tasks.
        :type file_name: str
        """

        self.file_name = file_name

        if not Path(self.file_name).exists():
            with open(file_name, "w") as file:
                json.dump([], file)

        with open(file_name, "r") as file:
            self.tasks = json.load(file)

    def list_tasks(self):
        """
        Print the task list to the command line interface.

        :returns: ``None``
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
        Save the task list to disk.

        :returns: ``None``
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
        Append or insert a new task.

        :param task: Task description to store.
        :type task: str
        :param is_done: Task completion status.
        :type is_done: bool
        :param index: Position to insert the task (optional).
        :type index: int | None
        :returns: Updated list of tasks.
        :rtype: list
        :raises ValueError: If ``index`` is out of range.
        """

        new_task = [task, is_done]
        if index is None:
            self.tasks.append(new_task)
        else:
            if index < 0 or index >= len(self.tasks):
                raise ValueError("Index out of range")
            self.tasks.insert(index, new_task)
        self.save_tasks()
        return self.tasks

    def edit_task(self, index: int, new_task: str):
        """
        Replace a task description at ``index``.

        :param index: Position of the task to edit.
        :type index: int
        :param new_task: Replacement task description.
        :type new_task: str
        :returns: Updated list of tasks after the edit.
        :rtype: list
        :raises ValueError: If ``index`` is out of range.
        """

        if index < 0 or index >= len(self.tasks):
            raise ValueError("Task index out of range")
        self.tasks[index] = [new_task, self.tasks[index][1]]
        self.save_tasks()
        return self.tasks

    def update_task_status(self, index: int):
        """
        Change the completion status for a task at ``index``.

        :param index: Position of the task to update the status.
        :type index: int
        :returns: Updated list of tasks after the status change.
        :rtype: list
        :raises ValueError: If ``index`` is out of range.
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
        Remove the task at ``index`` from the list.

        :param index: Position of the task to delete.
        :type index: int
        :returns: Updated list of tasks after removal.
        :rtype: list
        :raises ValueError: If ``index`` is out of range.
        """

        if index < 0 or index >= len(self.tasks):
            raise ValueError("Task index out of range")
        del self.tasks[index]
        self.save_tasks()
        return self.tasks
