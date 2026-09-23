def update_names_with_mapping(tensor, rename_map, inplace):
    dim_map = build_dim_map(tensor)
    for old_dim in rename_map.keys():
        new_dim = rename_map[old_dim]
        if old_dim in dim_map.keys():
            dim_map[old_dim] = new_dim
        else:
            raise RuntimeError(('{api_name}: Tried to rename dim \'{old_dim}\' to dim '
                                '{new_dim} in Tensor[{dims}] but dim \'{old_dim}\' does not exist')
                               .format(old_dim=old_dim, new_dim=new_dim, dims=tensor.names,
                                       api_name=namer_api_name(inplace)))
    return tensor._update_names(tuple(dim_map.values()), inplace)
