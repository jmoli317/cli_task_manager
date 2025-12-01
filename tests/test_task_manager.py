import pytest
from pathlib import Path
from task_manager import TaskManager


@pytest.fixture(scope="function")
def tasks_file(tmp_path: Path) -> Path:
    """
    Provide a temporary path for a JSON task file.

    Return a file path located in the per-test temporary directory.
    """
    return tmp_path / "test_tasks.json"


def test_task_manager_init_creates_json_if_nonexistent(
    tasks_file: Path,
) -> None:
    """
    Verify that TaskManager creates a JSON file when none exists.

    Instantiate the manager with a nonexistent path and assert that
    the file is created and the tasks list starts empty.
    """
    assert not tasks_file.exists()
    tm = TaskManager(file_path=tasks_file)
    assert tasks_file.exists()
    assert tm.tasks == []


def test_add_task_description_and_status(tasks_file: Path) -> None:
    """
    Verify that add_task appends descriptions and status flags.

    Add two tasks with different completion states and assert that
    the tasks list contains both entries in order.
    """
    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    tm.add_task(description="write docstrings", is_done=True)
    assert tm.tasks == [("test the code", False), ("write docstrings", True)]


def test_add_task_description_and_status_at_index(
    tasks_file: Path,
) -> None:
    """
    Verify that add_task inserts a task at the given index.

    Append two tasks, then insert a third at index one and assert
    that the list reflects the new ordering.
    """
    tm = TaskManager(file_path=tasks_file)

    tm.add_task(description="test the code", is_done=False)
    assert tm.tasks[0] == ("test the code", False)

    tm.add_task(description="write docstrings", is_done=True)
    assert tm.tasks[1] == ("write docstrings", True)

    tm.add_task(description="push git commit", is_done=False, index=1)
    assert tm.tasks[0] == ("test the code", False)
    assert tm.tasks[1] == ("push git commit", False)
    assert tm.tasks[2] == ("write docstrings", True)


def test_add_task_raises_value_error_if_index_out_of_range(
    tasks_file: Path,
) -> None:
    """
    Verify that add_task rejects an out-of-range index.

    Create a manager with one task and assert that inserting at
    index one raises a ValueError with the expected message.
    """
    tm = TaskManager(file_path=tasks_file)
    with pytest.raises(ValueError) as e:
        tm.add_task(description="test the code", is_done=False, index=1)
    assert str(e.value) == "Task index out of range"


def test_add_task_saves_to_json_file(tasks_file: Path) -> None:
    """
    Verify that add_task persists changes to the JSON file.

    Add a task with one manager instance and assert that a new
    instance reading the same file sees the same tasks list.
    """
    tm1 = TaskManager(file_path=tasks_file)
    tm1.add_task(description="test the code", is_done=False)
    assert tm1.tasks == [("test the code", False)]

    tm2 = TaskManager(file_path=tasks_file)
    assert tm2.tasks == [("test the code", False)]
    assert tm1.tasks == tm2.tasks


def test_edit_task_description_at_index(tasks_file: Path) -> None:
    """
    Verify that edit_task updates the description at an index.

    Add a single task, edit its description, and assert that the
    status flag is preserved and the text is replaced.
    """
    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    assert tm.tasks == [("test the code", False)]
    tm.edit_task(index=0, new_description="test the program")
    assert tm.tasks == [("test the program", False)]


def test_edit_task_raises_value_error_if_index_out_of_range(
    tasks_file: Path,
) -> None:
    """
    Verify that edit_task rejects an out-of-range index.

    Add one task and assert that editing index one raises a
    ValueError with the expected message.
    """
    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    assert tm.tasks == [("test the code", False)]

    with pytest.raises(ValueError) as e:
        tm.edit_task(index=1, new_description="test the program")
    assert str(e.value) == "Task index out of range"


def test_edit_task_saves_to_json_file(tasks_file: Path) -> None:
    """
    Verify that edit_task persists changes to the JSON file.

    Edit a task description with one manager instance and assert
    that a new instance sees the updated tasks list.
    """
    tm1 = TaskManager(file_path=tasks_file)
    tm1.add_task(description="test the code", is_done=False)
    tm1.edit_task(index=0, new_description="test the program")
    assert tm1.tasks == [("test the program", False)]

    tm2 = TaskManager(file_path=tasks_file)
    assert tm2.tasks == [("test the program", False)]
    assert tm1.tasks == tm2.tasks


def test_update_task_status_at_index(tasks_file: Path) -> None:
    """
    Verify that update_task_status toggles the status flag.

    Add a single task marked not done, toggle its status, and
    assert that the flag becomes True.
    """
    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    assert tm.tasks == [("test the code", False)]
    tm.update_task_status(index=0)
    assert tm.tasks == [("test the code", True)]


def test_update_task_status_raises_value_error_if_index_out_of_range(
    tasks_file: Path,
) -> None:
    """
    Verify that update_task_status rejects an out-of-range index.

    Add one task and assert that toggling index one raises a
    ValueError with the expected message.
    """
    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    assert tm.tasks == [("test the code", False)]

    with pytest.raises(ValueError) as e:
        tm.update_task_status(index=1)
    assert str(e.value) == "Task index out of range"


def test_update_task_status_saves_to_json_file(tasks_file: Path) -> None:
    """
    Verify that update_task_status persists updates to the file.

    Toggle the status of a task with one manager instance and
    assert that a new instance sees the updated status.
    """
    tm1 = TaskManager(file_path=tasks_file)
    tm1.add_task(description="test the code", is_done=False)
    tm1.update_task_status(index=0)
    assert tm1.tasks == [("test the code", True)]

    tm2 = TaskManager(file_path=tasks_file)
    assert tm2.tasks == [("test the code", True)]
    assert tm1.tasks == tm2.tasks


def test_delete_task_at_index(tasks_file: Path) -> None:
    """
    Verify that delete_task removes a task at the given index.

    Add a single task, delete it by index, and assert that the
    tasks list becomes empty.
    """
    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    assert tm.tasks == [("test the code", False)]
    tm.delete_task(index=0)
    assert tm.tasks == []


def test_delete_task_raises_value_error_if_index_out_of_range(
    tasks_file: Path,
) -> None:
    """
    Verify that delete_task rejects an out-of-range index.

    Add one task and assert that deleting index one raises a
    ValueError with the expected message.
    """
    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    assert tm.tasks == [("test the code", False)]

    with pytest.raises(ValueError) as e:
        tm.delete_task(index=1)
    assert str(e.value) == "Task index out of range"


def test_delete_task_saves_to_json_file(tasks_file: Path) -> None:
    """
    Verify that delete_task persists removals to the JSON file.

    Delete the only task with one manager instance and assert that
    a new instance sees an empty tasks list.
    """
    tm1 = TaskManager(file_path=tasks_file)
    tm1.add_task(description="test the code", is_done=False)
    tm1.delete_task(index=0)
    assert tm1.tasks == []

    tm2 = TaskManager(file_path=tasks_file)
    assert tm2.tasks == []
    assert tm1.tasks == tm2.tasks

