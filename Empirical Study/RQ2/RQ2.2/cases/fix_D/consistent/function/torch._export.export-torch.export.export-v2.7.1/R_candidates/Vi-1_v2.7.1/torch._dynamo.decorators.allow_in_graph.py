def allow_in_graph(fn):
    """
    Tells the compiler frontend (Dynamo) to skip symbolic introspection of the function
    and instead directly write it to the graph when encountered.

    See :func:`torch.compiler.allow_in_graph`'s docstring for the full documentation

    WARNING: this API can be a footgun, please read the documentation carefully.
    """
    if isinstance(fn, (list, tuple)):
        return [allow_in_graph(x) for x in fn]
    assert callable(fn), "allow_in_graph expects a callable"
    if trace_rules.lookup_callable(fn) != variables.TorchInGraphFunctionVariable:
        fn_id = id(fn)
        trace_rules._disallowed_callable_ids.remove(fn_id)
        trace_rules._allowed_callable_ids.add(fn_id)

        # Avoid id reuse which creates subtle bugs.
        def deregister():
            trace_rules._allowed_callable_ids.remove(fn_id)

        weakref.finalize(fn, deregister)
    return fn
