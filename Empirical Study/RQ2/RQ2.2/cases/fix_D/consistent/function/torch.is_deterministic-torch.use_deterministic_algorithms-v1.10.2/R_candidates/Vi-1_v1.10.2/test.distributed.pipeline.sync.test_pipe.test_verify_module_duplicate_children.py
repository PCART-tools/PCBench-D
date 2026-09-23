def test_verify_module_duplicate_children(setup_rpc):
    conv = nn.Conv2d(3, 3, 1)
    model = nn.Sequential(conv, conv)

    with pytest.raises(ValueError, match="module with duplicate children is not supported"):
        Pipe(model)
