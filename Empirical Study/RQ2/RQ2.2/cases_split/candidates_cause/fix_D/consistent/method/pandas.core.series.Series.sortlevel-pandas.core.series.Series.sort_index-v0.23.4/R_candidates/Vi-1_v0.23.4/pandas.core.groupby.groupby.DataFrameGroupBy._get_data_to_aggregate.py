    def _get_data_to_aggregate(self):
        obj = self._obj_with_exclusions
        if self.axis == 1:
            return obj.T._data, 1
        else:
            return obj._data, 1
