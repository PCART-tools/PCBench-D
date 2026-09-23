def rename_axis(model: ir.Model, rename_mapping: dict[str, str]) -> None:
    """Rename dynamic axes in a model according to the specified dynamic_axes names."""

    # NOTE: Mapping needs to be srted by length because the shape expression
    # could have multiple ways to be expressed, for example,
    # {"s1": sequence_length, "s11": "past_sequence_length", "s1 + s11": "masked_sequence_length"}
    # We prefer the replacement starts from the longest match.
    sorted_rename_mapping = dict(
        sorted(rename_mapping.items(), key=lambda item: len(item[0]), reverse=True)
    )
    for value in _all_values(model):
        if value.shape is None:
            continue
        new_shape = []
        changed = False
        for dim in value.shape:
            if not isinstance(dim, ir.SymbolicDim):
                new_shape.append(dim)
                continue
            dim_name = dim.value
            if dim_name in sorted_rename_mapping:
                new_shape.append(sorted_rename_mapping[dim_name])
                changed = True
            elif dim_name is not None:
                # For example: "2*s1", "s1+1", "s1-1", "s1*s2", "s1/s2"
                new_name = _replace_names(dim_name, sorted_rename_mapping)
                new_shape.append(new_name)
                if new_name != dim_name:
                    changed = True
            else:
                new_shape.append(None)
        if changed:
            value.shape = ir.Shape(new_shape)
