    def _initialize_chunksize(self, chunksize: int | None) -> int:
        if chunksize is None:
            return (100000 // (len(self.cols) or 1)) or 1
        return int(chunksize)
