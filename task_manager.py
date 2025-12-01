import json
from pathlib import Path


class TaskManager:
    """
    Manage tasks stored in a JSON-backed file.

    Load tasks from a JSON file at initialization and provide methods
    to list, add, edit, update status, and delete tasks.
    """

    def __init__(self, file_path: Path = Path("tasks.json")) -> None:
        """
        Initialize the task manager and load tasks from disk.

        Create the JSON file if it does not exist and define the tasks
        attribute from the data in the file.
        """

        self.file_path = file_path
        if not file_path.exists():
            with open(file_path, "w") as fp:
                json.dump([], fp)

        with open(file_path, "r") as fp:
            self.tasks = [tuple(task) for task in json.load(fp)]

    def list_tasks(self) -> None:
        """
        Print the task table to the command-line interface.

        Show indices, descriptions, and status values in aligned columns
        with headers and a separator line.

        Example:

        Index  Task             Status
        -------------------------------
        0      write tests      IN PROGRESS
        1      update README    DONE

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

        print()

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
        print()

    def save_tasks(self) -> None:
        """
        Save the current task list to disk.

        Write the tasks list to the JSON file specified by the
        file_path attribute. This method is invoked internally by add_task,
        edit_task, update_task_status, and delete_task.
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
        Add a new task to the list.

        Append the task when no index is given or insert it at the
        provided zero-based index. Raise a ValueError when the index is
        outside the valid range and return the updated list of tasks.

        Example:
        >>> TaskManager().tasks
        [("test the code", False)]
        >>> TaskManager().add_task("write docs")
        [("test the code", False), ("write docs", False)]
        """


        new_task = (description, is_done)
        if index is None:
            self.tasks.append(new_task)
        else:
            if index < 0 or index >= len(self.tasks):
                raise ValueError("Task index out of range")
            self.tasks.insert(index, new_task)
        self.save_tasks()
        return self.tasks

    def edit_task(
        self,
        index: int,
        new_description: str
        ) -> list[tuple[str, bool]]:
        """
        Edit the description of a task at the given index.

        Replace the existing description while preserving the completion
        status. Raise a ValueError when the index is outside the valid
        range and return the updated list of tasks.

        Example:
        >>> TaskManager().tasks
        [("test the code", False)]
        >>> TaskManager().edit_task(0, "test the program")
        [("test the program", False)]
        """


        if index < 0 or index >= len(self.tasks):
            raise ValueError("Task index out of range")

        old_description, is_done = self.tasks[index]
        self.tasks[index] = (new_description, is_done)
        self.save_tasks()
        return self.tasks

    def update_task_status(self, index: int) -> list[tuple[str, bool]]:
        """
        Toggle the completion status of a task at the given index.

        Switch the task between done and in-progress states. Raise a
        ValueError when the index is outside the valid range and return
        the updated list of tasks.

        Example:
        >>> TaskManager().tasks
        [("test the code", False)]
        >>> TaskManager().update_task_status(0)
        [("test the code", True)]
        """

        if index < 0 or index >= len(self.tasks):
            raise ValueError("Task index out of range")

        description, is_done = self.tasks[index]
        self.tasks[index] = (description, not is_done)
        self.save_tasks()
        return self.tasks

    def delete_task(self, index: int) -> list[tuple[str, bool]]:
        """
        Delete the task at the given index.

        Remove the task from the list. Raise a ValueError when the index
        is outside the valid range and return the updated list of tasks.

        Example:
        >>> TaskManager().tasks
        [("test the code", False), ("write docs", True)]
        >>> TaskManager().delete_task(0)
        [("write docs", True)]
        """

        if index < 0 or index >= len(self.tasks):
            raise ValueError("Task index out of range")
        del self.tasks[index]
        self.save_tasks()
        return self.tasks
