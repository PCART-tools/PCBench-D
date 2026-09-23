def test_empty_module(setup_rpc):
    # Empty sequential module is not illegal.
    model = nn.Sequential()
    model = Pipe(model)

    assert model(torch.tensor(42)).local_value() == torch.tensor(42)

    # But only tensor or tensors is legal in Pipe.
    with pytest.raises(TypeError):
        model(42)
