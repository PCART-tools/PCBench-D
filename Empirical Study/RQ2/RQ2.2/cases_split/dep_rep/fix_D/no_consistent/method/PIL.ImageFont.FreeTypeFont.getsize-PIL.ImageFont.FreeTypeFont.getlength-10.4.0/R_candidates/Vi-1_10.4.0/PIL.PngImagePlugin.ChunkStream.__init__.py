    def __init__(self, fp: IO[bytes]) -> None:
        self.fp: IO[bytes] | None = fp
        self.queue: list[tuple[bytes, int, int]] | None = []
