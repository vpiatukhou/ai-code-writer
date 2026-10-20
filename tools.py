import os
import os.path


_ENCODING = 'UTF-8'

PROMPT = """
You are a coding agent.

You can use tools.

If you are using a tool, answer with the following json:

{
    "tool_call": {
        "name": "tool_name",
        "args": [
            "name": "arg_value"
        ]
    }
}

No more text around the json.
You can call only one tool at once.

Note: all paths are relative to the working directory.
Never use absolute path.
Path must start with slash.
You can navigate to any file or a subdirectory in the working directory.
E.g.:

/foo/bar

Never try to leave the working directory. E.g.:

/../foo/bar

The following tools are available for you:

[
    {
        "name": "list_dir",
        "description": "lists files and directories inside the given directory.",
        "args": [
            {
                "name": "path"
                "description": "a path to the given directory"
            }
        ]
    },
    {
        "name": "read_file",
        "description": "reads the whole content of the file",
        "args": [
            {
                "name": "path",
                "description": "a path to the file"
            }
        ]
    },
    {
        "name": "write_file",
        "description": "writes the given content to a file. If the file exists it will be overwritten.",
        "args": [
            {
                "name": "path",
                "description": "a path to the file"
            },
            {
                "name": "content",
                "description": "a content of the file"
            }
        ]
    }
]
"""


def call_tool(tool_spec: dict) -> str:
    match tool_spec["name"]:
        case "listdir":
            return list_dir(path=tool_spec["args"]["path"])
        case "read_file":
            return read_file(path=tool_spec["args"]["path"])
        case "write_file":
            args = tool_spec["args"]
            return write_file(
                path=args["path"],
                content=args["content"]
            )


def list_dir(path: str) -> str:
    absolute_path = _resolve_path(path)
    print(f"listdir({absolute_path})")

    items = os.listdir(path=absolute_path)
    return "\n".join(items)


def read_file(path: str) -> str:
    absolute_path = _resolve_path(path)
    print(f"read_file({absolute_path})")

    with open(absolute_path, 'r', encoding=_ENCODING) as f:
        return f.read()


def write_file(path: str, content: str) -> str:
    absolute_path = _resolve_path(path)
    print(f"write_file({absolute_path})")

    with open(absolute_path, 'w', encoding=_ENCODING) as f:
        f.write(content)

    return ""


def _resolve_path(path: str):
    #TODO implement permission check
    absolute_path = os.path.curdir + path
    return absolute_path

