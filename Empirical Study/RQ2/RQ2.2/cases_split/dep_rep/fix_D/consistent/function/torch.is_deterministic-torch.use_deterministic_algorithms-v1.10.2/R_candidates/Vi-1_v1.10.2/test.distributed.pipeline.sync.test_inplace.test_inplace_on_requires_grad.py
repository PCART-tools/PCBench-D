def test_inplace_on_requires_grad(setup_rpc):
    model = nn.Sequential(nn.Linear(1, 1), nn.ReLU(inplace=True))
    model = Pipe(model, checkpoint="always")

    x = torch.rand(1)
    y = model(x).local_value()

    message = r"a leaf Variable that requires grad .* used in an in-place operation."
    with pytest.raises(RuntimeError, match=message):
        y.backward()
