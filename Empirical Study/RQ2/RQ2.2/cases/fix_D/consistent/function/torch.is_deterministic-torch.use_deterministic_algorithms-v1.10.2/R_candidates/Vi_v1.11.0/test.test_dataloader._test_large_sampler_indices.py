def _test_large_sampler_indices(persistent_workers):
    # See
    #   test_large_sampler_indices
    #   https://github.com/pytorch/pytorch/issues/48666

    dataloader = torch.utils.data.DataLoader(
        EmptyTensorDataset(10000000),
        batch_size=40960,
        persistent_workers=persistent_workers,
        num_workers=1)

    it = iter(dataloader)

    for x in it:
        assert x.numel() == 0
        raise RuntimeError('My Error')
