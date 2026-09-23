def escape_uri_path(path):
    """
    Escape the unsafe characters from the path portion of a Uniform Resource
    Identifier (URI).
    """
    # These are the "reserved" and "unreserved" characters specified in
    # sections 2.2 and 2.3 of RFC 2396:
    #   reserved    = ";" | "/" | "?" | ":" | "@" | "&" | "=" | "+" | "$" | ","
    #   unreserved  = alphanum | mark
    #   mark        = "-" | "_" | "." | "!" | "~" | "*" | "'" | "(" | ")"
    # The list of safe characters here is constructed subtracting ";", "=",
    # and "?" according to section 3.3 of RFC 2396.
    # The reason for not subtracting and escaping "/" is that we are escaping
    # the entire path, not a path segment.
    return quote(path, safe="/:@&+$,-_.!~*'()")
