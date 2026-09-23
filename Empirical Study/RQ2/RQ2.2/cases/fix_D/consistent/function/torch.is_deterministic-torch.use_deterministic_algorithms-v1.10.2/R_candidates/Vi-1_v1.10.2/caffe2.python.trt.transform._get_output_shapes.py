def _get_output_shapes(output_value_infos):
    names = [x.name for x in output_value_infos]
    shapes = [_dim_values_to_list(x.type.tensor_type.shape.dim) for x in output_value_infos]
    return dict(zip(names, shapes))
