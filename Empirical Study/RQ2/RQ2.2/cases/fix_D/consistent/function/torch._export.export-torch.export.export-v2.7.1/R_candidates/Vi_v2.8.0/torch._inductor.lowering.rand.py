@register_lowering(aten.rand)
def rand(*args, **kwargs):
    if kwargs.get("generator", None) is not None:
        return fallback_rand_generator(*args, **kwargs)
    elif config.fallback_random:
        kwargs.pop("generator", None)
        return fallback_rand_default(*args, **kwargs)
    raise AssertionError("should have been handled in replace_random.py")
