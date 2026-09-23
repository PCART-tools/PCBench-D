    def sum(self, *, skipna=True, min_count=0, axis: int | None = 0, **kwargs):
        nv.validate_sum((), kwargs)

        # TODO: do this in validate_sum?
        if "out" in kwargs:
            # np.sum; test_floating_array_numpy_sum
            if kwargs["out"] is not None:
                raise NotImplementedError
            kwargs.pop("out")

        result = masked_reductions.sum(
            self._data,
            self._mask,
            skipna=skipna,
            min_count=min_count,
            axis=axis,
        )
        return self._wrap_reduction_result(
            "sum", result, skipna=skipna, axis=axis, **kwargs
        )
