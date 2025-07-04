"""
簡単なHTTPSサーバー。ローカルテスト用。
このサーバーはカレントディレクトリからHTTPSでファイルを配信します。
"""
import argparse
import http.server
import ssl
import os
import yaml

class ConfigurableHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """設定されたディレクトリからファイルを配信するハンドラー。"""

    def __init__(self, *args, directory=None, **kwargs):
        """リソースディレクトリを指定してハンドラーを初期化する。"""

        if directory is None:
            directory = os.getcwd()
        self.directory = directory
        super().__init__(*args, directory=directory, **kwargs)


def run_server(config_path: str):
    """設定ファイルを読み込みHTTPSサーバーを起動する。"""

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    host = config.get('host', '0.0.0.0')
    port = int(config.get('port', 443))
    resource_path = config.get('resource_path', '.')
    certfile = config['certfile']
    keyfile = config.get('keyfile')

    handler_class = lambda *args, **kwargs: ConfigurableHTTPRequestHandler(*args, directory=resource_path, **kwargs)
    httpd = http.server.HTTPServer((host, port), handler_class)

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

    print(f"Serving HTTPS on {host}:{port}, resources at {resource_path}")
    httpd.serve_forever()


def main():
    """コマンドライン引数を解析してサーバーを起動する。"""

    parser = argparse.ArgumentParser(description="シンプルHTTPSサーバー")
    parser.add_argument('-c', '--config', default='server_config.yaml', help='設定YAMLファイルへのパス')
    args = parser.parse_args()
    run_server(args.config)


if __name__ == '__main__':
    main()
