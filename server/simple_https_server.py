"""
簡単なHTTPSサーバー。ローカルテスト用。
このサーバーはカレントディレクトリからHTTPSでファイルを配信します。
"""
import argparse
import http.server
import ssl
import os
import json
import yaml
import threading

CONFIG = {}
CONFIG_PATH = None


def load_config(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def save_config(path: str, config: dict):
    with open(path, "w") as f:
        yaml.safe_dump(config, f)


class ConfigurableHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """設定されたディレクトリからファイルを配信し、設定の表示と更新を行うハンドラー。"""

    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = CONFIG.get("resource_path", os.getcwd())
        self.directory = directory
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        if self.path == "/config":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(CONFIG).encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/config":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length else b"{}"
            data = json.loads(body.decode("utf-8"))
            restart = data.pop("restart", False)
            CONFIG.update(data)
            if CONFIG_PATH:
                save_config(CONFIG_PATH, CONFIG)
            # 動的に変更可能な設定のみ即時反映
            if "resource_path" in data:
                self.directory = CONFIG.get("resource_path", self.directory)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
            if restart:
                self.server.restart_after_shutdown = True
                threading.Thread(target=self.server.shutdown, daemon=True).start()
        else:
            super().do_POST()


def run_server(config_path: str):
    """設定ファイルを読み込み、更新に応じてサーバーを再起動しながら起動する。"""

    global CONFIG, CONFIG_PATH
    CONFIG_PATH = config_path
    CONFIG = load_config(config_path)

    restart = True
    while restart:
        restart = False
        host = CONFIG.get('host', '0.0.0.0')
        port = int(CONFIG.get('port', 443))
        resource_path = CONFIG.get('resource_path', '.')
        certfile = CONFIG['certfile']
        keyfile = CONFIG.get('keyfile')

        handler_class = lambda *args, **kwargs: ConfigurableHTTPRequestHandler(
            *args, directory=CONFIG.get('resource_path', resource_path), **kwargs)
        httpd = http.server.HTTPServer((host, port), handler_class)
        httpd.restart_after_shutdown = False

        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

        print(f"Serving HTTPS on {host}:{port}, resources at {resource_path}")
        httpd.serve_forever()
        httpd.server_close()
        if getattr(httpd, "restart_after_shutdown", False):
            CONFIG = load_config(CONFIG_PATH)
            restart = True


def main():
    """コマンドライン引数を解析してサーバーを起動する。"""

    parser = argparse.ArgumentParser(description="シンプルHTTPSサーバー")
    parser.add_argument('-c', '--config', default='server_config.yaml', help='設定YAMLファイルへのパス')
    args = parser.parse_args()
    run_server(args.config)


if __name__ == '__main__':
    main()
