def instantiate_class(cls, args, kwargs, extra_kwargs):
    return cls(*args, **kwargs) if extra_kwargs is None else cls(*args, **kwargs, **extra_kwargs)
