    def __init__(self, fn: StrOrBytesPath | IO[bytes], new: bool = False) -> None:
        self.f: IO[bytes]
        if is_path(fn):
            self.name = fn
            self.close_fp = True
            try:
                self.f = open(fn, "w+b" if new else "r+b")
            except OSError:
                self.f = open(fn, "w+b")
        else:
            self.f = cast(IO[bytes], fn)
            self.close_fp = False
        self.beginning = self.f.tell()
        self.setup()
