def bind_method(cls, name, func):
    """Bind a method to class, python 2 and python 3 compatible.

    Parameters
    ----------

    cls : type
        class to receive bound method
    name : basestring
        name of method on class instance
    func : function
        function to be bound as method


    Returns
    -------
    None
    """
    # only python 2 has bound/unbound method issue
    if not compat.PY3:
        setattr(cls, name, types.MethodType(func, None, cls))
    else:
        setattr(cls, name, func)
