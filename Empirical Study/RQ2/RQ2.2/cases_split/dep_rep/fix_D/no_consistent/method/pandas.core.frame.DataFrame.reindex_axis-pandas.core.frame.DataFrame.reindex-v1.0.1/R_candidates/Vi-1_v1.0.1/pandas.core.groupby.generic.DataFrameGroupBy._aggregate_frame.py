    def _aggregate_frame(self, func, *args, **kwargs) -> DataFrame:
        if self.grouper.nkeys != 1:
            raise AssertionError("Number of keys must be 1")

        axis = self.axis
        obj = self._obj_with_exclusions

        result: Dict[Union[int, str], Union[NDFrame, np.ndarray]] = {}
        if axis != obj._info_axis_number:
            for name, data in self:
                fres = func(data, *args, **kwargs)
                result[name] = fres
        else:
            for name in self.indices:
                data = self.get_group(name, obj=obj)
                fres = func(data, *args, **kwargs)
                result[name] = fres

        return self._wrap_frame_output(result, obj)
