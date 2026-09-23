def bind_args_cached(func, tx, fn_source, args, kwargs):
    spec = _get_spec(func)
    spec.update_defaults(func)
    ba = {}
    rem_kw = dict(kwargs)

    # 1) Bind all positional (pos-only + pos-or-kw)
    for i, name in enumerate(spec.all_pos_names):
        if i < len(args):
            ba[name] = wrap_bound_arg(tx, args[i])
        elif name in rem_kw:
            if name in spec.posonly_names:
                raise TypeError(f"{name} is positional-only")
            ba[name] = wrap_bound_arg(tx, rem_kw.pop(name))
        elif name in spec.pos_default_map:
            idx = spec.pos_default_map[name]
            default_source = None
            if fn_source:
                default_source = DefaultsSource(fn_source, idx)
            ba[name] = wrap_bound_arg(tx, spec.defaults[idx], default_source)
        else:
            raise TypeError(f"Missing required positional argument: {name}")

    # 2) *args
    extra = args[len(spec.all_pos_names) :]
    if spec.varargs_name:
        ba[spec.varargs_name] = wrap_bound_arg(tx, tuple(extra))
    elif extra:
        raise TypeError(
            f"Too many positional arguments: got {len(args)}, expected {len(spec.all_pos_names)}"
        )

    # 3) Keyword-only
    for name in spec.kwonly_names:
        if name in rem_kw:
            ba[name] = wrap_bound_arg(tx, rem_kw.pop(name))
        elif name in spec.kwdefaults:
            kwdefault_source = None
            if fn_source:
                kwdefault_source = DefaultsSource(fn_source, name, is_kw=True)
            ba[name] = wrap_bound_arg(tx, spec.kwdefaults[name], kwdefault_source)
        else:
            raise TypeError(f"Missing required keyword-only argument: {name}")

    # 4) **kwargs
    if spec.varkw_name:
        ba[spec.varkw_name] = wrap_bound_arg(tx, rem_kw)
    elif rem_kw:
        raise TypeError(f"Unexpected keyword arguments: {list(rem_kw)}")

    return ba
