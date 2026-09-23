def _test_worker_info_init_fn(worker_id):
    worker_info = torch.utils.data.get_worker_info()
    assert worker_id == worker_info.id, "worker_init_fn and worker_info should have consistent id"
    assert worker_id < worker_info.num_workers, "worker_init_fn and worker_info should have valid id"
    assert worker_info.seed == torch.initial_seed(), "worker_init_fn and worker_info should have consistent seed"
    dataset = worker_info.dataset
    assert isinstance(dataset, TestWorkerInfoDataset), "worker_info should have correct dataset copy"
    assert not hasattr(dataset, 'value'), "worker_info should have correct dataset copy"
    # test that WorkerInfo attributes are read-only
    try:
        worker_info.id = 3999
    except RuntimeError as e:
        assert str(e) == "Cannot assign attributes to WorkerInfo objects"
    try:
        worker_info.a = 3
    except RuntimeError as e:
        assert str(e) == "Cannot assign attributes to WorkerInfo objects"
    for k in ['id', 'num_workers', 'seed', 'dataset']:
        assert "{}=".format(k) in repr(worker_info)
    dataset.value = [worker_id, os.getpid()]
