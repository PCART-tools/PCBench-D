    def __enter__(self) -> "ElapsedTimer":
        self.start = perf_counter()
        return self
