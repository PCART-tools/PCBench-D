    def convert(
        self: T,
        copy: bool = True,
        datetime: bool = True,
        numeric: bool = True,
        timedelta: bool = True,
    ) -> T:
        def _convert(arr):
            if is_object_dtype(arr.dtype):
                # extract PandasArray for tests that patch PandasArray._typ
                arr = np.asarray(arr)
                return soft_convert_objects(
                    arr,
                    datetime=datetime,
                    numeric=numeric,
                    timedelta=timedelta,
                    copy=copy,
                )
            else:
                return arr.copy() if copy else arr

        return self.apply(_convert)
