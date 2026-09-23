    def _get_sorted_data(self):
        return self.data._take(self.sort_idx, axis=self.axis)
