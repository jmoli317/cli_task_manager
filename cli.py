import argparse
from task_manager import TaskManager


def cmd_parser():
    """
    Build the argument parser with task subcommands.

    :returns: Configured parser ready to parse CLI input.
    :rtype: argparse.ArgumentParser
    """

    parser = argparse.ArgumentParser(
        description=(
            "Manage tasks stored in a JSON file with commands to list, add, "
            "edit, toggle status, and delete entries."
        )
        )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Available task commands"
        )

    subparsers.add_parser(
        "list",
        help="Display all tasks with their indices and completion status.",
        description="Show the current task table."
        )

    add_cmd = subparsers.add_parser(
        "add",
        help="Create a new task and append it to the list.",
        description="Add a task description to the task list."
        )
    add_cmd.add_argument(
        "task",
        type=str,
        help="Description text to store for the new task.",
        )
    add_cmd.add_argument(
        "--index",
        type=int,
        help=(
            "Insert the task at a zero-based index instead of appending to "
            "the end."
            ),
        )

    edit_cmd = subparsers.add_parser(
        "edit",
        help="Replace the description text for an existing task.",
        description="Update the description for the task at the given index."
        )

    edit_cmd.add_argument(
        "index",
        type=int,
        help="Zero-based index of the task to edit."
        )
    edit_cmd.add_argument(
        "text",
        type=str,
        help="Replacement description text for the task."
        )

    status_cmd = subparsers.add_parser(
        "status",
        help="Toggle the completion status of a task.",
        description="Switch a task between IN PROGRESS and DONE."
        )
    status_cmd.add_argument(
        "index",
        type=int,
        help="Index of the task to update."
        )

    delete_cmd = subparsers.add_parser(
        "delete",
        help="Remove a task from the list.",
        description="Delete the task located at the provided index."
        )
    delete_cmd.add_argument(
        "index",
        type=int,
        help="Zero-based index of the task to delete from the list."
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
            tm.add_task(args.task, index=args.index)
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
