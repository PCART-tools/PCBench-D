    def _iterate_slices(self):
        if self.axis == 0:
            # kludge
            if self._selection is None:
                slice_axis = self._selected_obj.items
            else:
                slice_axis = self._selection_list
            slicer = lambda x: self._selected_obj[x]
        else:
            raise NotImplementedError("axis other than 0 is not supported")

        for val in slice_axis:
            if val in self.exclusions:
                continue

            yield val, slicer(val)
