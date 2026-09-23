    def _cython_agg_general(
        self, how: str, alt=None, numeric_only: bool = True, min_count: int = -1
    ):
        output: Dict[base.OutputKey, Union[np.ndarray, DatetimeArray]] = {}
        # Ideally we would be able to enumerate self._iterate_slices and use
        # the index from enumeration as the key of output, but ohlc in particular
        # returns a (n x 4) array. Output requires 1D ndarrays as values, so we
        # need to slice that up into 1D arrays
        idx = 0
        for obj in self._iterate_slices():
            name = obj.name
            is_numeric = is_numeric_dtype(obj.dtype)
            if numeric_only and not is_numeric:
                continue

            result, agg_names = self.grouper.aggregate(
                obj._values, how, min_count=min_count
            )

            if agg_names:
                # e.g. ohlc
                assert len(agg_names) == result.shape[1]
                for result_column, result_name in zip(result.T, agg_names):
                    key = base.OutputKey(label=result_name, position=idx)
                    output[key] = self._try_cast(result_column, obj)
                    idx += 1
            else:
                assert result.ndim == 1
                key = base.OutputKey(label=name, position=idx)
                output[key] = self._try_cast(result, obj)
                idx += 1

        if len(output) == 0:
            raise DataError("No numeric types to aggregate")

        return self._wrap_aggregated_output(output)
