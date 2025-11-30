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
        help="Index of the task to edit."
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


if __name__ == "__main__":
    tm = TaskManager()
    command_parser = cmd_parser()
    args = command_parser.parse_args()
    if args.command == "add":
        if args.index is not None:
            tm.add_task(args.task, args.index)
        else:
            tm.add_task(args.task)
    if args.command == "edit":
        tm.edit_task(args.index, args.new_text)
    if args.command == "delete":
        tm.delete_task(args.index)
