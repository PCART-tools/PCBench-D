    def _aggregate_frame(self, func, *args, **kwargs) -> DataFrame:
        if self.grouper.nkeys != 1:
            raise AssertionError("Number of keys must be 1")

        obj = self._obj_with_exclusions

        result: dict[Hashable, NDFrame | np.ndarray] = {}
        for name, grp_df in self.grouper.get_iterator(obj, self.axis):
            fres = func(grp_df, *args, **kwargs)
            result[name] = fres

        result_index = self.grouper.result_index
        other_ax = obj.axes[1 - self.axis]
        out = self.obj._constructor(result, index=other_ax, columns=result_index)
        if self.axis == 0:
            out = out.T

        return out
