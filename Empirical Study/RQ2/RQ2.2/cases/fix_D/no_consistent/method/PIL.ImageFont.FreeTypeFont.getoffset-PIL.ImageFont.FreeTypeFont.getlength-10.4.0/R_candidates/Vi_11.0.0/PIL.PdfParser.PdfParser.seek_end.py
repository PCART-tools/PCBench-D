    def seek_end(self) -> None:
        assert self.f is not None
        self.f.seek(0, os.SEEK_END)
