    def _aggregate_generic(self, func, *args, **kwargs):
        if self.grouper.nkeys != 1:
            raise AssertionError('Number of keys must be 1')

        axis = self.axis
        obj = self._obj_with_exclusions

        result = {}
        if axis != obj._info_axis_number:
            try:
                for name, data in self:
                    result[name] = self._try_cast(func(data, *args, **kwargs),
                                                  data)
            except Exception:
                return self._aggregate_item_by_item(func, *args, **kwargs)
        else:
            for name in self.indices:
                try:
                    data = self.get_group(name, obj=obj)
                    result[name] = self._try_cast(func(data, *args, **kwargs),
                                                  data)
                except Exception:
                    wrapper = lambda x: func(x, *args, **kwargs)
                    result[name] = data.apply(wrapper, axis=axis)

        return self._wrap_generic_output(result, obj)
