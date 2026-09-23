def create_attach_sparsifier(model, **sparse_config):
    """Create a DataNormSparsifier and the attach it to the model embedding layers

    Args:
        model (nn.Module)
            layer of the model that needs to be attached to the sparsifier
        sparse_config (Dict)
            Config to the DataNormSparsifier. Should contain the following keys:
                - sparse_block_shape
                - norm
                - sparsity_level
    """
    data_norm_sparsifier = DataNormSparsifier(**sparse_config)
    for name, parameter in model.named_parameters():
        if "emb_l" in name:
            valid_name = get_valid_name(name)
            data_norm_sparsifier.add_data(name=valid_name, data=parameter)
    return data_norm_sparsifier
