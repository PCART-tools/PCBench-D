def with_comms(eager_init: Union[TestFunc, bool] = False) -> TestFunc:
    def decorator(func, eager_init: bool = False):
        @wraps(func)  # pyre-ignore[6]
        def wrapper(
            self, *args: tuple[object], **kwargs: dict[str, Any]  # type: ignore[misc]
        ) -> None:
            self.init_pg(eager_init)

            try:
                func(self, *args, **kwargs)  # type: ignore[misc]
            except Exception as e:
                dist.destroy_process_group()
                raise e

            self.destroy_pg()

        return wrapper

    return (
        decorator(func=eager_init)
        if callable(eager_init)
        else partial(decorator, eager_init=eager_init)
    )
