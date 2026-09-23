def test_parameters(setup_rpc):
    model = nn.Sequential(nn.Linear(1, 1))
    pipe = Pipe(model, chunks=1)
    assert list(pipe.parameters()) != []
