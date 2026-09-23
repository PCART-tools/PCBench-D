def _create_model(compute_cycles, has_params: bool):
    model = FSDP(
        nn.Sequential(
            FSDP(Layer(compute_cycles, has_params)),
            FSDP(Layer(compute_cycles, has_params)),
            FSDP(Layer(compute_cycles, has_params)),
            FSDP(Layer(compute_cycles, has_params)),
        )
    ).cuda()
    return model
