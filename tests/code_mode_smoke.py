#!/usr/bin/env python3
"""Exercise a release binary's code-mode exec against a local mock model."""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import threading


def events(response_id, item):
    result = [
        {"type": "response.created", "response": {"id": response_id}},
        {"type": "response.output_item.done", "item": item},
        {"type": "response.completed", "response": {
            "id": response_id,
            "usage": {"input_tokens": 0, "input_tokens_details": None,
                      "output_tokens": 0, "output_tokens_details": None, "total_tokens": 0},
        }},
    ]
    return "".join(f"event: {event['type']}\ndata: {json.dumps(event)}\n\n" for event in result).encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bin", type=Path, required=True)
    parser.add_argument("--cwd", type=Path, required=True)
    args = parser.parse_args()
    # Preserve the public symlink: resolving it here would miss regressions in
    # Codex's companion lookup when consumers launch the installed entrypoint.
    binary = args.bin.absolute()
    cwd = args.cwd.resolve()
    if not binary.is_file() or not cwd.is_dir():
        parser.error("--bin must be a file and --cwd must be a directory")

    requests = []
    with tempfile.NamedTemporaryFile(mode="w", prefix=".codexnk-smoke-", dir=cwd) as fixture:
        fixture.write("codexnk-runtime-smoke\n")
        fixture.flush()
        command = f"pwd; printf 'files='; ls -A | wc -l; cat -- {shlex.quote(Path(fixture.name).name)}"
        script = f"text((await tools.exec_command({{cmd: {json.dumps(command)}, login: false}})).output);"

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                length = int(self.headers["Content-Length"])
                body = json.loads(self.rfile.read(length))
                requests.append(body)
                if self.path != "/v1/responses" or len(requests) > 2:
                    self.send_error(400)
                    return
                if len(requests) == 1:
                    item = {"type": "custom_tool_call", "call_id": "smoke-exec",
                            "name": "exec", "input": script}
                else:
                    item = {"type": "message", "role": "assistant", "id": "done",
                            "content": [{"type": "output_text", "text": "Smoke complete"}]}
                payload = events(f"smoke-{len(requests)}", item)
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, *_args):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory(prefix="codexnk-smoke-") as home:
                config = f'''
model = "mock-model"
model_provider = "smoke"
approval_policy = "never"
sandbox_mode = "read-only"
[features]
code_mode = true
code_mode_only = true
[model_providers.smoke]
name = "Local smoke model"
base_url = "http://127.0.0.1:{server.server_port}/v1"
wire_api = "responses"
request_max_retries = 0
stream_max_retries = 0
'''
                (Path(home) / "config.toml").write_text(config)
                env = {**os.environ, "CODEX_HOME": home, "OPENAI_API_KEY": "local-smoke-only"}
                result = subprocess.run(
                    [str(binary), "exec", "--json", "--ephemeral", "--skip-git-repo-check",
                     "-C", str(cwd), "Read and count the files in this directory."],
                    env=env, text=True, capture_output=True, timeout=120,
                )
        finally:
            server.shutdown()
            thread.join(timeout=5)
            server.server_close()

        if result.returncode != 0:
            raise RuntimeError(f"codex exec failed ({result.returncode}):\n{result.stderr}\n{result.stdout}")
        if len(requests) != 2:
            raise RuntimeError(f"expected code-mode tool result and final response, got {len(requests)} requests")
        returned = json.dumps(requests[1])
        if "smoke-exec" not in returned or str(cwd) not in returned or "codexnk-runtime-smoke" not in returned or "files=" not in returned:
            raise RuntimeError(f"model did not receive Bot-cwd file count and contents: {returned}")
        print(f"Code-mode exec read and counted files in {cwd} using {binary}")


if __name__ == "__main__":
    main()
