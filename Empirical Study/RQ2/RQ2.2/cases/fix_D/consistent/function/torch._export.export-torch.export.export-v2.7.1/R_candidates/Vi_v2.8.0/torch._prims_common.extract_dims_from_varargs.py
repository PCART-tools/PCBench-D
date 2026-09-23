def extract_dims_from_varargs(
    dims: Union[DimsSequenceType, tuple[DimsSequenceType, ...]]
) -> DimsSequenceType:
    if dims and isinstance(dims[0], Sequence):
        assert len(dims) == 1
        dims = cast(tuple[DimsSequenceType], dims)
        return dims[0]
    else:
        return cast(DimsSequenceType, dims)
