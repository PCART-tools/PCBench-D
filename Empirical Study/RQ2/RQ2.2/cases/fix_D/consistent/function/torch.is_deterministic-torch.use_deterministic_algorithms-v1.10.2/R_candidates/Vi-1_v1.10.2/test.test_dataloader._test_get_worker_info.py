def _test_get_worker_info():
    # get_worker_info returns None in main proc
    assert torch.utils.data.get_worker_info() is None
    num_workers = 2
    batch_size = 2
    dataset = TestWorkerInfoDataset(6, batch_size, num_workers)
    dataloader = DataLoader(dataset, batch_size=batch_size,
                            num_workers=num_workers,
                            worker_init_fn=_test_worker_info_init_fn)
    it = iter(dataloader)
    data = []
    for d in it:
        data.append(d)
    worker_pids = [w.pid for w in it._workers]
    data = torch.cat(data, 0)
    for d in data:
        # each `d` is a [worker_id, worker_pid] pair, which is set in
        # _test_worker_info_init_fn
        assert d[1] == worker_pids[d[0]]
    # get_worker_info returns None in main proc after data loading
    assert torch.utils.data.get_worker_info() is None
    # main proc dataset was never assigned this attribute
    assert not hasattr(dataset, 'value')
    try:
        _ = dataset[0]
    except AttributeError:
        return
    raise RuntimeError('Expected AttributeError')
