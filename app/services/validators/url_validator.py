import ipaddress
import socket
from urllib.parse import urlparse

from app.core.errors import ApiError


PRIVATE_HOSTNAMES = {"localhost", "127.0.0.1", "::1"}



def _is_disallowed_ip(ip: str) -> bool:
    addr = ipaddress.ip_address(ip)
    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_multicast
        or addr.is_reserved
        or addr.is_unspecified
    )



def validate_public_http_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise ApiError(422, "INVALID_JOB_URL", "Job URL must use http or https.")

    if not parsed.hostname:
        raise ApiError(422, "INVALID_JOB_URL", "Job URL must include a hostname.")

    host = parsed.hostname.lower()
    if host in PRIVATE_HOSTNAMES or host.endswith(".local"):
        raise ApiError(422, "INVALID_JOB_URL", "Private or local hosts are not allowed.")

    try:
        addr_infos = socket.getaddrinfo(host, parsed.port or 80)
    except socket.gaierror:
        raise ApiError(422, "INVALID_JOB_URL", "Unable to resolve host for job URL.") from None

    for info in addr_infos:
        ip = info[4][0]
        if _is_disallowed_ip(ip):
            raise ApiError(422, "INVALID_JOB_URL", "Private or internal network addresses are blocked.")

    return url.strip()
