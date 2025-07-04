# aisandbox
Sandbox for Codex

## Simple HTTPS Server

This repository includes a lightweight RFC 7231 compliant HTTPS web server implemented in Python.

### Setup

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Generate or provide a certificate and key. Update `server/server_config.yaml` with paths to your certificate (`certfile`) and key (`keyfile`).

3. Place HTML or other resources in the directory specified by `resource_path`.
   Sample HTML5, CSS3 and JavaScript files are provided under `server/html`.

### Running

Start the server with:

```bash
python server/simple_https_server.py -c server/server_config.yaml
```

The server will listen on the configured host and port using HTTPS.

### Generating a Self-Signed Certificate (optional)

You can generate a self-signed certificate for testing with the following command:

```bash
openssl req -x509 -newkey rsa:4096 -keyout server/key.pem -out server/cert.pem -days 365 -nodes -subj "/CN=example.com"
```

### Configuration Fields

- `host`: Address to bind the server to.
- `port`: Port to listen on (default 443 for HTTPS).
- `domain`: Domain name for reference.
- `certfile`: Path to the TLS certificate.
- `keyfile`: Path to the private key for the certificate.
- `resource_path`: Directory containing static resources to serve.
