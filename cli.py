import argparse
from task_manager import TaskManager


def cmd_parser():

    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_cmd = subparsers.add_parser("add")
    add_cmd.add_argument(
        "task",
        type=str,
        help="Description of the task",
        )
    add_cmd.add_argument(
        "--index",
        type=int,
        help="Index where to insert the task.",
        )

    edit_cmd = subparsers.add_parser("edit")
    edit_cmd.add_argument(
        "index",
        type=int,
        description="Index of the task to edit."
        )
    edit_cmd.add_argument(
        "new_text",
        type=str,
        help="New task description."
        )

    delete_cmd = subparsers.add_parser("delete")
    delete_cmd.add_argument(
        "index",
        type=int,
        help="Index of the task to delete."
        )

    return parser
