    def _from_backing_data(self, arr: np.ndarray) -> PandasArray:
        return type(self)(arr)
