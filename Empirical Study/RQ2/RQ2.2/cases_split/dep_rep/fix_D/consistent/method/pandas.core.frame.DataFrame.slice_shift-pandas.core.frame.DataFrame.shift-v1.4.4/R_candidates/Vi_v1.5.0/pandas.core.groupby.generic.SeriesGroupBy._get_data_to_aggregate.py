    def _get_data_to_aggregate(self) -> SingleManager:
        ser = self._obj_with_exclusions
        single = ser._mgr
        return single
