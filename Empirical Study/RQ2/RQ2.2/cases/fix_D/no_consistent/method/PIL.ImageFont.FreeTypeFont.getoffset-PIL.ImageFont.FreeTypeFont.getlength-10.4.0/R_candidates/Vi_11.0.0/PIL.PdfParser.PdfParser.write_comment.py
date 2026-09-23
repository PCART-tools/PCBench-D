    def write_comment(self, s: str) -> None:
        assert self.f is not None
        self.f.write(f"% {s}\n".encode())
