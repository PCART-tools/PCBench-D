def _insert_fun(
    op_and_target: Tuple[str, Union[str, Callable]],
    arg_replacement_tuples: List[Tuple],
    new_fn_target: Optional[Callable] = None,
    custom_mapping_fn: Optional[Callable] = None,
    kwargs_to_move_to_acc_out_ty: Optional[
        List[Union[Tuple[str, str, bool], Tuple[str, str]]]
    ] = None,
    needs_shapes_for_normalization=False,
    allow_normalize_from_torch_package=False,
):
    if op_and_target[0] == "call_function":
        assert callable(op_and_target[1])
    elif op_and_target[0] == "call_method":
        assert isinstance(op_and_target[1], str)
    elif op_and_target[0] == "call_module":
        assert isinstance(op_and_target[1], type)

    # Finalize arg replacement tuples.
    # 1. Check to see if they have the `is_optional` bool, and if not defaulting it to
    #   False.
    # 2. Some kwargs might have aliases. e.g. "a", "x" and "x1" are aliases of "input".
    #   Here we replace `orig_kwarg` with a tuple of all aliases if it has aliases.
    final_arg_replacement_tuples = []
    for arg_replacement_tuple in arg_replacement_tuples:
        if len(arg_replacement_tuple) == 2:
            orig_kwarg, new_kwarg, is_optional = *arg_replacement_tuple, False
        else:
            assert len(arg_replacement_tuple) == 3
            orig_kwarg, new_kwarg, is_optional = arg_replacement_tuple

        if not isinstance(orig_kwarg, tuple):
            orig_kwarg = (orig_kwarg,)

        # Use set to avoid duplicates.
        orig_kwarg_set = set(orig_kwarg)

        for k in orig_kwarg:
            if k in ALIAS_MAP:
                orig_kwarg_set.update(ALIAS_MAP[k])
        final_arg_replacement_tuples.append(
            (tuple(orig_kwarg_set), new_kwarg, is_optional)
        )

    assert op_and_target not in _normalization_dict.keys()
    norm_info = NormalizationInfo(
        new_fn_target=new_fn_target,  # type: ignore[arg-type]
        arg_replacement_tuples=final_arg_replacement_tuples,
        custom_mapping_fn=custom_mapping_fn,
        kwargs_to_move_to_acc_out_ty=kwargs_to_move_to_acc_out_ty,
        needs_shapes_for_normalization=needs_shapes_for_normalization,
    )
    _normalization_dict[op_and_target] = norm_info

    # If allow_normalize_from_torch_package then add another entry to
    # _normalization_dict where we look for the qualified name of the target with the
    # torch_package module prefix. Note that we leave off any integer at the end of
    # "<torch_package_>" in order to allow for whatever mangling index is used.
    if allow_normalize_from_torch_package:
        torch_package_op_and_target = (
            op_and_target[0],  # type: ignore[]
            f"<torch_package_>.{_get_qualified_name(op_and_target[1])}",  # type: ignore[arg-type]
        )
        _normalization_dict[torch_package_op_and_target] = norm_info
