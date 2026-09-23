def skip_if_no_gpu(func):
    """Nccl multigpu tests require at least 2 GPUS. Skip if this is not met"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not torch.cuda.is_available():
            sys.exit(TEST_SKIPS["no_cuda"].exit_code)
        world_size = int(os.environ["WORLD_SIZE"])
        if torch.cuda.device_count() < world_size:
            sys.exit(TEST_SKIPS[f"multi-gpu-{world_size}"].exit_code)

        return func(*args, **kwargs)

    return wrapper
