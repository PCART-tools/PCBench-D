def smart_urlquote(url):
    """Quote a URL if it isn't already quoted."""
    def unquote_quote(segment):
        segment = unquote(segment)
        # Tilde is part of RFC3986 Unreserved Characters
        # http://tools.ietf.org/html/rfc3986#section-2.3
        # See also http://bugs.python.org/issue16285
        segment = quote(segment, safe=RFC3986_SUBDELIMS + RFC3986_GENDELIMS + '~')
        return force_text(segment)

    # Handle IDN before quoting.
    try:
        scheme, netloc, path, query, fragment = urlsplit(url)
    except ValueError:
        # invalid IPv6 URL (normally square brackets in hostname part).
        return unquote_quote(url)

    try:
        netloc = netloc.encode('idna').decode('ascii')  # IDN -> ACE
    except UnicodeError:  # invalid domain part
        return unquote_quote(url)

    if query:
        # Separately unquoting key/value, so as to not mix querystring separators
        # included in query values. See #22267.
        query_parts = [(unquote(q[0]), unquote(q[1]))
                       for q in parse_qsl(query, keep_blank_values=True)]
        # urlencode will take care of quoting
        query = urlencode(query_parts)

    path = unquote_quote(path)
    fragment = unquote_quote(fragment)

    return urlunsplit((scheme, netloc, path, query, fragment))
