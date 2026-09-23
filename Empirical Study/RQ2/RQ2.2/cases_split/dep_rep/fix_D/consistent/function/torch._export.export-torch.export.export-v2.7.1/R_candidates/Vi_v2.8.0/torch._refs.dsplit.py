def dsplit(a: TensorLikeType, sections: DimsType) -> TensorSequenceType:
    if a.ndim < 3:
        raise RuntimeError(
            f"torch.dsplit requires a tensor with at least 3 dimension, but got a tensor with {a.ndim} dimensions!"
        )
    if isinstance(sections, IntLike) and (sections == 0 or a.shape[2] % sections != 0):
        raise RuntimeError(
            "torch.dsplit attempted to split along dimension 2, "
            + f"but the size of the dimension {a.shape[2]} is not divisible by the split_size {sections}!"
        )
    return tensor_split(a, sections, 2)
