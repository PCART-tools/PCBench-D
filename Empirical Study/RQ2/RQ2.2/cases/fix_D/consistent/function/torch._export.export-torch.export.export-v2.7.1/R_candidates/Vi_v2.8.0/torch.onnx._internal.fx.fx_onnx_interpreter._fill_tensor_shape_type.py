def _fill_tensor_shape_type(
    onnxscript_values: onnxscript_graph_building.TorchScriptTensor
    | tuple[onnxscript_graph_building.TorchScriptTensor, ...],
    name: str,
    expected_values: fx_type_utils.META_VALUE_TYPE
    | list[fx_type_utils.META_VALUE_TYPE]
    | tuple[fx_type_utils.META_VALUE_TYPE | None, ...],
):
    """Fill the meta information of onnxscript_values with that from the fx FakeTensor."""

    if isinstance(expected_values, (list, tuple)) and not isinstance(
        onnxscript_values, (list, tuple)
    ):
        # ex: aten::split - in onnx_dtype: seq(tensor)
        # onnxscript_values is a single tensor, but expected_values is a list of tensors.
        return

    flat_onnxscript_values, _ = _pytree.tree_flatten(onnxscript_values)
    flat_expected_values, _ = _pytree.tree_flatten(expected_values)
    for i, (onnxscript_value, expected_value) in enumerate(
        zip(flat_onnxscript_values, flat_expected_values)
    ):
        if expected_value is None:
            # There is no shape/type from None.
            # NOTE: according to https://github.com/pytorch/pytorch/blob/main/torch/_meta_registrations.py,
            # None could be a valid value for return type, so we need to handle it.
            # e.g. the function: meta__scaled_dot_product_flash() in cpu mode.
            continue
        elif fx_type_utils.is_torch_symbolic_type(expected_value):
            # aten::sym_size output is a int, not a tensor, which stands
            # for the size of one dim. We treat it as 1-D tensor.
            onnxscript_value.dtype = fx_type_utils.from_sym_value_to_torch_dtype(
                expected_value
            )
            onnxscript_value.shape = torch.Size([1])
        elif isinstance(expected_value, (int, float, bool)):
            onnxscript_value.dtype = fx_type_utils.from_scalar_type_to_torch_dtype(
                type(expected_value)
            )
            onnxscript_value.shape = torch.Size([])
        elif isinstance(expected_value, complex):
            # From complex scalar to real representation
            onnxscript_value_to_torch_dtype = (
                fx_type_utils.from_scalar_type_to_torch_dtype(type(expected_value))
            )
            onnxscript_value.dtype = (
                fx_type_utils.from_complex_to_float(onnxscript_value_to_torch_dtype)
                if onnxscript_value_to_torch_dtype is not None
                else None
            )
            onnxscript_value.shape = torch.Size([2])
        elif fx_type_utils.is_torch_complex_dtype(expected_value.dtype):
            # Like torch.view_as_real, we flatten complex tensors to real tensors with
            # additional last dimension of 2
            onnxscript_value.shape = torch.Size((*expected_value.size(), 2))
            # complex64 -> float32, complex128 -> float64, etc.
            onnxscript_value.dtype = fx_type_utils.from_complex_to_float(
                expected_value.dtype
            )
            # Dispatcher needs to know the value is complex
            onnxscript_value.is_complex = True
        else:
            # We set node output sizes to be dynamic to continue the model conversion,
            # and inputs are also set to be dynamic in add_input().
            onnxscript_value.shape = expected_value.size()
            onnxscript_value.dtype = expected_value.dtype

        # naming
        if i > 0:
            onnxscript_value.name = f"{name}_{i}"
        else:
            onnxscript_value.name = name
