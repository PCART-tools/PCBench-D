    def _transform_general(
        self, func: Callable, engine, engine_kwargs, *args, **kwargs
    ) -> Series:
        """
        Transform with a callable `func`.
        """
        if maybe_use_numba(engine):
            return self._transform_with_numba(
                func, *args, engine_kwargs=engine_kwargs, **kwargs
            )
        assert callable(func)
        klass = type(self.obj)

        results = []
        for name, group in self.grouper.get_iterator(
            self._selected_obj, axis=self.axis
        ):
            # this setattr is needed for test_transform_lambda_with_datetimetz
            object.__setattr__(group, "name", name)
            res = func(group, *args, **kwargs)

            results.append(klass(res, index=group.index))

        # check for empty "results" to avoid concat ValueError
        if results:
            from pandas.core.reshape.concat import concat

            concatenated = concat(results)
            result = self._set_result_index_ordered(concatenated)
        else:
            result = self.obj._constructor(dtype=np.float64)

        result.name = self.obj.name
        return result
