def deprecate_option(key, msg=None, rkey=None, removal_ver=None):
    """
    Mark option `key` as deprecated, if code attempts to access this option,
    a warning will be produced, using `msg` if given, or a default message
    if not.
    if `rkey` is given, any access to the key will be re-routed to `rkey`.

    Neither the existence of `key` nor that if `rkey` is checked. If they
    do not exist, any subsequence access will fail as usual, after the
    deprecation warning is given.

    Parameters
    ----------
    key - the name of the option to be deprecated. must be a fully-qualified
          option name (e.g "x.y.z.rkey").

    msg - (Optional) a warning message to output when the key is referenced.
          if no message is given a default message will be emitted.

    rkey - (Optional) the name of an option to reroute access to.
           If specified, any referenced `key` will be re-routed to `rkey`
           including set/get/reset.
           rkey must be a fully-qualified option name (e.g "x.y.z.rkey").
           used by the default message if no `msg` is specified.

    removal_ver - (Optional) specifies the version in which this option will
                  be removed. used by the default message if no `msg`
                  is specified.

    Returns
    -------
    Nothing

    Raises
    ------
    OptionError - if key has already been deprecated.

    """

    key = key.lower()

    if key in _deprecated_options:
        raise OptionError("Option '%s' has already been defined as deprecated."
                          % key)

    _deprecated_options[key] = DeprecatedOption(key, msg, rkey, removal_ver)
