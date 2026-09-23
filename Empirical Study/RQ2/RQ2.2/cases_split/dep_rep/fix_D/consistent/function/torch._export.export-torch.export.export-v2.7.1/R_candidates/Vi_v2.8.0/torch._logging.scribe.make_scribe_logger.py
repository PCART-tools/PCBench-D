    def make_scribe_logger(name: str, thrift_src: str) -> Callable[..., None]:
        def inner(**kwargs: TLazyField) -> None:
            pass

        return inner
