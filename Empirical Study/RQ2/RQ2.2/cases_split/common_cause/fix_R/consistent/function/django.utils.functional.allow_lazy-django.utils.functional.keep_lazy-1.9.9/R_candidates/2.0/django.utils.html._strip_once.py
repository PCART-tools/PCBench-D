def _strip_once(value):
    """
    Internal tag stripping utility used by strip_tags.
    """
    s = MLStripper()
    try:
        s.feed(value)
    except HTMLParseError:
        return value
    try:
        s.close()
    except HTMLParseError:
        return s.get_data() + s.rawdata
    else:
        return s.get_data()
