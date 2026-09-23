@auto_functionalized_v2.py_impl(DispatchKey.CompositeExplicitAutograd)
def auto_functionalized_v2_dense(
    _mutable_op: OpOverload,
    _only_clone_these_bases: Optional[tuple[int, ...]] = None,
    **kwargs: Any,
) -> tuple[Any, tuple[Tensor, ...]]:
    all_bases: list[Tensor] = kwargs.pop("_all_bases", [])
    mutable_args_names, mutable_args_types = get_mutable_args(_mutable_op)
    args_view_info = read_view_information_from_args(
        mutable_args_names, mutable_args_types, kwargs, all_bases
    )

    if _only_clone_these_bases is None:
        _only_clone_these_bases = tuple(range(len(all_bases)))

    def maybe_copy(i, t):
        if t is None:
            return None
        if i in _only_clone_these_bases:
            return clone_preserve_strides(t)
        else:
            return t

    all_bases_new = [maybe_copy(i, t) for i, t in enumerate(all_bases)]

    # create new args
    new_kwargs = dict(**kwargs)

    # re-generate all inputs from all_bases_new using args_view_info and add them to new_kwargs.
    for arg_name in mutable_args_names:
        if args_view_info[arg_name] is None:
            new_kwargs[arg_name] = None
        elif isinstance(args_view_info[arg_name], list):
            new_kwargs[arg_name] = []
            for i, elem in enumerate(args_view_info[arg_name]):
                if elem is None:
                    new_kwargs[arg_name].append(None)
                else:
                    view_info = args_view_info[arg_name][i]
                    new_kwargs[arg_name].append(
                        view_info.regenerate_view(all_bases_new)
                    )
        else:
            new_kwargs[arg_name] = args_view_info[arg_name].regenerate_view(
                all_bases_new
            )

    out = _mutable_op(**new_kwargs)

    if isinstance(out, tuple):
        return (*out, *all_bases_new)  # type: ignore[return-value]
    else:
        return (out, *all_bases_new)  # type: ignore[return-value]
