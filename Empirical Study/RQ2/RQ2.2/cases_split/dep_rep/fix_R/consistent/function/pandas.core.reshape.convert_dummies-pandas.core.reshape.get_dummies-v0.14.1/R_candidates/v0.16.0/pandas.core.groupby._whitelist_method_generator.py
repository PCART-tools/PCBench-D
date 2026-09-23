def _whitelist_method_generator(klass, whitelist) :
    """
    Yields all GroupBy member defs for DataFrame/Series names in _whitelist.

    Parameters
    ----------
    klass - class where members are defined.  Should be Series or DataFrame

    whitelist - list of names of klass methods to be constructed

    Returns
    -------
    The generator yields a sequence of strings, each suitable for exec'ing,
    that define implementations of the named methods for DataFrameGroupBy
    or SeriesGroupBy.

    Since we don't want to override methods explicitly defined in the
    base class, any such name is skipped.
    """

    method_wrapper_template = \
    """def %(name)s(%(sig)s) :
    \"""
    %(doc)s
    \"""
    f = %(self)s.__getattr__('%(name)s')
    return f(%(args)s)"""
    property_wrapper_template = \
    """@property
def %(name)s(self) :
    \"""
    %(doc)s
    \"""
    return self.__getattr__('%(name)s')"""
    for name in whitelist :
        # don't override anything that was explicitly defined
        # in the base class
        if hasattr(GroupBy,name) :
            continue
        # ugly, but we need the name string itself in the method.
        f = getattr(klass,name)
        doc = f.__doc__
        doc = doc if type(doc)==str else ''
        if type(f) == types.MethodType :
            wrapper_template = method_wrapper_template
            decl, args = make_signature(f)
            # pass args by name to f because otherwise
            # GroupBy._make_wrapper won't know whether
            # we passed in an axis parameter.
            args_by_name = ['{0}={0}'.format(arg) for arg in args[1:]]
            params = {'name':name,
                      'doc':doc,
                      'sig':','.join(decl),
                      'self':args[0],
                      'args':','.join(args_by_name)}
        else :
            wrapper_template = property_wrapper_template
            params = {'name':name, 'doc':doc}
        yield wrapper_template % params
