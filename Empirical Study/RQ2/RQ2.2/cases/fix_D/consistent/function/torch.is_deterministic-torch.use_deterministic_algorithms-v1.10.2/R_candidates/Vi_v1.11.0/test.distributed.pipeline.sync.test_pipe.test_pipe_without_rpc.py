def test_pipe_without_rpc():
    model = nn.Sequential(nn.Linear(1, 1))
    with pytest.raises(RuntimeError, match='Please initialize RPC framework'):
        pipe = Pipe(model, chunks=1)
