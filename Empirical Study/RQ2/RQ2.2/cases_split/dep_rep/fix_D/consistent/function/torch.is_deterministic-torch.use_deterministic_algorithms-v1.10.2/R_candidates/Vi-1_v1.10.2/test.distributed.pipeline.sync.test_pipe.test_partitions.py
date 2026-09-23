def test_partitions(setup_rpc):
    a = nn.Linear(1, 1)
    b = nn.Linear(1, 1)

    model = nn.Sequential(a, b)
    model = Pipe(model)

    assert isinstance(model.partitions, nn.ModuleList)
    assert isinstance(model.partitions[0], nn.Sequential)
    assert isinstance(model.partitions[1], nn.Sequential)

    assert "partitions.0.0.weight" in model.state_dict()
