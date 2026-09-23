def _test_segfault():
    dataset = SegfaultDataset(10)
    dataloader = DataLoader(dataset, batch_size=2, num_workers=2, worker_init_fn=disable_stderr)
    _ = next(iter(dataloader))
