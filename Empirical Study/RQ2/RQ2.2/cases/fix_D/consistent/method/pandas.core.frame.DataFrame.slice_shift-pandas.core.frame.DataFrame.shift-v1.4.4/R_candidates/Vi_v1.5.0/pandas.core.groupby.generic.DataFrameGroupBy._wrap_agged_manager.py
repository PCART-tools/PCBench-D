    def _wrap_agged_manager(self, mgr: Manager2D) -> DataFrame:
        if not self.as_index:
            # GH 41998 - empty mgr always gets index of length 0
            rows = mgr.shape[1] if mgr.shape[0] > 0 else 0
            index = Index(range(rows))
            mgr.set_axis(1, index)
            result = self.obj._constructor(mgr)

            self._insert_inaxis_grouper_inplace(result)
            result = result._consolidate()
        else:
            index = self.grouper.result_index
            mgr.set_axis(1, index)
            result = self.obj._constructor(mgr)

        if self.axis == 1:
            result = result.T

        # Note: we only need to pass datetime=True in order to get numeric
        #  values converted
        return self._reindex_output(result)._convert(datetime=True)
