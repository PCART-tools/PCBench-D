def warmup_and_run_forward(f, *args):
    for _ in range(torch._C._jit_get_num_profiled_runs() + 1):
        results = f(*args)
    return results
