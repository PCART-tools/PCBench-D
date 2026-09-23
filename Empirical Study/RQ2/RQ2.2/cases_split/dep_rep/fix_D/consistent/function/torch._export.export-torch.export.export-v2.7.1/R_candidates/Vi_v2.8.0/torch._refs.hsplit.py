def hsplit(
    a: TensorLikeType, indices_or_sections: DimsType
) -> tuple[TensorLikeType, ...]:
    torch._check(
        a.ndim >= 1,
        lambda: (
            "torch.hsplit requires a tensor with at least 1 dimension, but got a tensor with "
            + str(a.ndim)
            + " dimensions!"
        ),
    )
    dim = 0 if a.ndim == 1 else 1
    if isinstance(indices_or_sections, IntLike):
        split_size = indices_or_sections
        torch._check(
            (split_size != 0 and a.shape[dim] % split_size == 0),
            lambda: (
                "torch.hsplit attempted to split along dimension "
                + str(dim)
                + ", but the size of the dimension "
                + str(a.shape[dim])
                + " is not divisible by the split_size "
                + str(split_size)
                + "!"
            ),
        )
        return tensor_split(a, split_size, dim)

    torch._check_type(
        isinstance(indices_or_sections, (list, tuple)),
        lambda: (
            "hsplit(): received an invalid combination of arguments. "
            "Expected indices_or_sections to be of type int, list of ints or tuple of ints "
            f"but got type {type(indices_or_sections)}"
        ),
    )

    split_sizes = indices_or_sections
    return tensor_split(a, split_sizes, dim)
