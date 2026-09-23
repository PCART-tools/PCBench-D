    def __init__(self, fp: IO[bytes] | None = None) -> None:
        if not fp:
            fp = sys.stdout.buffer
        self.fp = fp
