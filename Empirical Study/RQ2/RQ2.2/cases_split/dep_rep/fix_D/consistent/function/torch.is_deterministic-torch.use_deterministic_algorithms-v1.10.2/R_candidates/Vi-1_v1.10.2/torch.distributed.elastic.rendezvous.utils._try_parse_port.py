def _try_parse_port(port_str: str) -> Optional[int]:
    """Tries to extract the port number from ``port_str``."""
    if port_str and re.match(r"^[0-9]{1,5}$", port_str):
        return int(port_str)
    return None
