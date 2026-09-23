def worker(in_queue: InQueue, out_queue: OutQueue, device: torch.device) -> None:
    """The main loop of a worker thread."""
    with use_device(device):
        while True:
            task = in_queue.get()

            if task is None:
                break

            try:
                batch = task.compute()
            except Exception:
                exc_info = cast(ExcInfo, sys.exc_info())
                out_queue.put((False, exc_info))
                continue

            out_queue.put((True, (task, batch)))

    done = (False, None)
    out_queue.put(done)
