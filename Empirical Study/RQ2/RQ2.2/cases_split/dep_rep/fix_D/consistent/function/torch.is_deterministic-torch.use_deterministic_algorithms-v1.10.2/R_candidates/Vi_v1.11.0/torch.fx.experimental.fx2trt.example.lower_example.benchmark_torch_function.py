def benchmark_torch_function(iters: int, f, *args) -> float:
    """Estimates the average time duration for a single inference call in second

    If the input is batched, then the estimation is for the batches inference call.

    Args:
        iters: number of inference iterations to run
        f: a function to perform a single inference call

    Returns:
        estimated average time duration in second for a single inference call
    """
    with torch.inference_mode():
        f(*args)
    torch.cuda.synchronize()
    start_event = torch.cuda.Event(enable_timing=True)
    end_event = torch.cuda.Event(enable_timing=True)
    print("== Start benchmark iterations")
    with torch.inference_mode():
        start_event.record()
        for _ in range(iters):
            f(*args)
        end_event.record()
    torch.cuda.synchronize()
    print("== End benchmark iterations")
    return (start_event.elapsed_time(end_event) * 1.0e-3) / iters
