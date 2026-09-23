def repercent_broken_unicode(path):
    """
    As per section 3.2 of RFC 3987, step three of converting a URI into an IRI,
    repercent-encode any octet produced that is not part of a strictly legal
    UTF-8 octet sequence.
    """
    try:
        path.decode()
    except UnicodeDecodeError as e:
        repercent = quote(path[e.start:e.end], safe=b"/#%[]=:;$&()+,!?*@'~")
        path = repercent_broken_unicode(
            path[:e.start] + force_bytes(repercent) + path[e.end:])
    return path
