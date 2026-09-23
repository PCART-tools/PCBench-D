def test_compute_success():
    """Task.compute returns (True, (task, batch)) on success."""

    def _42():
        return Batch(torch.tensor(42))

    with spawn_workers([torch.device("cpu")]) as (in_queues, out_queues):
        t = Task(CPUStream, compute=_42, finalize=None)
        in_queues[0].put(t)
        ok, (task, batch) = out_queues[0].get()

        assert ok
        assert task is t
        assert isinstance(batch, Batch)
        assert batch[0].item() == 42
