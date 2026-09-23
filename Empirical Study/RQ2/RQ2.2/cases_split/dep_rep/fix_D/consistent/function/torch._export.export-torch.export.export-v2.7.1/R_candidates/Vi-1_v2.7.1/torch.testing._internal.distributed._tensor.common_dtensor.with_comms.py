def with_comms(eager_init: Union[TestFunc, bool] = False) -> TestFunc:

    def decorator(func, eager_init: bool = False):

        @wraps(func)  # pyre-ignore[6]
        def wrapper(
            self, *args: tuple[object], **kwargs: dict[str, Any]  # type: ignore[misc]
        ) -> None:
            # if enough GPU we can use GPU, otherwise we fallback to CPU
            if not (TEST_CUDA or TEST_XPU) or torch.accelerator.device_count() < self.world_size:
                self.device_type = "cpu"
            else:
                self.device_type = DEVICE_TYPE

            self.init_pg(eager_init)

            try:
                func(self, *args, **kwargs)  # type: ignore[misc]
            except Exception as e:
                dist.destroy_process_group()
                raise e

            self.destroy_pg()

        return wrapper

    return decorator(func=eager_init) if callable(eager_init) else partial(decorator, eager_init=eager_init)
