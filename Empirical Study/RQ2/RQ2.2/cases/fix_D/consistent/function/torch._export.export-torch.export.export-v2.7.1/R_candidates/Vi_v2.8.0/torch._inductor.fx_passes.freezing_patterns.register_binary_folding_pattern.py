def register_binary_folding_pattern(pattern, extra_check=_return_true):
    return register_graph_pattern(
        pattern,
        extra_check=extra_check,
        pass_dict=binary_folding_pass,
    )
