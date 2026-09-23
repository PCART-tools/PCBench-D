def _sharding_worker_init_fn(worker_init_fn, worker_id):
    if worker_init_fn is not None:
        worker_init_fn(worker_id)
    torch.utils.data.backward_compatibility.worker_init_fn(
        worker_id)
