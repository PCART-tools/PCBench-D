    def _quantile(self, qs: npt.NDArray[np.float64], interpolation: str):
        # Special case: the returned array isn't _really_ sparse, so we don't
        #  wrap it in a SparseArray
        result = super()._quantile(qs, interpolation)
        return np.asarray(result)
