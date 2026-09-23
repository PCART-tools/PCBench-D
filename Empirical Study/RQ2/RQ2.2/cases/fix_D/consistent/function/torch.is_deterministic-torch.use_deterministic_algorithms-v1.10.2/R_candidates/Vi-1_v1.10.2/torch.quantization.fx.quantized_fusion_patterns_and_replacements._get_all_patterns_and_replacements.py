def _get_all_patterns_and_replacements():
    return [
        (relu_inplace_pattern, relu_replacement),
        (relu_non_inplace_pattern, relu_replacement)
    ]
