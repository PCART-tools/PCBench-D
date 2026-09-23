def register_option(key, defval, doc='', validator=None, cb=None):
    """Register an option in the package-wide pandas config object

    Parameters
    ----------
    key       - a fully-qualified key, e.g. "x.y.option - z".
    defval    - the default value of the option
    doc       - a string description of the option
    validator - a function of a single argument, should raise `ValueError` if
                called with a value which is not a legal value for the option.
    cb        - a function of a single argument "key", which is called
                immediately after an option value is set/reset. key is
                the full name of the option.

    Returns
    -------
    Nothing.

    Raises
    ------
    ValueError if `validator` is specified and `defval` is not a valid value.

    """
    import tokenize
    import keyword
    key = key.lower()

    if key in _registered_options:
        raise OptionError("Option '%s' has already been registered" % key)
    if key in _reserved_keys:
        raise OptionError("Option '%s' is a reserved key" % key)

    # the default value should be legal
    if validator:
        validator(defval)

    # walk the nested dict, creating dicts as needed along the path
    path = key.split('.')

    for k in path:
        if not bool(re.match('^' + tokenize.Name + '$', k)):
            raise ValueError("%s is not a valid identifier" % k)
        if keyword.iskeyword(k):
            raise ValueError("%s is a python keyword" % k)

    cursor = _global_config
    for i, p in enumerate(path[:-1]):
        if not isinstance(cursor, dict):
            raise OptionError("Path prefix to option '%s' is already an option"
                              % '.'.join(path[:i]))
        if p not in cursor:
            cursor[p] = {}
        cursor = cursor[p]

    if not isinstance(cursor, dict):
        raise OptionError("Path prefix to option '%s' is already an option" %
                          '.'.join(path[:-1]))

    cursor[path[-1]] = defval  # initialize

    # save the option metadata
    _registered_options[key] = RegisteredOption(key=key, defval=defval,
                                                doc=doc, validator=validator,
                                                cb=cb)
