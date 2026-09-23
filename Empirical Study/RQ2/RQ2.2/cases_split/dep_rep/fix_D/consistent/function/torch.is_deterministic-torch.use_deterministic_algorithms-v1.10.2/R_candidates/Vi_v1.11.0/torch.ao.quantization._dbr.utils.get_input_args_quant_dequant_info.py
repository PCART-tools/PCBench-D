def get_input_args_quant_dequant_info(
    seen_op_info: SeenOpInfo,
    tensor_id_to_scale_zp: Dict[int, Tuple[torch.Tensor, torch.Tensor]],
) -> Tuple[List[Optional[Tuple[float, int]]], List[bool], bool]:
    """
    Returns a list of information about the tensor inputs to the current op.

    Quant list:
    For each tensor input:
    * if the tensor input needs a quant, the list will contain
      (scale, zero_point)
    * if the tensor input does not need a quant, the list will contain None

    Dequant list:
    For each tensor input:
    * if the tensor input needs a dequant, True, otherwise, False

    any_arg_quant_or_dequant_needed:
    If True, at least one of quants or dequants is needed. If False,
    there are no quants or dequants needed.

    For example, if there are two tensor inputs to the current op, and the
    first input needs a quant, this function will return

      # quants
      [(scale0, zero_point0), None],
      # dequants
      [False, False]
    """
    quant_infos: List[Optional[Tuple[float, int]]] = []
    dequant_infos: List[bool] = []

    # determine the expected output dtype
    output_dtype = seen_op_info.output_tensor_infos[0].inf_dtype
    packable_arg_idxs = get_packable_arg_idxs(seen_op_info.type)
    any_arg_quant_or_dequant_needed = False

    for input_arg_idx, input_arg in enumerate(seen_op_info.input_tensor_infos):
        arg_will_be_packed = packable_arg_idxs is not None and \
            input_arg_idx in packable_arg_idxs and \
            seen_op_info.op_packing_only_uses_module_attributes
        if input_arg is not None and not arg_will_be_packed:
            tensor_id = input_arg.id
            if input_arg.inf_dtype != output_dtype:
                any_arg_quant_or_dequant_needed = True
                if output_dtype == torch.quint8:
                    assert tensor_id in tensor_id_to_scale_zp
                    scale, zp = tensor_id_to_scale_zp[tensor_id]
                    # TODO: return this to the caller
                    quant_infos.append((scale, zp,))  # type: ignore[arg-type]
                    dequant_infos.append(False)
                else:
                    quant_infos.append(None)
                    dequant_infos.append(True)
            else:
                quant_infos.append(None)
                dequant_infos.append(False)
        else:
            quant_infos.append(None)
            dequant_infos.append(False)
    return quant_infos, dequant_infos, any_arg_quant_or_dequant_needed
