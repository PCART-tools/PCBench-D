    def has_next_box(self) -> bool:
        if self.has_length:
            return self.fp.tell() + self.remaining_in_box < self.length
        else:
            return True
