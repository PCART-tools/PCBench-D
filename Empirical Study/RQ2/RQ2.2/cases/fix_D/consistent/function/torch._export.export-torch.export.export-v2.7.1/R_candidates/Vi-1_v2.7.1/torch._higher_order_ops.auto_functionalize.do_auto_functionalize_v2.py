def do_auto_functionalize_v2(
    mode: "torch._subclasses.functional_tensor.FunctionalTensorMode",
    op: OpOverload,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> Any:
    from torch._subclasses.functional_tensor import PythonFunctionalizeAPI

    ctx = PythonFunctionalizeAPI(mode=mode)

    # All of the (args, kwargs), but all as kwargs. The names for the
    # args come from the schema. This makes it easier for us to work with them.
    normalized_kwargs = {}

    schema = op._schema
    for idx, arg in enumerate(schema.arguments):
        # NB: torch_dispatch kwargs are the args defined as kwarg-only in the schema
        if arg.name in kwargs:
            normalized_kwargs[arg.name] = kwargs[arg.name]
        elif idx < len(args):
            # if its out of bounds we don't need to do anything
            # as it means the the optional arg was passed with its default
            # value
            normalized_kwargs[arg.name] = args[idx]
        else:
            normalized_kwargs[arg.name] = arg.default_value

    # List of the name of args that get mutated (according to the schema)
    mutable_args_names, mutable_args_types = get_mutable_args(op)

    # A list of all bases of mutable args without duplication
    all_bases = []
    all_bases_addresses: list[int] = []

    # Map arg_name to the index of its base in all_bases.
    arg_to_base_index: dict[str, Any] = {}

    def update_dict(tensor, arg_name, index=None):
        base = tensor if get_base(tensor) is None else get_base(tensor)

        def set_result(base_index):
            if index is None:
                arg_to_base_index[arg_name] = base_index
            else:
                arg_to_base_index[arg_name][index] = base_index

        if not all_bases_addresses.__contains__(base._cdata):
            all_bases_addresses.append(base._cdata)
            all_bases.append(base)
            set_result(len(all_bases) - 1)
        else:
            set_result(all_bases_addresses.index(base._cdata))

    for arg_name in mutable_args_names:
        arg = normalized_kwargs[arg_name]
        if arg is None:
            continue

        if isinstance(arg, list):
            arg_to_base_index[arg_name] = {}
            for i, tensor in enumerate(arg):
                if tensor is None:
                    arg_to_base_index[arg_name].append(None)
                    continue

                update_dict(tensor, arg_name, i)

        else:
            update_dict(arg, arg_name)

    # add view_meta for each args into unwrapped_kwargs.
    write_view_information_to_args(
        mutable_args_names,
        mutable_args_types,
        normalized_kwargs,
        arg_to_base_index,
    )

    # remove mutated args from the kwargs (its a function of _all_bases now)
    for arg_name in mutable_args_names:
        del normalized_kwargs[arg_name]  # type: ignore[arg-type]

    unwrapped_kwargs = ctx.unwrap_tensors(normalized_kwargs)  # type: ignore[arg-type]
    if "self" in unwrapped_kwargs or "self_" in unwrapped_kwargs:
        warnings.warn(
            "Using `self` or `self_` as an argument in the definition of custom ops may lead to ambiguous parsing. "
            "Please consider using a different name for this argument to avoid potential issues."
        )
    all_basis_unwrapped = ctx.unwrap_tensors(all_bases)

    with ctx.redispatch_to_next():
        unwrapped_outs = auto_functionalized_v2(
            op, **dict(unwrapped_kwargs, _all_bases=all_basis_unwrapped)  # type: ignore[arg-type]
        )

    unwrapped_actual_out: Union[Any, tuple[Any]] = (
        unwrapped_outs if len(all_bases) == 0 else unwrapped_outs[: -len(all_bases)]
    )

    unwrapped_mutable_out = (
        [] if len(all_bases) == 0 else unwrapped_outs[-len(all_bases) :]
    )

    if len(op._schema.returns) == 0:
        assert unwrapped_actual_out[0] is None
        unwrapped_actual_out = None
    elif len(op._schema.returns) == 1:
        assert len(unwrapped_actual_out) == 1
        unwrapped_actual_out = unwrapped_actual_out[0]
    else:
        assert len(unwrapped_actual_out) == len(op._schema.returns)

    for orig_arg, unwrapped_out in zip(all_bases, unwrapped_mutable_out):
        # Can be None if input was `Tensor(a!)?`
        if unwrapped_out is None:
            continue

        # We only handle Tensor or List[Tensor] here for now.
        def sync_update(o, orig_arg):
            ctx.replace(orig_arg, o)
            ctx.commit_update(orig_arg)
            ctx.sync(orig_arg)

        if isinstance(unwrapped_out, torch.Tensor):
            sync_update(unwrapped_out, orig_arg)
        elif isinstance(unwrapped_out, list) and all(
            isinstance(o, torch.Tensor) for o in unwrapped_out
        ):
            assert len(orig_arg) == len(unwrapped_out)
            for orig_a, o in zip(orig_arg, unwrapped_out):
                sync_update(o, orig_a)
        else:
            raise RuntimeError(
                f"unsupported type for auto-functionalization: {unwrapped_out}"
            )

    return ctx.wrap_tensors(unwrapped_actual_out)  # type: ignore[arg-type]
