    def _get_data_to_aggregate(self) -> BlockManager:
        obj = self._obj_with_exclusions
        if self.axis == 1:
            return obj.T._data
        else:
            return obj._data
