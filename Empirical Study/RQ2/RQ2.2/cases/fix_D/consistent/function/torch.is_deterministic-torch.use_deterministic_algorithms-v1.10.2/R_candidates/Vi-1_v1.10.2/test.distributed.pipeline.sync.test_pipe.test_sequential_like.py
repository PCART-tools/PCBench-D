def test_sequential_like(setup_rpc):
    a = nn.Linear(1, 1)
    b = nn.Linear(1, 1)

    model = nn.Sequential(a, b)
    model = Pipe(model)

    assert len(model) == 2
    assert list(model) == [a, b]

    assert model[0] is a
    assert model[1] is b
    with pytest.raises(IndexError):
        _ = model[2]

    assert model[-1] is b
    assert model[-2] is a
