    def __init__(self, fp: IO[bytes], chunk: Callable[..., None]) -> None:
        self.fp = fp
        self.chunk = chunk
