def test_verify_module_non_sequential(setup_rpc):
    with pytest.raises(TypeError, match="module must be nn.Sequential to be partitioned"):
        Pipe(nn.Module())
