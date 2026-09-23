def fn_var_getattr(tx, fn, source, name):
    source = source and AttrSource(source, name)
    try:
        subobj = inspect.getattr_static(fn, name)
    except AttributeError:
        # function does not have a __getattr__ or __getattribute__ method,
        # so we can safely assume that this attribute is absent
        raise_observed_exception(AttributeError, tx)

    # Special handling for known dunder attributes
    if name in fn_known_dunder_attrs:
        subobj = getattr(fn, name)
    if source:
        return variables.LazyVariableTracker.create(subobj, source)
    return VariableTracker.build(tx, subobj)
