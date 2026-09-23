    def close(self) -> None:
        self.finalize()
        if self.close_fp:
            self.f.close()
