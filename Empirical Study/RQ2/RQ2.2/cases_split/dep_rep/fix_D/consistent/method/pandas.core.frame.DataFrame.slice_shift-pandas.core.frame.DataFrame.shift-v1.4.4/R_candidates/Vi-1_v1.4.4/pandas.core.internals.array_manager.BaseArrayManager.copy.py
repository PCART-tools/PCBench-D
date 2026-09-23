    def copy(self: T, deep=True) -> T:
        """
        Make deep or shallow copy of ArrayManager

        Parameters
        ----------
        deep : bool or string, default True
            If False, return shallow copy (do not copy data)
            If 'all', copy data and a deep copy of the index

        Returns
        -------
        BlockManager
        """
        # this preserves the notion of view copying of axes
        if deep:
            # hit in e.g. tests.io.json.test_pandas

            def copy_func(ax):
                return ax.copy(deep=True) if deep == "all" else ax.view()

            new_axes = [copy_func(ax) for ax in self._axes]
        else:
            new_axes = list(self._axes)

        if deep:
            new_arrays = [arr.copy() for arr in self.arrays]
        else:
            new_arrays = list(self.arrays)
        return type(self)(new_arrays, new_axes, verify_integrity=False)
