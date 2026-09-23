    @property
    def elapsed(self) -> timedelta:
        if self.end is None:
            return timedelta(seconds=perf_counter() - self.start)
        return timedelta(seconds=self.end - self.start)
