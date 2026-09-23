    def close(self) -> None:
        self.finalize()
        self.f.close()
