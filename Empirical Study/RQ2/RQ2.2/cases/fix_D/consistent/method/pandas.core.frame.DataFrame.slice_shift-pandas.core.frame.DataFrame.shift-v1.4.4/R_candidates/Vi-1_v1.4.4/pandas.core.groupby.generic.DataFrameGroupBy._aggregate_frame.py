    def _aggregate_frame(self, func, *args, **kwargs) -> DataFrame:
        if self.grouper.nkeys != 1:
            raise AssertionError("Number of keys must be 1")

        obj = self._obj_with_exclusions

        result: dict[Hashable, NDFrame | np.ndarray] = {}
        if self.axis == 0:
            # test_pass_args_kwargs_duplicate_columns gets here with non-unique columns
            for name, data in self:
                fres = func(data, *args, **kwargs)
                result[name] = fres
        else:
            # we get here in a number of test_multilevel tests
            for name in self.indices:
                grp_df = self.get_group(name, obj=obj)
                fres = func(grp_df, *args, **kwargs)
                result[name] = fres

        result_index = self.grouper.result_index
        other_ax = obj.axes[1 - self.axis]
        out = self.obj._constructor(result, index=other_ax, columns=result_index)
        if self.axis == 0:
            out = out.T

        return out
