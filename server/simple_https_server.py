#!/usr/bin/env python3
"""
簡単なHTTPSサーバー。ローカルテスト用。
このサーバーはカレントディレクトリからHTTPSでファイルを配信します。
"""

import http.server
import ssl


def run(server_class=http.server.HTTPServer,
        handler_class=http.server.SimpleHTTPRequestHandler):
    """Start the HTTPS server."""
    server_address = ('', 4443)
    httpd = server_class(server_address, handler_class)
    # Create or specify a certificate "server.pem" for real use
    httpd.socket = ssl.wrap_socket(
        httpd.socket, certfile='server.pem', server_side=True)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
