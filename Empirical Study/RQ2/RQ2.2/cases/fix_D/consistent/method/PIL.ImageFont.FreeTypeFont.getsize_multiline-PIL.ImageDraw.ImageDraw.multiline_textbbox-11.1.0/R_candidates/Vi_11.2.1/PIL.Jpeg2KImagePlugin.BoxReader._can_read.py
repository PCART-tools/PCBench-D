    def _can_read(self, num_bytes: int) -> bool:
        if self.has_length and self.fp.tell() + num_bytes > self.length:
            # Outside box: ensure we don't read past the known file length
            return False
        if self.remaining_in_box >= 0:
            # Inside box contents: ensure read does not go past box boundaries
            return num_bytes <= self.remaining_in_box
        else:
            return True  # No length known, just read
