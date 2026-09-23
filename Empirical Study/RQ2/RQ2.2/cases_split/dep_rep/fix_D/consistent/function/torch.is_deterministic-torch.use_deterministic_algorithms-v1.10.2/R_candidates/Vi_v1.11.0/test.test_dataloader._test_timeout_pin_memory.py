def _test_timeout_pin_memory(persistent_workers):
    dataset = SleepDataset(10, 3)
    dataloader = DataLoader(dataset, batch_size=2, num_workers=2, timeout=1, pin_memory=True,
                            persistent_workers=persistent_workers)
    _ = next(iter(dataloader))
