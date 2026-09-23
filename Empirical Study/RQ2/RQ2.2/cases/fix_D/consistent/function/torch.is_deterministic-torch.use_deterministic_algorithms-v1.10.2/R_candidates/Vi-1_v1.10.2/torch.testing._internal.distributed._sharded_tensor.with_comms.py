def with_comms(func=None, init_rpc=True):
    if func is None:
        return partial(
            with_comms,
            init_rpc=init_rpc,
        )

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if torch.cuda.device_count() < self.world_size:
            sys.exit(TEST_SKIPS[f"multi-gpu-{self.world_size}"].exit_code)
        self.init_comms(init_rpc)
        func(self)
        self.destroy_comms(init_rpc)

    return wrapper
