def signature_to_meta(
    signature: list[KernelArgType],
    *,
    size_dtype: Optional[str],
    argdefs: list[ArgName],
    indices: Optional[list[int]] = None,
) -> dict[str, str]:
    if indices is None:
        indices = list(range(len(signature)))
    return {
        argdefs[i].name: signature_of(arg, size_dtype=size_dtype)
        for i, arg in zip(indices, signature)
    }
