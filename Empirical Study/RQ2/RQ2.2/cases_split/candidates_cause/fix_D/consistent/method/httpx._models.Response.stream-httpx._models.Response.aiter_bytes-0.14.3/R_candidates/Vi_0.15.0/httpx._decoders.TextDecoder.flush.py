    def flush(self) -> str:
        if self.decoder is None:
            return ""
        return self.decoder.decode(b"", True)
