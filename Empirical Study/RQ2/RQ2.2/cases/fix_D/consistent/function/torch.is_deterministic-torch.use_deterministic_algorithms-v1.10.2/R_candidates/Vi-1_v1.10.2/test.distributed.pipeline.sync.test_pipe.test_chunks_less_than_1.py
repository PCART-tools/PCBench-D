def test_chunks_less_than_1(setup_rpc):
    model = nn.Sequential(nn.Linear(1, 1))

    with pytest.raises(ValueError):
        Pipe(model, chunks=0)

    with pytest.raises(ValueError):
        Pipe(model, chunks=-1)
