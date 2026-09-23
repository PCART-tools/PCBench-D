    def sync_elapsed(self) -> float:
        now = time.perf_counter()
        return now - self.started
