def _check_outputs_same_dtype_and_shape(output1, output2, eps, idx=None) -> None:
    # Check that the returned outputs don't have different dtype or shape when you
    # perturb the input
    on_index = "on index {idx} " if idx is not None else ""
    assert output1.shape == output2.shape, (
        f"Expected `func` to return outputs with the same shape"
        f" when inputs are perturbed {on_index}by {eps}, but got:"
        f" shapes {output1.shape} and {output2.shape}."
    )
    assert output1.dtype == output2.dtype, (
        f"Expected `func` to return outputs with the same dtype"
        f" when inputs are perturbed {on_index}by {eps}, but got:"
        f" dtypes {output1.dtype} and {output2.dtype}."
    )
