def _matches_machine_hostname(host: str) -> bool:
    """Indicates whether ``host`` matches the hostname of this machine.

    This function compares ``host`` to the hostname as well as to the IP
    addresses of this machine. Note that it may return a false negative if this
    machine has CNAME records beyond its FQDN or IP addresses assigned to
    secondary NICs.
    """
    if host == "localhost":
        return True

    try:
        addr = ipaddress.ip_address(host)
    except ValueError:
        addr = None

    if addr and addr.is_loopback:
        return True

    this_host = socket.gethostname()
    if host == this_host:
        return True

    addr_list = socket.getaddrinfo(
        this_host, None, proto=socket.IPPROTO_TCP, flags=socket.AI_CANONNAME
    )
    for addr_info in addr_list:
        # If we have an FQDN in the addr_info, compare it to `host`.
        if addr_info[3] and addr_info[3] == host:
            return True
        # Otherwise if `host` represents an IP address, compare it to our IP
        # address.
        if addr and addr_info[4][0] == str(addr):
            return True

    return False
