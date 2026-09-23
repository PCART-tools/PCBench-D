    def _iterate_slices(self):
        if self.axis == 0:
            # kludge
            if self._selection is None:
                slice_axis = self.obj.columns
            else:
                slice_axis = self._selection_list
            slicer = lambda x: self.obj[x]
        else:
            slice_axis = self.obj.index
            slicer = self.obj.xs

        for val in slice_axis:
            if val in self.exclusions:
                continue
            yield val, slicer(val)
