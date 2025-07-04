import argparse
import http.server
import ssl
import os
import yaml

class ConfigurableHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler that serves files from a configured directory."""

    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = directory
        super().__init__(*args, directory=directory, **kwargs)


def run_server(config_path: str):
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
    parser = argparse.ArgumentParser(description="Simple HTTPS server")
    parser.add_argument('-c', '--config', default='server_config.yaml', help='Path to configuration YAML file')
    args = parser.parse_args()
    run_server(args.config)


if __name__ == '__main__':
    main()
