    def _from_backing_data(self, arr: np.ndarray) -> NumpyExtensionArray:
        return type(self)(arr)
