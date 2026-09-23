    def searchsorted(
        self,
        v: ArrayLike | object,
        side: Literal["left", "right"] = "left",
        sorter: NumpySorter = None,
    ) -> npt.NDArray[np.intp] | np.intp:

        msg = "searchsorted requires high memory usage."
        warnings.warn(
            msg, PerformanceWarning, stacklevel=find_stack_level(inspect.currentframe())
        )
        if not is_scalar(v):
            v = np.asarray(v)
        v = np.asarray(v)
        return np.asarray(self, dtype=self.dtype.subtype).searchsorted(v, side, sorter)
