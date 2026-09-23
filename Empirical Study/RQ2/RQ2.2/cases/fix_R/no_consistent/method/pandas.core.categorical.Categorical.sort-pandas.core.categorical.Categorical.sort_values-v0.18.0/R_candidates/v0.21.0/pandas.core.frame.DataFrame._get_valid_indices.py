    def _get_valid_indices(self):
        is_valid = self.count(1) > 0
        return self.index[is_valid]
