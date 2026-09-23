def block_diag(*tensors: list[TensorLikeType]) -> TensorLikeType:
    """
    This is used as an input to PythonRefInfo. `torch.block_diag`
    expects arguments splatted, but `aten.block_diag` expects only
    one argument that is a list of Tensors.
    """
    return _block_diag_iterable(tensors)  # type: ignore[arg-type]
