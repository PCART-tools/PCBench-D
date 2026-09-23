def test_batch_size_small(setup_rpc):
    model = nn.Sequential(nn.Linear(1, 1))
    model = Pipe(model, chunks=4)

    with pytest.warns(None) as record:
        model(torch.rand(2, 1))

    # Batch size smaller than chunks is legal.
    assert not record
