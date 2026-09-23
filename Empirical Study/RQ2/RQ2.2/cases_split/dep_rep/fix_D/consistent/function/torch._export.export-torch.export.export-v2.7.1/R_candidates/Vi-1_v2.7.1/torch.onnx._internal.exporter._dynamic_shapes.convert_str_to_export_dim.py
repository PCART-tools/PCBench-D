def convert_str_to_export_dim(
    dynamic_shapes: dict[str, Any] | tuple[Any, ...] | list[Any] | None,
) -> tuple[dict[str, Any] | tuple[Any, ...] | list[Any] | None, bool]:
    # 1. If there is no string in dynamic_shapes, we do not touch dynamic_shapes
    if dynamic_shapes is None or not _any_str_or_dim_in_dynamic_shapes(dynamic_shapes):
        return dynamic_shapes, False
    # 2. Convert "name" to Dim.AUTO with flattening and identify if there is any string
    #    to be replaced with Dim.AUTO, and then unflatten it back to the original structure.
    #    for example: {"y": {0: "dim_0"}, "x": {1: "dim_1"}}
    #    to {"y": {0: Dim.AUTO}, "x": {1: Dim.AUTO}}
    dynamic_shapes_with_export_dim: list[
        list[_Dim | _DimHint | None] | dict[int, _Dim | _DimHint | None] | None
    ] = []
    flat_dynamic_shapes, tree_structure = _flatten_dynamic_shapes_to_axes(
        dynamic_shapes
    )
    for axes in flat_dynamic_shapes:
        if axes is None:
            dynamic_shapes_with_export_dim.append(None)
        elif isinstance(axes, dict):
            converted_axes_dict: dict[int, _Dim | _DimHint | None] = {}
            for axis, dim in axes.items():
                if isinstance(dim, str):
                    converted_axes_dict[axis] = torch.export.Dim.AUTO  # type: ignore[attr-defined]
                else:
                    converted_axes_dict[axis] = dim
            dynamic_shapes_with_export_dim.append(converted_axes_dict)
        elif isinstance(axes, (list, tuple)):
            converted_axes_list: list[_Dim | _DimHint | None] = []
            for dim in axes:
                if isinstance(dim, str):
                    converted_axes_list.append(torch.export.Dim.AUTO)  # type: ignore[attr-defined]
                else:
                    converted_axes_list.append(dim)
            dynamic_shapes_with_export_dim.append(converted_axes_list)

    dynamic_shapes_with_export_dim = _pytree.tree_unflatten(
        dynamic_shapes_with_export_dim, tree_structure
    )
    return (
        dynamic_shapes_with_export_dim,
        True,
    )
