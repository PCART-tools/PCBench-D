def test_deny_moving(setup_rpc):
    a = nn.Linear(1, 1)
    b = nn.Linear(1, 1)

    model = nn.Sequential(a, b)
    model = Pipe(model)

    # Moving is denied.
    with pytest.raises(TypeError):
        model.cuda()

    with pytest.raises(TypeError):
        model.cpu()

    with pytest.raises(TypeError):
        model.to(torch.device("cuda"))

    with pytest.raises(TypeError):
        model.to(0)

    with pytest.raises(TypeError):
        model.to("cuda")

    with pytest.raises(TypeError):
        model.to(device=0)

    with pytest.raises(TypeError):
        model.to(torch.rand(1))

    with pytest.raises(TypeError):
        model.to(tensor=torch.rand(1))

    # Casting is allowed.
    model.half()
    model.to(torch.double)
    model.to(dtype=torch.float)
