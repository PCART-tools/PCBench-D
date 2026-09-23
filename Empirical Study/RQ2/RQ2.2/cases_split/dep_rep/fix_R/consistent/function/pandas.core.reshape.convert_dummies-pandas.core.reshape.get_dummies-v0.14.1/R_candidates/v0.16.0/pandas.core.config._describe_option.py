def _describe_option(pat='', _print_desc=True):

    keys = _select_options(pat)
    if len(keys) == 0:
        raise OptionError('No such keys(s)')

    s = u('')
    for k in keys:  # filter by pat
        s += _build_option_description(k)

    if _print_desc:
        print(s)
    else:
        return s
