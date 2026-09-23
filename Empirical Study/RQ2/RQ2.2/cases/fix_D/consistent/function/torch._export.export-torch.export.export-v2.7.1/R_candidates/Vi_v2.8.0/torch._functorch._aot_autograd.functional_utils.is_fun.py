def is_fun(t):
    if isinstance(t, Tensor) and is_traceable_wrapper_subclass(t):
        # See Note [Functionalization always runs last]
        # This means that if we want to "functionalize" a subclass, we need to ensure that the functional wrapper
        # goes at the bottom.
        # recurse here, so we can support nested wrapper subclasses
        t_attrs, _ = t.__tensor_flatten__()  # type: ignore[attr-defined]
        t_inners = [getattr(t, attr) for attr in t_attrs]
        any_fun = any(is_fun(x) for x in t_inners)
        all_fun = all(is_fun(x) for x in t_inners)
        assert any_fun == all_fun
        return any_fun

    return isinstance(t, FunctionalTensor)
