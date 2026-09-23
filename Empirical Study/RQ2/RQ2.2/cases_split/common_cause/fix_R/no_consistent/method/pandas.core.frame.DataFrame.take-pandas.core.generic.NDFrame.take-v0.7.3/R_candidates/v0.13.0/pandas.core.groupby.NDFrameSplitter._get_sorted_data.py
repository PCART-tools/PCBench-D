    def _get_sorted_data(self):
        # this is the BlockManager
        data = self.data._data

        # this is sort of wasteful but...
        sorted_axis = data.axes[self.axis].take(self.sort_idx)
        sorted_data = data.reindex_axis(sorted_axis, axis=self.axis)

        return sorted_data
