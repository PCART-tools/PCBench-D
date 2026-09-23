    def _reduce_axis1(self, name: str, func, skipna: bool) -> Series:
        """
        Special case for _reduce to try to avoid a potentially-expensive transpose.

        Apply the reduction block-wise along axis=1 and then reduce the resulting
        1D arrays.
        """
        if name == "all":
            result = np.ones(len(self), dtype=bool)
            ufunc = np.logical_and
        elif name == "any":
            result = np.zeros(len(self), dtype=bool)
            # error: Incompatible types in assignment
            # (expression has type "_UFunc_Nin2_Nout1[Literal['logical_or'],
            # Literal[20], Literal[False]]", variable has type
            # "_UFunc_Nin2_Nout1[Literal['logical_and'], Literal[20],
            # Literal[True]]")
            ufunc = np.logical_or  # type: ignore[assignment]
        else:
            raise NotImplementedError(name)

        for arr in self._mgr.arrays:
            middle = func(arr, axis=0, skipna=skipna)
            result = ufunc(result, middle)

        res_ser = self._constructor_sliced(result, index=self.index)
        return res_ser
