@_api.deprecated("3.3")
def validate_webagg_address(s):
    if s is not None:
        import socket
        try:
            socket.inet_aton(s)
        except socket.error as e:
            raise ValueError(
                "'webagg.address' is not a valid IP address") from e
        return s
    raise ValueError("'webagg.address' is not a valid IP address")
