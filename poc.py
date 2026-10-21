
#!/usr/bin/env python3
"""
PHP2Shell Response Inspector
HTTP/HTTPS response inspection for authorized security research.

This script sends a normal GET request. It does not exploit or
confirm CVE-2026-109618 or CVE-2026-109619.
"""

import argparse
import http.client
import ssl
import sys


def inspect_response(host, port, path, use_https, output_file=None):
    connection_class = (
        http.client.HTTPSConnection
        if use_https
        else http.client.HTTPConnection
    )

    kwargs = {"timeout": 10}

    if use_https:
        kwargs["context"] = ssl.create_default_context()

    conn = connection_class(host, port=port, **kwargs)

    try:
        if not path.startswith("/"):
            path = "/" + path

        print(f"[*] Target: {host}:{port}")
        print(f"[*] Path:   {path}")
        print(f"[*] Scheme: {'https' if use_https else 'http'}")
        print("[*] Sending GET request...\n")

        conn.request(
            "GET",
            path,
            headers={
                "User-Agent": "PHP2Shell-Response-Inspector/1.0",
                "Accept": "*/*",
                "Connection": "close",
            },
        )

        response = conn.getresponse()

        # Read at most 3000 bytes for the displayed/saved preview.
        body = response.read(3000)

        print(f"[+] Status:       {response.status} {response.reason}")
        print(
            f"[+] Content-Type: "
            f"{response.getheader('Content-Type', 'Not provided')}"
        )
        print(
            f"[+] Server:       "
            f"{response.getheader('Server', 'Not provided')}"
        )
        print(f"[+] Preview size: {len(body)} bytes")

        print("\n--- Response Body Preview ---")
        print(body.decode("utf-8", errors="replace"))
        print("--- End Preview ---")

        if output_file:
            with open(output_file, "wb") as file:
                file.write(body)

            print(f"\n[+] Preview saved locally to: {output_file}")

        print(
            "\n[!] An HTTP response alone does not establish "
            "whether a PHP vulnerability is present."
        )

    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Inspect HTTP/HTTPS responses for authorized "
            "PHP2Shell-related security research."
        ),
        epilog=(
            "Use only against systems you own or are authorized "
            "to test. This is not a vulnerability detector."
        ),
    )

    parser.add_argument(
        "--host",
        required=True,
        help="Target hostname or IP address",
    )

    parser.add_argument(
        "--port",
        type=int,
        help="Target port (default: 443 for HTTPS, 80 for HTTP)",
    )

    parser.add_argument(
        "--path",
        default="/",
        help="Request path, e.g. /whatever.php (default: /)",
    )

    parser.add_argument(
        "--http",
        action="store_true",
        help="Use plain HTTP instead of HTTPS",
    )

    parser.add_argument(
        "--output",
        help="Optional local file to save the response preview",
    )

    args = parser.parse_args()

    if not 1 <= (args.port or (80 if args.http else 443)) <= 65535:
        parser.error("Port must be between 1 and 65535")

    if not args.host.strip():
        parser.error("Host cannot be empty")

    if not args.path.startswith("/"):
        args.path = "/" + args.path

    port = args.port or (80 if args.http else 443)

    try:
        inspect_response(
            host=args.host,
            port=port,
            path=args.path,
            use_https=not args.http,
            output_file=args.output,
        )
    except (OSError, http.client.HTTPException, ValueError) as exc:
        print(f"\n[-] Request failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
