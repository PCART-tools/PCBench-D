def sample_inputs_argsort(*args, **kwargs):
    return [sample_input for sample_input in sample_inputs_sort(*args, **kwargs) if "stable" not in sample_input.kwargs]
