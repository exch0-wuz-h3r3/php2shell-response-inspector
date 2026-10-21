
# PHP2Shell Response Inspector

A lightweight Python HTTP/HTTPS response inspection tool for authorized security research related to PHP2Shell — **CVE-2026-109618** and **CVE-2026-109619**.

Inspect HTTP status codes, response headers, and response body previews from a specified web server using a configurable hostname, port, and request path.

> **Disclaimer:** This tool is a basic HTTP response inspector. It does not exploit PHP2Shell, execute remote code, or independently determine whether a target is vulnerable to either CVE.

## Overview

PHP2Shell refers to two critical PHP vulnerabilities that can allow unauthenticated remote code execution in affected PHP deployments.

This project provides a simple way to inspect HTTP/HTTPS responses from authorized test environments while conducting web security research.

### Features

- Supports HTTP and HTTPS connections.
- Configurable target hostname or IP address.
- Configurable destination port.
- Custom request paths, including `.php` endpoints.
- Displays HTTP status code and reason.
- Displays the response `Content-Type`.
- Prints a response body preview.
- Optionally saves the response preview to a local file.
- Uses Python's standard library; no third-party dependencies required.

## Related vulnerabilities

| CVE | Description |
|---|---|
| CVE-2026-109618 | Critical PHP vulnerability associated with remote code execution |
| CVE-2026-109619 | Critical PHP vulnerability associated with remote code execution |

Both vulnerabilities received a CVSS v4.0 score of 9.2. Consult the official PHP advisory for technical details, affected releases, and remediation guidance.

## Requirements

- Python 3.8 or later
- Network connectivity to the authorized target
- Permission to test the specified host and endpoint

No additional Python packages are required.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/php2shell-response-inspector.git
cd php2shell-response-inspector
```

Replace `YOUR-USERNAME` with your GitHub username.

## Usage

### Basic HTTPS request

```bash
python poc.py --host example.com
```

By default, the tool connects over HTTPS on port 443 and requests `/`.

### Specify a port and PHP endpoint

```bash
python poc.py --host example.com --port 443 --path /whatever.php
```

### Test a local development environment

```bash
python poc.py --host 127.0.0.1 --port 8443 --path /test.php
```

This example uses HTTPS. The service must support TLS on the specified port.

### Use HTTP instead of HTTPS

```bash
python poc.py --host 127.0.0.1 --port 8080 --path /test.php --http
```

Plain HTTP is unencrypted. Use it only where appropriate, such as a local test environment.

### Save the response preview

```bash
python poc.py --host example.com --path /whatever.php --output response.bin
```

The output file contains the first 3,000 bytes of the response body. It is saved locally and is not a request to download a remote filesystem file.

## Example output

The following is illustrative output from a normal HTTP response:

```text
Host: example.com
Port: 443
Path: /whatever.php
Status: 200 OK
Content-Type: text/html

Body preview:
<!doctype html>
<html>
...
```

Actual output depends on the server response.

## Project structure

```text
php2shell-response-inspector/
├── poc.py
├── README.md
├── LICENSE
└── .gitignore
```

- `poc.py` — HTTP/HTTPS response inspection script.
- `README.md` — documentation and usage examples.
- `LICENSE` — project license.
- `.gitignore` — excludes temporary Python files and virtual environments.

## Limitations

This project performs a standard HTTP GET request. It does not:

- Send PHP2Shell exploit payloads.
- Execute commands on the remote server.
- Read arbitrary files from the remote filesystem.
- Confirm the PHP version or runtime configuration behind a response.
- Determine whether CVE-2026-109618 or CVE-2026-109619 is exploitable.
- Guarantee that an HTTP error indicates a vulnerability.

A `200 OK` response does not establish that the server uses PHP, and a `403`, `404`, or `500` response does not independently prove vulnerability.

## Security and responsible use

Use this tool only against systems you own or have explicit authorization to assess.

- Respect the scope and rules of any penetration test or bug bounty program.
- Avoid testing third-party systems without permission.
- Do not treat response status codes or body content as definitive vulnerability evidence.
- Do not publish sensitive information collected during authorized testing.
- Follow responsible disclosure procedures when reporting security findings.

## Remediation

If you administer a PHP deployment, identify the actual PHP runtime serving web traffic and apply the relevant security update.

The PHP project lists these fixed releases:

- PHP 8.5.12
- PHP 8.4.27
- PHP 8.3.36
- PHP 8.2.35

For older branches, consult your operating system or vendor for supported security backports. Updating the PHP runtime is the recommended remediation.

## References

- [Official PHP security advisories](https://www.php.net/archive/2026.php)
- [PHP source security advisory](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp)
- [UK National Cyber Security Centre guidance](https://www.ncsc.gov.uk/news/critical-security-issue-affecting-php)
- [Dutch NCSC PHP2Shell tracking repository](https://github.com/NCSC-NL/php2shell)

## License

Distributed under the MIT License if the repository includes an MIT `LICENSE` file. See that file for the applicable terms.



![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Purpose](https://img.shields.io/badge/Purpose-Security%20Research-orange)
