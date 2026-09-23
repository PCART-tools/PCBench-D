    def __init__(self, fp: IO[bytes], chunk: Callable[..., None], seq_num: int) -> None:
        self.fp = fp
        self.chunk = chunk
        self.seq_num = seq_num
