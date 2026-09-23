def _init_model(rank, world_size):
    device_mesh = init_device_mesh(DEVICE, (world_size,))

    # Create a dummy model and wrap it in FSDP
    model = Model().cuda()
    device_mesh = init_device_mesh(DEVICE, (world_size,))
    model = FSDP(model, device_mesh=device_mesh, use_orig_params=True)

    optim = torch.optim.Adam(model.parameters(), lr=0.0001)

    _patch_model_state_dict(model)
    _patch_optimizer_state_dict(model, optimizers=optim)

    return model, optim
