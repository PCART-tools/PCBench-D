    def _read_bytes(self, num_bytes: int) -> bytes:
        if not self._can_read(num_bytes):
            msg = "Not enough data in header"
            raise SyntaxError(msg)

        data = self.fp.read(num_bytes)
        if len(data) < num_bytes:
            msg = f"Expected to read {num_bytes} bytes but only got {len(data)}."
            raise OSError(msg)

        if self.remaining_in_box > 0:
            self.remaining_in_box -= num_bytes
        return data
