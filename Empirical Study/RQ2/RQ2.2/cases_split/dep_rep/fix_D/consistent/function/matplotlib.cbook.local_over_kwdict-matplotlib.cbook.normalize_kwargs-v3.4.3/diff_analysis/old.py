@_api.delete_parameter("3.3", "required")
@_api.delete_parameter("3.3", "forbidden")
@_api.delete_parameter("3.3", "allowed")
def normalize_kwargs(kw, alias_mapping=None, required=(), forbidden=(),
                     allowed=None):
    """
    Helper function to normalize kwarg inputs.

    The order they are resolved are:

    1. aliasing
    2. required
    3. forbidden
    4. allowed

    This order means that only the canonical names need appear in
    *allowed*, *forbidden*, *required*.

    Parameters
    ----------
    kw : dict or None
        A dict of keyword arguments.  None is explicitly supported and treated
        as an empty dict, to support functions with an optional parameter of
        the form ``props=None``.

    alias_mapping : dict or Artist subclass or Artist instance, optional
        A mapping between a canonical name to a list of
        aliases, in order of precedence from lowest to highest.

        If the canonical value is not in the list it is assumed to have
        the highest priority.

        If an Artist subclass or instance is passed, use its properties alias
        mapping.

    required : list of str, optional
        A list of keys that must be in *kws*.  This parameter is deprecated.

    forbidden : list of str, optional
        A list of keys which may not be in *kw*.  This parameter is deprecated.

    allowed : list of str, optional
        A list of allowed fields.  If this not None, then raise if
        *kw* contains any keys not in the union of *required*
        and *allowed*.  To allow only the required fields pass in
        an empty tuple ``allowed=()``.  This parameter is deprecated.

    Raises
    ------
    TypeError
        To match what python raises if invalid args/kwargs are passed to
        a callable.
    """
    from matplotlib.artist import Artist

    if kw is None:
        return {}

    # deal with default value of alias_mapping
    if alias_mapping is None:
        alias_mapping = dict()
    elif (isinstance(alias_mapping, type) and issubclass(alias_mapping, Artist)
          or isinstance(alias_mapping, Artist)):
        alias_mapping = getattr(alias_mapping, "_alias_map", {})

    to_canonical = {alias: canonical
                    for canonical, alias_list in alias_mapping.items()
                    for alias in alias_list}
    canonical_to_seen = {}
    ret = {}  # output dictionary

    for k, v in kw.items():
        canonical = to_canonical.get(k, k)
        if canonical in canonical_to_seen:
            raise TypeError(f"Got both {canonical_to_seen[canonical]!r} and "
                            f"{k!r}, which are aliases of one another")
        canonical_to_seen[canonical] = k
        ret[canonical] = v

    fail_keys = [k for k in required if k not in ret]
    if fail_keys:
        raise TypeError("The required keys {keys!r} "
                        "are not in kwargs".format(keys=fail_keys))

    fail_keys = [k for k in forbidden if k in ret]
    if fail_keys:
        raise TypeError("The forbidden keys {keys!r} "
                        "are in kwargs".format(keys=fail_keys))

    if allowed is not None:
        allowed_set = {*required, *allowed}
        fail_keys = [k for k in ret if k not in allowed_set]
        if fail_keys:
            raise TypeError(
                "kwargs contains {keys!r} which are not in the required "
                "{req!r} or allowed {allow!r} keys".format(
                    keys=fail_keys, req=required, allow=allowed))

    return ret
