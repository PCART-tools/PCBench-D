def test_checkpoint_mode_invalid(setup_rpc):
    model = nn.Sequential(nn.Linear(1, 1))

    with pytest.raises(ValueError, match="checkpoint is not one of 'always', 'except_last', or 'never'"):
        Pipe(model, chunks=2, checkpoint="INVALID_CHECKPOINT")
