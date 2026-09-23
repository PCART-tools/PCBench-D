def _infer_reduction_dims(dims_arg: object, ndim: int) -> Optional[list[int]]:
    if dims_arg is None:
        return None
    dims = cast(list[int], as_list(dims_arg))
    dims = cast(list[int], normalize_dims(dims, ndim))
    empty_dims = [[0], [-1], []]
    if ndim == 0 and dims_arg in empty_dims:
        return None
    return dims
