    def _get_data_to_aggregate(self) -> Manager2D:
        obj = self._obj_with_exclusions
        if self.axis == 1:
            return obj.T._mgr
        else:
            return obj._mgr
