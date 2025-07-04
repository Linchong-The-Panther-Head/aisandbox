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

3. Place folders or zip archives in the directory specified by `resource_path`.
   Each folder name becomes a context path. If a zip file is found, its filename
   (without `.zip`) is used as the context path and the contents are served
directly. Built-in pages live under `server/resources/__system` and a simple
sample application lives in `server/resources/__sample`.

### Running

Start the server with:

```bash
python server/simple_https_server.py -c server/server_config.yaml
```

The server will listen on the configured host and port using HTTPS.
You can also view this README in your browser at `https://<host>:<port>/__system/readme.html`.

### Editing Configuration via Browser

Navigate to `https://<host>:<port>/__system/config.html` while the server is running. This
page shows the contents of `server_config.yaml` and allows you to update values.
Changes to `resource_path` are applied immediately. After saving, the server
gracefully restarts so that all other fields take effect without further
interaction. The restart is triggered only from this page. Each field is
validated when you leave it and errors are shown in Japanese. The submit button
remains disabled until all fields are valid. Full-width digits are converted to
half-width before validation. Hover the **?** icons next to each field to see a
short description and example value in the current language.

Both the index page and the configuration editor include a language toggle at
the top-right corner. Click **日本語** or **English** to switch all labels and
messages between Japanese and English. Your choice is stored locally so the
language persists across pages without using cookies.

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
  Place subfolders or zip files here. Each folder name or zip filename becomes
  a context path such as `/__sample` or `/app1`.
