def skip_if_no_gpu(func):
    """Skips if the world size exceeds the number of GPUs, ensuring that if the
    test is run, each rank has its own GPU via ``torch.cuda.device(rank)``."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not torch.cuda.is_available():
            sys.exit(TEST_SKIPS["no_cuda"].exit_code)
        world_size = int(os.environ["WORLD_SIZE"])
        if torch.cuda.device_count() < world_size:
            sys.exit(TEST_SKIPS[f"multi-gpu-{world_size}"].exit_code)
        if TEST_HPU and torch.hpu.device_count < world_size:
            sys.exit(TEST_SKIPS[f"multi-gpu-{world_size}"].exit_code)
        if TEST_XPU and torch.xpu.device_count < world_size:
            sys.exit(TEST_SKIPS[f"multi-xpu-{world_size}"].exit_code)

        return func(*args, **kwargs)

    return wrapper
