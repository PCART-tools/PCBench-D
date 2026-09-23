def test_no_grad(setup_rpc):
    model = nn.Sequential(nn.Linear(1, 1))
    model = Pipe(model, chunks=2)
    input = torch.rand(2, 1)

    latent = None

    def hook(module, input, output):
        _ = module
        _ = input

        nonlocal latent
        latent = output

    partition = model.partitions[0]
    partition.register_forward_hook(hook)

    with torch.no_grad():
        model(input)

    assert latent.grad_fn is None
