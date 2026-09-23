    def update(self, new_data):
        # so as not to conflict with spdict
        value = max(max(self.locs) + 1, 0)
        self._set_seq_locs(new_data, value)
