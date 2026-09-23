def test_checkpoint_mode_when_chunks_1(setup_rpc):
    model = nn.Sequential(nn.Linear(1, 1))

    # All checkpoint modes are fine.
    Pipe(model, chunks=1, checkpoint="except_last")
    Pipe(model, chunks=1, checkpoint="always")
    Pipe(model, chunks=1, checkpoint="never")
