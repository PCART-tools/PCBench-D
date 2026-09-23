    def __init__(self, fp: IO[bytes], length: int = -1) -> None:
        self.fp = fp
        self.has_length = length >= 0
        self.length = length
        self.remaining_in_box = -1
