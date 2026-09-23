def add_flex_arithmetic_methods(cls, flex_arith_method, radd_func=None,
                                flex_comp_method=None, flex_bool_method=None,
                                use_numexpr=True, force=False, select=None,
                                exclude=None):
    """
    Adds the full suite of flex arithmetic methods (``pow``, ``mul``, ``add``)
    to the class.

    Parameters
    ----------
    flex_arith_method : function (optional)
        factory for special arithmetic methods, with op string:
        f(op, name, str_rep, default_axis=None, fill_zeros=None, **eval_kwargs)
    radd_func :  function (optional)
        Possible replacement for ``lambda x, y: operator.add(y, x)`` for
        compatibility
    flex_comp_method : function, optional,
        factory for rich comparison - signature: f(op, name, str_rep)
    use_numexpr : bool, default True
        whether to accelerate with numexpr, defaults to True
    force : bool, default False
        if False, checks whether function is defined **on ``cls.__dict__``**
        before defining if True, always defines functions on class base
    select : iterable of strings (optional)
        if passed, only sets functions with names in select
    exclude : iterable of strings (optional)
        if passed, will not set functions with names in exclude
    """
    radd_func = radd_func or (lambda x, y: operator.add(y, x))
    # in frame, default axis is 'columns', doesn't matter for series and panel
    new_methods = _create_methods(
        flex_arith_method, radd_func, flex_comp_method, flex_bool_method,
        use_numexpr, default_axis='columns', special=False)
    new_methods.update(dict(
        multiply=new_methods['mul'],
        subtract=new_methods['sub'],
        divide=new_methods['div']
    ))
    # opt out of bool flex methods for now
    for k in ('ror_', 'rxor', 'rand_'):
        if k in new_methods:
            new_methods.pop(k)

    add_methods(cls, new_methods=new_methods, force=force, select=select,
                exclude=exclude)
