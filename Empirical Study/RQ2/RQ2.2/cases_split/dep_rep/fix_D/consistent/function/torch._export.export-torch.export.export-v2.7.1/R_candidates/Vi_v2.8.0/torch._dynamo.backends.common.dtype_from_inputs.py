def dtype_from_inputs(example_inputs) -> torch.dtype:
    for x in example_inputs:
        if hasattr(x, "dtype"):
            return x.dtype
