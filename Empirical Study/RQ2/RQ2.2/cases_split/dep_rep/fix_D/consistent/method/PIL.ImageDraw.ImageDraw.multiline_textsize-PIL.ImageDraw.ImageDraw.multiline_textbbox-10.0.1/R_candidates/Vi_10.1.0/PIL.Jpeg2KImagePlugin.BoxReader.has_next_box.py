    def has_next_box(self):
        if self.has_length:
            return self.fp.tell() + self.remaining_in_box < self.length
        else:
            return True
