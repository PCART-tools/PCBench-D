def test_compute_exception():
    """Task.compute returns (False, exc_info) on failure."""

    def zero_div():
        0 / 0

    with spawn_workers([torch.device("cpu")]) as (in_queues, out_queues):
        t = Task(CPUStream, compute=zero_div, finalize=None)
        in_queues[0].put(t)
        ok, exc_info = out_queues[0].get()

        assert not ok
        assert isinstance(exc_info, tuple)
        assert issubclass(exc_info[0], ZeroDivisionError)
