    def aggregate(self, arg, *args, **kwargs):

        _level = kwargs.pop('_level', None)
        result, how = self._aggregate(arg, _level=_level, *args, **kwargs)
        if how is None:
            return result

        if result is None:

            # grouper specific aggregations
            if self.grouper.nkeys > 1:
                return self._python_agg_general(arg, *args, **kwargs)
            else:

                # try to treat as if we are passing a list
                try:
                    assert not args and not kwargs
                    result = self._aggregate_multiple_funcs(
                        [arg], _level=_level)
                    result.columns = Index(
                        result.columns.levels[0],
                        name=self._selected_obj.columns.name)
                except:
                    result = self._aggregate_generic(arg, *args, **kwargs)

        if not self.as_index:
            self._insert_inaxis_grouper_inplace(result)
            result.index = np.arange(len(result))

        return result._convert(datetime=True)
