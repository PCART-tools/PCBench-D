def create_model(with_fsdp, with_checkpoint, model_hidden_dim):
    torch.manual_seed(0)
    model = Model(model_hidden_dim, with_fsdp, with_checkpoint)
    if with_fsdp:
        model.stem = FSDP(model.stem)
        model.blocks = FSDP(model.blocks)
        model.head = FSDP(model.head)

    return model
