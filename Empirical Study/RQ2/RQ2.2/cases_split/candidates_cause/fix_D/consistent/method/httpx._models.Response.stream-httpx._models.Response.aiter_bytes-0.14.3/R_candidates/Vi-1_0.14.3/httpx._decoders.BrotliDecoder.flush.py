    def flush(self) -> bytes:
        if not self.seen_data:
            return b""
        try:
            if hasattr(self.decompressor, "finish"):
                self.decompressor.finish()
            return b""
        except brotli.error as exc:  # pragma: nocover
            raise ValueError(str(exc))
