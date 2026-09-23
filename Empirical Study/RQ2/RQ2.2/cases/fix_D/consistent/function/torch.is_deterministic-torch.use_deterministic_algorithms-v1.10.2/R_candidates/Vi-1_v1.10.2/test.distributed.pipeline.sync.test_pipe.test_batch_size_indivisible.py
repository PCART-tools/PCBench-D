def test_batch_size_indivisible(setup_rpc):
    model = nn.Sequential(nn.Linear(1, 1))
    model = Pipe(model, chunks=4)

    with pytest.warns(None) as record:
        model(torch.rand(7, 1))

    # Indivisible batch size is legal.
    assert not record
