    def _get_sorted_data(self):
        return self.data.take(self.sort_idx, axis=self.axis, convert=False)
