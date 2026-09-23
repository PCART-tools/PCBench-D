def reference_representation_rewrite(model: GraphModule) -> GraphModule:
    _QUANTIZED_LINEAR_EXAMPLE_INPUTS = (
        torch.randint(-128, 127, (2, 5), dtype=torch.int8),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.tensor([-128], dtype=torch.int),
        torch.tensor([127], dtype=torch.int),
        torch.randint(-128, 127, (5, 5), dtype=torch.int8),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.tensor([-127], dtype=torch.int),
        torch.tensor([127], dtype=torch.int),
        torch.randn(1, dtype=torch.float),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.tensor([-128], dtype=torch.int),
        torch.tensor([127], dtype=torch.int),
    )

    _DYNAMIC_QUANTIZED_LINEAR_EXAMPLE_INPUTS = (
        torch.randn((2, 5), dtype=torch.float),
        -128,
        127,
        torch.finfo(torch.float32).eps,
        torch.randint(-128, 127, (5, 5), dtype=torch.int8),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.tensor([-127], dtype=torch.int),
        torch.tensor([127], dtype=torch.int),
        torch.randn(1, dtype=torch.float),
    )

    _QUANTIZED_CONV2d_EXAMPLE_INPUTS = (
        torch.randint(-128, 127, (1, 3, 3, 3), dtype=torch.int8),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.tensor([-128], dtype=torch.int),
        torch.tensor([127], dtype=torch.int),
        torch.randint(-128, 127, (1, 3, 3, 3), dtype=torch.int8),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.tensor([-127], dtype=torch.int),
        torch.tensor([127], dtype=torch.int),
        torch.randn(1, dtype=torch.float),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.tensor([-128], dtype=torch.int),
        torch.tensor([127], dtype=torch.int),
    )

    _QUANTIZED_ADD_OR_ADD_RELU_EXAMPLE_INPUTS = (
        torch.randint(-128, 127, (1, 3, 3, 3), dtype=torch.int8),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.randint(-128, 127, (1, 3, 3, 3), dtype=torch.int8),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.tensor([-128], dtype=torch.int),
        torch.tensor([127], dtype=torch.int),
    )

    _QUANTIZED_MAX_POOL2D_EXAMPLE_INPUTS = (
        torch.randint(-128, 127, (1, 3, 3, 3), dtype=torch.int8),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.tensor([-128], dtype=torch.int),
        torch.tensor([127], dtype=torch.int),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.tensor([-128], dtype=torch.int),
        torch.tensor([127], dtype=torch.int),
    )

    _QUANTIZE_PER_TENSOR_INT8_EXAMPLE_INPUTS = (
        torch.randn(1, 3, 3, 3, dtype=torch.float),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.tensor([-128], dtype=torch.int),
        torch.tensor([127], dtype=torch.int),
    )

    _DEQUANTIZE_PER_TENSOR_INT8_EXAMPLE_INPUTS = (
        torch.randint(-128, 127, (1, 3, 3, 3), dtype=torch.int8),
        torch.randn(1, dtype=torch.float),
        torch.zeros(1, dtype=torch.int),
        torch.tensor([-128], dtype=torch.int),
        torch.tensor([127], dtype=torch.int),
    )

    _QUANTIZE_PER_CHANNEL_INT8_EXAMPLE_INPUTS = (
        torch.randn(1, 3, 3, 3, dtype=torch.float),
        torch.randn(3, dtype=torch.float),
        torch.zeros(3, dtype=torch.int),
        1,
        -128,
        127,
    )

    _DEQUANTIZE_PER_CHANNEL_INT8_EXAMPLE_INPUTS = (
        torch.randint(-128, 127, (1, 3, 3, 3), dtype=torch.int8),
        torch.randn(3, dtype=torch.float),
        torch.zeros(3, dtype=torch.int),
        1,
        -128,
        127,
    )

    _REWRITE_INFO_LIST = [
        _RewriteInfo(
            _DYNAMIC_QUANTIZED_LINEAR_EXAMPLE_INPUTS,
            _WrapperModule(_qdq_dynamic_quantized_linear),
            _WrapperModule(_reference_dynamic_quantized_linear),
            partial(
                _replace_literals_with_existing_placeholders,
                literal_to_ph_idx={-128: 1, 127: 2, torch.finfo(torch.float32).eps: 3},
            ),
            partial(
                _replace_literals_with_existing_placeholders,
                literal_to_ph_idx={-128: 1, 127: 2, torch.finfo(torch.float32).eps: 3},
            ),
        ),
        _RewriteInfo(
            _QUANTIZED_LINEAR_EXAMPLE_INPUTS,
            _WrapperModule(_qdq_quantized_linear),
            _WrapperModule(_reference_quantized_linear),
            _replace_literals_with_new_placeholders,
            _replace_literals_with_new_placeholders,
        ),
        _RewriteInfo(
            _QUANTIZED_CONV2d_EXAMPLE_INPUTS,
            _WrapperModule(_qdq_quantized_conv2d),
            _WrapperModule(_reference_quantized_conv2d),
            partial(_replace_literals_with_new_placeholders, exclude_literals=[-1]),
            partial(_replace_literals_with_new_placeholders, exclude_literals=[-1]),
        ),
        _RewriteInfo(
            _QUANTIZED_ADD_OR_ADD_RELU_EXAMPLE_INPUTS,
            _WrapperModule(_qdq_quantized_add_relu),
            _WrapperModule(_reference_quantized_add_relu),
        ),
        _RewriteInfo(
            _QUANTIZED_ADD_OR_ADD_RELU_EXAMPLE_INPUTS,
            _WrapperModule(_qdq_quantized_add),
            _WrapperModule(_reference_quantized_add),
        ),
        _RewriteInfo(
            _QUANTIZED_MAX_POOL2D_EXAMPLE_INPUTS,
            _WrapperModule(_qdq_quantized_max_pool2d),
            _WrapperModule(_reference_quantized_max_pool2d),
            _replace_literals_with_new_placeholders,
            _replace_literals_with_new_placeholders,
        ),
        _RewriteInfo(
            _QUANTIZE_PER_TENSOR_INT8_EXAMPLE_INPUTS,
            _WrapperModule(_quantize_per_tensor_int8),
            _WrapperModule(_reference_quantize_per_tensor_int8),
        ),
        _RewriteInfo(
            _DEQUANTIZE_PER_TENSOR_INT8_EXAMPLE_INPUTS,
            _WrapperModule(_dequantize_per_tensor_int8),
            _WrapperModule(_reference_dequantize_per_tensor_int8),
        ),
        _RewriteInfo(
            _QUANTIZE_PER_CHANNEL_INT8_EXAMPLE_INPUTS,
            _WrapperModule(_quantize_per_channel_int8),
            _WrapperModule(_reference_quantize_per_channel_int8),
            _replace_ph_qdq_per_channel_replacement,
            _replace_ph_qdq_per_channel_replacement,
        ),
        _RewriteInfo(
            _DEQUANTIZE_PER_CHANNEL_INT8_EXAMPLE_INPUTS,
            _WrapperModule(_dequantize_per_channel_int8),
            _WrapperModule(_reference_dequantize_per_channel_int8),
            _replace_ph_qdq_per_channel_replacement,
            _replace_ph_qdq_per_channel_replacement,
        ),
    ]

    remove_tensor_overload_for_qdq_ops(model)

    with _disable_aten_to_metadata_assertions():
        for rewrite_info in _REWRITE_INFO_LIST:
            example_inputs = rewrite_info.example_inputs
            pattern = rewrite_info.pattern
            replacement = rewrite_info.replacement
            pattern_post_trans = rewrite_info.pattern_post_trans
            replacement_post_trans = rewrite_info.replacement_post_trans
            pattern = _get_aten_graph_module_for_pattern(pattern, example_inputs)  # type: ignore[arg-type, assignment]
            remove_tensor_overload_for_qdq_ops(pattern)  # type: ignore[arg-type]
            replacement = _get_aten_graph_module_for_pattern(  # type: ignore[assignment]
                replacement,
                example_inputs,  # type: ignore[arg-type]
            )
            remove_tensor_overload_for_qdq_ops(replacement)  # type: ignore[arg-type]
            if pattern_post_trans:
                pattern = pattern_post_trans(pattern)
            if replacement_post_trans:
                replacement = replacement_post_trans(replacement)
            pattern.recompile()  # type: ignore[attr-defined]
            replacement.recompile()  # type: ignore[attr-defined]
            replace_pattern(model, pattern, replacement)

    return model
