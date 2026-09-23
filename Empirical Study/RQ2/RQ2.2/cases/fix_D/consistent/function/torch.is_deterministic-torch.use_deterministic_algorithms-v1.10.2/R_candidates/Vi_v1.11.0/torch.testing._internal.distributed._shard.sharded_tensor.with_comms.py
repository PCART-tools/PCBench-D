def with_comms(func=None, init_rpc=True, backend="nccl"):
    if func is None:
        return partial(
            with_comms,
            init_rpc=init_rpc,
            backend=backend,
        )

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if backend == "nccl" and torch.cuda.device_count() < self.world_size:
            sys.exit(TEST_SKIPS[f"multi-gpu-{self.world_size}"].exit_code)
        self.init_comms(init_rpc=init_rpc, backend=backend)
        func(self)
        self.destroy_comms(destroy_rpc=init_rpc)
    return wrapper
