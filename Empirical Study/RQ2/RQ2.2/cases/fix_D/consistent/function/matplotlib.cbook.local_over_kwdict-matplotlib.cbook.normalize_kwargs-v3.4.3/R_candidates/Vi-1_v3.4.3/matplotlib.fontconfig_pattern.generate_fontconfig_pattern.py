def generate_fontconfig_pattern(d):
    """
    Given a dictionary of key/value pairs, generates a fontconfig
    pattern string.
    """
    props = []

    # Family is added first w/o a keyword
    family = d.get_family()
    if family is not None and family != []:
        props.append(_escape_val(family, family_escape))

    # The other keys are added as key=value
    for key in ['style', 'variant', 'weight', 'stretch', 'file', 'size']:
        val = getattr(d, 'get_' + key)()
        # Don't use 'if not val' because 0 is a valid input.
        if val is not None and val != []:
            props.append(":%s=%s" % (key, _escape_val(val, value_escape)))

    return ''.join(props)
