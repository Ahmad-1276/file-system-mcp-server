# File System MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io) server that gives AI agents safe, structured tools for working with the local file system: browsing directories, reading and writing text, searching file names and contents, inspecting metadata, and organizing files into collections.

Built with **FastMCP** and **Pydantic**, it works with any MCP client — Claude Desktop, Cursor, VS Code, or your own agent.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-000000)
![FastMCP](https://img.shields.io/badge/FastMCP-2.x-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- **16 tools** covering the file-system operations agents actually need
- **Cross-platform** — Windows, macOS, and Linux
- **Structured results** — every tool returns typed JSON with `success`/`error` fields
- **Safe defaults** — recursive search depth limits, file-type filters, and result caps
- **Collections** — group related files into named collections for later retrieval
- **Optional GitHub agent** — a LangChain + Groq demo agent that uses GitHub tools

## Tools

| Tool | Description |
| --- | --- |
| `scan_directory_tool` | Scan a directory, optionally recursive, filtered by file type |
| `get_file_metadata_tool` | Size, timestamps, MIME type, and permissions for a file |
| `list_drives` | List available drives (Windows) |
| `create_collection` | Create a named collection from a list of file paths |
| `list_user_directories` | Common user folders (Desktop, Documents, Downloads, …) |
| `read_text_file_tool` | Read a text file, optionally limited to the first N lines |
| `write_text_file_tool` | Write or append text to a file |
| `search_files_tool` | Search for files by name |
| `search_file_contents_tool` | Search inside file contents (grep-style), capped results |
| `get_system_info` | OS, Python version, and runtime information |
| `copy_file` | Copy a file, with optional overwrite |
| `move_file` | Move or rename a file, with optional overwrite |
| `delete_file` | Delete a file |
| `create_directory` | Create a directory, including parents |
| `list_directory` | List the direct contents of a directory |
| `list_directory_recursively` | Return a nested directory tree |

## Requirements

- Python 3.10+
- `pip install -r requirements.txt`

## Installation

```bash
git clone https://github.com/Ahmad-1276/file-system-mcp-server.git
cd file-system-mcp-server

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Running the server

```bash
python fs_server.py
```

The server communicates over **stdio**, which is what MCP clients expect. It prints startup information to stderr/stdout and then waits for a client.

To try the bundled demo instead:

```bash
python demo_fs_fixed.py
```

Or use the interactive launcher:

```bash
python start.py
```

## Connecting an MCP client

### Claude Desktop

Add this to `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/`, Windows: `%APPDATA%\Claude\`):

```json
{
  "mcpServers": {
    "file-system": {
      "command": "python",
      "args": ["/absolute/path/to/file-system-mcp-server/fs_server.py"]
    }
  }
}
```

Use the absolute path to the Python interpreter inside your virtual environment if `python` is not on `PATH`.

### Cursor / VS Code

Add the same `mcpServers` block to your MCP settings file (`.cursor/mcp.json` for Cursor, or the MCP section in VS Code settings).

### Other clients

Any client that supports stdio MCP servers can launch `python fs_server.py` and speak the protocol over stdin/stdout.

## Project structure

```
.
├── fs_server.py             # MCP server and all 16 tools
├── demo_fs_fixed.py         # Script that exercises the tools directly
├── github_agent_updated.py  # Optional LangChain + Groq GitHub agent
├── start.py                 # Interactive launcher
├── windows_utils.py         # Windows-specific helpers
├── requirements.txt
└── .env.example
```

## Optional GitHub agent

`github_agent_updated.py` is a separate demo that combines a Groq-hosted LLM with the GitHub API. It needs two environment variables:

```bash
cp .env.example .env
# edit .env:
# GROQ_API_KEY=gsk_...
# GITHUB_TOKEN=ghp_...
```

Then run:

```bash
python github_agent_updated.py
```

The file-system server itself does **not** require any API keys.

## Data and collections

Collections are stored under `data/collections/` inside the project directory. The directory is created automatically on first run and is ignored by Git.

## Security notes

This server exposes write, move, and delete operations to whatever client connects to it. Only connect it to agents you trust, and consider running it in a sandbox or container when working with sensitive files.

## License

MIT — see [LICENSE](LICENSE).
