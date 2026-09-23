def _test_timeout(persistent_workers):
    dataset = SleepDataset(10, 3)
    dataloader = DataLoader(dataset, batch_size=2, num_workers=2, timeout=1,
                            persistent_workers=persistent_workers)
    _ = next(iter(dataloader))
