    @final
    def _mpl_repr(self) -> np.ndarray:
        # how to represent ourselves to matplotlib
        if isinstance(self.dtype, np.dtype) and self.dtype.kind != "M":
            return cast(np.ndarray, self.values)
        return self.astype(object, copy=False)._values
