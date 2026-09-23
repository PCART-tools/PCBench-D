def _StringifyName(name, expected_type):
    if isinstance(name, basestring):
        return name
    assert type(name).__name__ == expected_type, \
        "Expected a string or %s" % expected_type
    return str(name)
