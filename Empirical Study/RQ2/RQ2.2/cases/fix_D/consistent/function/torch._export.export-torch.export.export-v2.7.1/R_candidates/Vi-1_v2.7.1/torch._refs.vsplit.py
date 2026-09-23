def vsplit(
    a: TensorLikeType, indices_or_sections: DimsType
) -> tuple[TensorLikeType, ...]:
    torch._check(
        a.ndim >= 2,
        lambda: (
            "torch.vsplit requires a tensor with at least 2 dimension, but got a tensor with "
            + str(a.ndim)
            + " dimensions!"
        ),
    )
    if isinstance(indices_or_sections, IntLike):
        split_size = indices_or_sections
        torch._check(
            (split_size != 0 and a.shape[0] % split_size == 0),
            lambda: (
                f"torch.vsplit attempted to split along dimension 0"
                f", but the size of the dimension "
                f"{a.shape[0]}"
                f" is not divisible by the split_size "
                f"{split_size}"
                f"!"
            ),
        )
        return tensor_split(a, split_size, 0)

    torch._check_type(
        isinstance(indices_or_sections, (list, tuple)),
        lambda: (
            "vsplit(): received an invalid combination of arguments. "
            "Expected indices_or_sections to be of type int, list of ints or tuple of ints "
            f"but got type {type(indices_or_sections)}"
        ),
    )

    split_sizes = indices_or_sections
    return tensor_split(a, split_sizes, 0)
