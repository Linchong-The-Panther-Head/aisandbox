"""
簡単なHTTPSサーバー。ローカルテスト用。
このサーバーはカレントディレクトリからHTTPSでファイルを配信します。
Simple HTTPS server for local testing that serves files from the current
directory.
"""
import argparse
import http.server
import ssl
import os
import json
import yaml
import threading
import mimetypes
import zipfile
import io

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

CONFIG = {}
CONFIG_PATH = None


def load_config(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def save_config(path: str, config: dict):
    with open(path, "w") as f:
        yaml.safe_dump(config, f)


class ConfigurableHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """設定されたディレクトリまたはZIPアーカイブからファイルを配信し、設定の表示と更新を行うハンドラー。"""

    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = CONFIG.get("resource_path", os.getcwd())
        self.resource_root = directory
        super().__init__(*args, directory=os.getcwd(), **kwargs)

    def update_paths(self):
        self.resource_root = CONFIG.get("resource_path", self.resource_root)

    def do_GET(self):
        if self.path == "/config":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(CONFIG).encode("utf-8"))
            return

        self._serve(head=False)

    def do_HEAD(self):
        if self.path == "/config":
            self.send_error(405, "Method Not Allowed")
            return
        self._serve(head=True)

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
                self.update_paths()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
            if restart:
                self.server.restart_after_shutdown = True
                threading.Thread(target=self.server.shutdown, daemon=True).start()
        else:
            super().do_POST()

    def _serve(self, head: bool):
        path = self.path.split('?')[0]
        if path in ('/README.md', '/README.ja.md'):
            file_path = os.path.join(REPO_ROOT, path.lstrip('/'))
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/markdown')
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                if not head:
                    self.wfile.write(data)
            else:
                self.send_error(404, 'File not found')
            return
        # コンテキストが指定されていない場合のデフォルト / default context
        if path == '/' or path == '':
            context = '__system'
            inner = 'index.html'
        else:
            parts = path.lstrip('/').split('/', 1)
            context = parts[0]
            inner = parts[1] if len(parts) > 1 else ''
            if inner == '' or inner.endswith('/'):
                inner += 'index.html'

        dir_path = os.path.join(self.resource_root, context)
        zip_path = os.path.join(self.resource_root, context + '.zip')
        if os.path.isdir(dir_path):
            prev_dir = self.directory
            prev_path = self.path
            self.directory = dir_path
            self.path = '/' + inner
            try:
                if head:
                    super().do_HEAD()
                else:
                    super().do_GET()
            finally:
                self.directory = prev_dir
                self.path = prev_path
        elif os.path.isfile(zip_path):
            try:
                with zipfile.ZipFile(zip_path) as zf:
                    data = zf.read(inner)
            except KeyError:
                self.send_error(404, "File not found")
                return
            ctype = mimetypes.guess_type(inner)[0] or 'application/octet-stream'
            self.send_response(200)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            if not head:
                self.wfile.write(data)
        else:
            self.send_error(404, "Not Found")


def run_server(config_path: str):
    """設定ファイルを読み込み、更新に応じてサーバーを再起動しながら起動する。
    Load the configuration file and restart the server when it changes.
    """

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
            *args, directory=resource_path, **kwargs)
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
    """コマンドライン引数を解析してサーバーを起動する。
    Parse command line arguments and start the server.
    """

    parser = argparse.ArgumentParser(description="シンプルHTTPSサーバー")
    parser.add_argument('-c', '--config', default='server_config.yaml', help='設定YAMLファイルへのパス')
    args = parser.parse_args()
    run_server(args.config)


if __name__ == '__main__':
    main()
