def move_kwargs_to_acc_out_ty(
    node_or_normalization_info: Union[NormalizationInfo, torch.fx.Node],
    new_kwargs: Dict[str, Any],
):
    """
    Given `node_or_normalization_info` which is either NormalizationInfo for a node, or
    a node to fetch NormalizationInfo for, check if kwargs_to_move_to_acc_out_ty exists
    in the NormalizationInfo, and if so perform the move of kwargs to acc_out_ty.
    """

    if isinstance(node_or_normalization_info, torch.fx.Node):
        node = node_or_normalization_info
        normalization_info = _normalization_dict.get((node.op, node.target))
    else:
        assert isinstance(node_or_normalization_info, NormalizationInfo)
        normalization_info = node_or_normalization_info

    assert normalization_info is not None
    if normalization_info.kwargs_to_move_to_acc_out_ty is None:
        return

    assert acc_utils.is_acc_op_with_kwarg(
        normalization_info.new_fn_target, "acc_out_ty"
    )

    # Build a dict representing the new TensorMetadata to use for acc_out_ty,
    # and then remove the kwarg from the new_kwargs since it's passed in via
    # acc_out_ty instead.
    tmd_dict: Dict[str, Any] = {}
    qparams: Dict[str, Any] = {}

    for kwarg_replacement_tuple in normalization_info.kwargs_to_move_to_acc_out_ty:
        if len(kwarg_replacement_tuple) == 2:
            orig_kwarg_name, tmd_field_name, move_to_qparams = *kwarg_replacement_tuple, False  # type: ignore[misc]
        else:
            assert len(kwarg_replacement_tuple) == 3
            orig_kwarg_name, tmd_field_name, move_to_qparams = kwarg_replacement_tuple  # type: ignore[misc]
        if move_to_qparams:
            qparams[tmd_field_name] = new_kwargs[orig_kwarg_name]
        else:
            tmd_dict[tmd_field_name] = new_kwargs[orig_kwarg_name]
        del new_kwargs[orig_kwarg_name]

    tmd_dict["qparams"] = qparams
    # Note: allow_partial_spec here because we are only using the tensor metadata tuple
    # here to pass specific values into the function. For example, for quantization we
    # only need to provide qparams dictionary, but is_quantized is
    # not passed in.
    new_kwargs["acc_out_ty"] = acc_utils.build_raw_tensor_meta(**tmd_dict)
