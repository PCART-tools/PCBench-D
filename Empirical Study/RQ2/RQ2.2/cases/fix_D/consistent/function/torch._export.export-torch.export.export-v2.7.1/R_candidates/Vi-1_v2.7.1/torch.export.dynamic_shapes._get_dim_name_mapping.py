def _get_dim_name_mapping(
    dynamic_shapes: Union[dict[str, Any], tuple[Any], list[Any], None]
):
    name_to_dim = {}
    for dim in tree_flatten(
        dynamic_shapes,
        is_leaf=lambda x: isinstance(x, _Dim),
    )[0]:
        if dim is None:
            # NOTE: this must denote a non-Tensor or automatic at this point.
            continue
        if isinstance(dim, int):
            continue
        elif isinstance(dim, _Dim):
            name_to_dim[dim.__name__] = dim
            if isinstance(dim, _DerivedDim):
                name_to_dim[dim.root.__name__] = dim.root  # type: ignore[attr-defined]
        else:
            assert isinstance(dim, _DimHint)
    return name_to_dim
