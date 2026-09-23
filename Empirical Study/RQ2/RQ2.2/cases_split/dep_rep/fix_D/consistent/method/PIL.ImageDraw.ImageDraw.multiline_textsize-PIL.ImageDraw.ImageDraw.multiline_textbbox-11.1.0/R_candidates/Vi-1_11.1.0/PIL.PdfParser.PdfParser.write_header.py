    def write_header(self) -> None:
        assert self.f is not None
        self.f.write(b"%PDF-1.4\n")
