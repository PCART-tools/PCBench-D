    def convert(self: T, copy: bool | None) -> T:
        if copy is None:
            copy = True

        def _convert(arr):
            if is_object_dtype(arr.dtype):
                # extract PandasArray for tests that patch PandasArray._typ
                arr = np.asarray(arr)
                result = lib.maybe_convert_objects(
                    arr,
                    convert_datetime=True,
                    convert_timedelta=True,
                    convert_period=True,
                    convert_interval=True,
                )
                if result is arr and copy:
                    return arr.copy()
                return result
            else:
                return arr.copy() if copy else arr

        return self.apply(_convert)
