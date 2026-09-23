    def _mode(self, dropna: bool = True):
        values = self
        if dropna:
            mask = values.isna()
            values = values[~mask]

        i8modes = mode(values.view("i8"))
        npmodes = i8modes.view(self._ndarray.dtype)
        npmodes = cast(np.ndarray, npmodes)
        return self._from_backing_data(npmodes)
