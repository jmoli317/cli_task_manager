import pytest
from pathlib import Path
from task_manager import TaskManager


@pytest.fixture(scope="function")
def tasks_file(tmp_path) -> Path:
    return tmp_path / "test_tasks.json"


def test_task_manager_init_creates_json_if_nonexistent(tasks_file):
    assert not tasks_file.exists()
    tm = TaskManager(file_path=tasks_file)
    assert tasks_file.exists()
    assert tm.tasks == []


def test_add_task_description_and_status(tasks_file):
    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    tm.add_task(description="write docstrings", is_done=True)
    assert tm.tasks == [("test the code", False), ("write docstrings", True)]


def test_add_task_description_and_status_at_index(tasks_file):
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
    tasks_file
    ):
    tm = TaskManager(file_path=tasks_file)
    with pytest.raises(ValueError) as e:
        tm.add_task(description="test the code", is_done=False, index=1)
    assert str(e.value) == "Task index out of range"


def test_add_task_saves_to_json_file(tasks_file):
    tm1 = TaskManager(file_path=tasks_file)
    tm1.add_task(description="test the code", is_done=False)
    assert tm1.tasks == [("test the code", False)]

    tm2 = TaskManager(file_path=tasks_file)
    assert tm2.tasks == [("test the code", False)]
    assert tm1.tasks == tm2.tasks


def test_edit_task_description_at_index(tasks_file):
    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    assert tm.tasks == [("test the code", False)]
    tm.edit_task(index=0, new_description="test the program")
    assert tm.tasks == [("test the program", False)]


def test_edit_task_raises_value_error_if_index_out_of_range(
    tasks_file
    ):

    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    assert tm.tasks == [("test the code", False)]

    with pytest.raises(ValueError) as e:
        tm.edit_task(index=1, new_description="test the program")
    assert str(e.value) == "Task index out of range"


def test_edit_task_saves_to_json_file(tasks_file):
    tm1 = TaskManager(file_path=tasks_file)
    tm1.add_task(description="test the code", is_done=False)
    tm1.edit_task(index=0, new_description="test the program")
    assert tm1.tasks == [("test the program", False)]

    tm2 = TaskManager(file_path=tasks_file)
    assert tm2.tasks == [("test the program", False)]
    assert tm1.tasks == tm2.tasks


def test_update_task_status_at_index(tasks_file):
    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    assert tm.tasks == [("test the code", False)]
    tm.update_task_status(index=0)
    assert tm.tasks == [("test the code", True)]


def test_update_task_status_raises_value_error_if_index_out_of_range(
    tasks_file
    ):
    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    assert tm.tasks == [("test the code", False)]

    with pytest.raises(ValueError) as e:
        tm.update_task_status(index=1)
    assert str(e.value) == "Task index out of range"


def test_update_task_status_saves_to_json_file(tasks_file):
    tm1 = TaskManager(file_path=tasks_file)
    tm1.add_task(description="test the code", is_done=False)
    tm1.update_task_status(index=0)
    assert tm1.tasks == [("test the code", True)]

    tm2 = TaskManager(file_path=tasks_file)
    assert tm2.tasks == [("test the code", True)]
    assert tm1.tasks == tm2.tasks


def test_delete_task_at_index(tasks_file):
    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    assert tm.tasks == [("test the code", False)]
    tm.delete_task(index=0)
    assert tm.tasks == []


def test_delete_task_raises_value_error_if_index_out_of_range(
    tasks_file
    ):
    tm = TaskManager(file_path=tasks_file)
    tm.add_task(description="test the code", is_done=False)
    assert tm.tasks == [("test the code", False)]

    with pytest.raises(ValueError) as e:
        tm.delete_task(index=1)
    assert str(e.value) == "Task index out of range"


def test_delete_task_saves_to_json_file(tasks_file):
    tm1 = TaskManager(file_path=tasks_file)
    tm1.add_task(description="test the code", is_done=False)
    tm1.delete_task(index=0)
    assert tm1.tasks == []

    tm2 = TaskManager(file_path=tasks_file)
    assert tm2.tasks == []
    assert tm1.tasks == tm2.tasks
