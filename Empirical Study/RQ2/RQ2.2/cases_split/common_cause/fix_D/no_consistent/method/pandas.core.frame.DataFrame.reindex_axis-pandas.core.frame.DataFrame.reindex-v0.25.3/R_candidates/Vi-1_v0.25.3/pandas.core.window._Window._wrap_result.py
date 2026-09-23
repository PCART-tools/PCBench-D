    def _wrap_result(self, result, block=None, obj=None) -> FrameOrSeries:
        """
        Wrap a single result.
        """

        if obj is None:
            obj = self._selected_obj
        index = obj.index

        if isinstance(result, np.ndarray):

            # coerce if necessary
            if block is not None:
                if is_timedelta64_dtype(block.values.dtype):
                    from pandas import to_timedelta

                    result = to_timedelta(result.ravel(), unit="ns").values.reshape(
                        result.shape
                    )

            if result.ndim == 1:
                from pandas import Series

                return Series(result, index, name=obj.name)

            return type(obj)(result, index=index, columns=block.columns)
        return result
