def test_named_children(setup_rpc):
    a = nn.Linear(1, 1)
    b = nn.Linear(1, 1)

    model = nn.Sequential(OrderedDict([("a", a), ("b", b)]))
    model = Pipe(model)

    names = set(n for n, _ in model.named_modules())
    assert "partitions.0.0" in names
    assert "partitions.1.0" in names

    # Pipe doesn't support __getattr__. Unlike nn.Sequential, Pipe requires
    # several methods in its namespace.
    with pytest.raises(AttributeError):
        model.a
