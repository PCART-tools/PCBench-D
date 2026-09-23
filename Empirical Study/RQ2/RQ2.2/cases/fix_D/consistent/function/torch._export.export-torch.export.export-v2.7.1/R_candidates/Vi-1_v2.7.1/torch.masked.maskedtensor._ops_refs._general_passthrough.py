@register_dispatch_func(PASSTHROUGH_FNS)
def _general_passthrough(func, *args, **kwargs):
    return _apply_pass_through_fn(func, *args, **kwargs)
