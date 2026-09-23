def test_input_varargs(setup_rpc):
    model = nn.Sequential(nn.Linear(1, 1))
    model = Pipe(model)

    a = torch.rand(1)
    b = torch.rand(1)

    # TypeError: forward() takes 2 positional arguments but 3 were given
    with pytest.raises(TypeError):
        model(a, b)
