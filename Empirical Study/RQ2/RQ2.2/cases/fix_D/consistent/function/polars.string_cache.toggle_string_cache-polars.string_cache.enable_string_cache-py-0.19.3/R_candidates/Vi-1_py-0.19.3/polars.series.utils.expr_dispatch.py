def expr_dispatch(cls: type[T]) -> type[T]:
    """
    Series/NameSpace class decorator that sets up expression dispatch.

    * Applied to the Series class, and/or any Series 'NameSpace' classes.
    * Walks the class attributes, looking for methods that have empty function
      bodies, with signatures compatible with an existing Expr function.
    * IIF both conditions are met, the empty method is decorated with @call_expr.
    """
    # create lookup of expression functions in this namespace
    namespace = getattr(cls, "_accessor", None)
    expr_lookup = _expr_lookup(namespace)

    for name in dir(cls):
        if not name.startswith("_"):
            attr = getattr(cls, name)
            if callable(attr):
                attr = _undecorated(attr)
                # note: `co_varnames` starts with the function args, but needs to be
                # constrained by `co_argcount` as it also includes function-level consts
                args = attr.__code__.co_varnames[: attr.__code__.co_argcount]
                # if an expression method with compatible method exists, further check
                # that the series implementation has an empty function body
                if (namespace, name, args) in expr_lookup and _is_empty_method(attr):
                    setattr(cls, name, call_expr(attr))
    return cls
