"""Shell tool: Bash."""

from __future__ import annotations

import subprocess

from tools import tool


@tool(
    name="Bash",
    description="Execute a shell command and return its output. "
                "Use this to run scripts, compilers, tests, or any CLI tool. "
                "Default timeout is 600 seconds (10 minutes). "
                "Interactive commands are not supported.",
    parameters={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The shell command to execute",
            },
            "timeout": {
                "type": "integer",
                "description": "Timeout in seconds (default: 600, max: 3600)",
            },
        },
        "required": ["command"],
    },
)
def bash(command: str, timeout: int = 600) -> str:
    # Clamp timeout to max 3600 seconds (1 hour)
    timeout_seconds = min(max(timeout, 1), 3600)
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        output = []
        if result.stdout:
            output.append(result.stdout.strip())
        if result.stderr:
            output.append(f"[stderr]\n{result.stderr.strip()}")
        if result.returncode != 0:
            output.insert(0, f"Exit code: {result.returncode}")
        return "\n".join(output) if output else f"(completed with no output, exit code {result.returncode})"
    except subprocess.TimeoutExpired:
        return f"[Error] Command timed out after {timeout_seconds}s"
    except Exception as e:
        return f"[Error] {e}"


__all__ = ["bash"]