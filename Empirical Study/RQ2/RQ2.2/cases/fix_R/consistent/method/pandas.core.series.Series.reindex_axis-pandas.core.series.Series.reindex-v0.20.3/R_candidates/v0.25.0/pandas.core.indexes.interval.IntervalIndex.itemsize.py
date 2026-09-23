    @property
    def itemsize(self):
        msg = (
            "IntervalIndex.itemsize is deprecated and will be removed in "
            "a future version"
        )
        warnings.warn(msg, FutureWarning, stacklevel=2)

        # suppress the warning from the underlying left/right itemsize
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return self.left.itemsize + self.right.itemsize
