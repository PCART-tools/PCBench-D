def get_example_args(module_cls, constructor_arg_db, extra_kwargs=None):
    assert module_cls in constructor_arg_db, \
        f"No entry for {module_cls} in the constructor arg DB. Please add it to pass these tests."
    args, kwargs = constructor_arg_db[module_cls]
    extra_kwargs = {} if extra_kwargs is None else extra_kwargs

    # Recursively instantiate args / kwargs that are class objects.
    args = [instantiate_class(arg, *get_example_args(arg, constructor_arg_db), extra_kwargs=extra_kwargs)
            if inspect.isclass(arg) else torch.nn.Parameter(arg.to(**extra_kwargs))
            if isinstance(arg, torch.nn.Parameter) else arg for arg in args]
    kwargs = {k: instantiate_class(v, *get_example_args(v, constructor_arg_db), extra_kwargs=extra_kwargs)
              if inspect.isclass(v) else torch.nn.Parameter(v.to(*extra_kwargs))
              if isinstance(v, torch.nn.Parameter) else v for k, v in kwargs.items()}
    kwargs.update(extra_kwargs)
    return args, kwargs
