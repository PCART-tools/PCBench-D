def _get_all_patterns_and_replacements():
    return [
        (relu_inplace_pattern, relu_replacement),
        (relu_non_inplace_pattern, relu_replacement),
        (relu_method_pattern, relu_method_replacement),
        (relu_inplace_method_pattern, relu_inplace_method_replacement),
        (relu6_inplace_pattern, relu6_replacement),
        (relu6_non_inplace_pattern, relu6_replacement),
        (hardtanh_pattern, hardtanh_replacement),
        (hardtanh_non_inplace_pattern, hardtanh_replacement),
        (hardtanh_inplace_pattern, hardtanh_inplace_replacement),
        (mean_pattern, mean_replacement),
        (mean_method_pattern, mean_method_replacement),
    ]
