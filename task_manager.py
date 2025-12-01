import json
from pathlib import Path


class TaskManager:
    """
    Manage a JSON-backed list of tasks with convenience helpers.

    :param file_path: JSON file path used to save tasks.
    :type file_path: Path
    """

    def __init__(self, file_path: Path = Path("tasks.json")) -> None:
        """
        Initialize storage and load tasks.

        :param file_path: JSON file path used to save tasks.
        :type file_path: Path
        """

        self.file_path = file_path
        if not file_path.exists():
            with open(file_path, "w") as fp:
                json.dump([], fp)

        with open(file_path, "r") as fp:
            self.tasks = json.load(fp)

    def list_tasks(self) -> None:
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

        for index, (description, is_done) in enumerate(self.tasks):
            status = "DONE" if is_done else "IN PROGRESS"
            print(
                f"{index:>{index_width}}  {description:<{task_width}} "
                f" {status}"
                )
        print()  # blank line after table

    def save_tasks(self) -> None:
        """
        Save the task list to disk.

        :returns: ``None``
        """

        with open(self.file_path, "w") as fp:
            json.dump(self.tasks, fp)

    def add_task(
        self,
        description: str,
        is_done: bool = False,
        index: int | None = None
        ) -> list[tuple[str, bool]]:
        """
        Append or insert a new task.

        :param description: Task description to store.
        :type description: str
        :param is_done: Task completion status.
        :type is_done: bool
        :param index: Index to insert the task (optional).
        :type index: int | None
        :returns: Updated list of tasks.
        :rtype: list
        :raises ValueError: If ``index`` is out of range.
        """

        new_task = (description, is_done)
        if index is None:
            self.tasks.append(new_task)
        else:
            if index < 0 or index >= len(self.tasks):
                raise ValueError("Index out of range")
            self.tasks.insert(index, new_task)
        self.save_tasks()
        return self.tasks

    def edit_task(
        self,
        index: int,
        new_description: str
        ) -> list[tuple[str, bool]]:
        """
        Replace a task description at ``index``.

        :param index: Index of the task to edit.
        :type index: int
        :param new_description: Replacement task description.
        :type new_description: str
        :returns: Updated list of tasks after the edit.
        :rtype: list
        :raises ValueError: If ``index`` is out of range.
        """

        if index < 0 or index >= len(self.tasks):
            raise ValueError("Task index out of range")

        old_description, is_done = self.tasks[index]
        self.tasks[index] = (new_description, is_done)
        self.save_tasks()
        return self.tasks

    def update_task_status(self, index: int) -> list[tuple[str, bool]]:
        """
        Change the completion status for a task at ``index``.

        :param index: Index of the task to update the status.
        :type index: int
        :returns: Updated list of tasks after the status change.
        :rtype: list
        :raises ValueError: If ``index`` is out of range.
        """

        if index < 0 or index >= len(self.tasks):
            raise ValueError("Task index out of range")

        description, is_done = self.tasks[index]
        self.tasks[index] = (description, not is_done)
        self.save_tasks()
        return self.tasks

    def delete_task(self, index: int) -> list[tuple[str, bool]]:
        """
        Remove the task at ``index`` from the list.

        :param index: Index of the task to delete.
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
