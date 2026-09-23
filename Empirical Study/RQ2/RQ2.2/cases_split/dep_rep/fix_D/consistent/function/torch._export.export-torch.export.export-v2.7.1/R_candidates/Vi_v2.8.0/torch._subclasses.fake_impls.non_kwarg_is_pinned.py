@register_op_impl(aten.is_pinned.default)
def non_kwarg_is_pinned(fake_mode, func, *args, **kwargs):
    _, new_kwargs = normalize_function(
        func, args, kwargs, normalize_to_only_use_kwargs=True
    )
    inp = new_kwargs.pop("input")
    # we'll ignore device argument because it is deprecated and not
    # actually used by is_pinned.
    with in_kernel_invocation_manager(fake_mode):
        r = func(inp)
    return r
