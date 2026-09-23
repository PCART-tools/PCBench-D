    def _get_comb_axis(self, i):
        if self._is_series:
            all_indexes = [x.index for x in self.objs]
        else:
            try:
                all_indexes = [x._data.axes[i] for x in self.objs]
            except IndexError:
                types = [type(x).__name__ for x in self.objs]
                raise TypeError("Cannot concatenate list of %s" % types)

        return _get_combined_index(all_indexes, intersect=self.intersect)
