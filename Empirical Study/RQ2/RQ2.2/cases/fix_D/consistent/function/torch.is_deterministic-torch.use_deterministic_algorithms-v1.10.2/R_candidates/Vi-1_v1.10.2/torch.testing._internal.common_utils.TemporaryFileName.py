    @contextmanager  # noqa: T484
    def TemporaryFileName(*args, **kwargs):
        with tempfile.NamedTemporaryFile(*args, **kwargs) as f:
            yield f.name
