import argparse
from task_manager import TaskManager


def cmd_parser():
    """
    Build the argument parser with task subcommands.

    :returns: Configured parser ready to parse CLI input.
    :rtype: argparse.ArgumentParser
    """

    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list")

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
        "text",
        type=str,
        help="New task description."
        )

    status_cmd = subparsers.add_parser("status")
    status_cmd.add_argument(
        "index",
        type=int,
        help="Index of the task to update."
        )

    delete_cmd = subparsers.add_parser("delete")
    delete_cmd.add_argument(
        "index",
        type=int,
        help="Index of the task to delete."
        )

    return parser


def main():
    """
    Parse CLI arguments and route to TaskManager actions.

    :returns: ``None``
    """

    tm = TaskManager()
    command_parser = cmd_parser()

    args = command_parser.parse_args()
    if args.command == "list":
        tm.list_tasks()
    elif args.command == "add":
        if args.index is not None:
            tm.add_task(args.task, args.index)
        else:
            tm.add_task(args.task)
    elif args.command == "edit":
        tm.edit_task(args.index, args.text)
    elif args.command == "status":
        tm.update_task_status(args.index)
    elif args.command == "delete":
        tm.delete_task(args.index)


if __name__ == "__main__":
    main()
