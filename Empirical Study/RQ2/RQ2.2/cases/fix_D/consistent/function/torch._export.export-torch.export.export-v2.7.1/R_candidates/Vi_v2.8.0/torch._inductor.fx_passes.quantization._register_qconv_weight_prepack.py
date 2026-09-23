def _register_qconv_weight_prepack():
    for dtype in [torch.float32, torch.bfloat16]:
        weight_prepack_patterns = _generate_qconv_weight_prepack_patterns(dtype)
        for weight_prepack_pattern in weight_prepack_patterns:
            # Register to pass_number 1, so we can do dequant promotion in pass_number 0.
            _register_qconv_weight_prepack_pass(
                weight_prepack_pattern, pass_number=1, dtype=dtype
            )
