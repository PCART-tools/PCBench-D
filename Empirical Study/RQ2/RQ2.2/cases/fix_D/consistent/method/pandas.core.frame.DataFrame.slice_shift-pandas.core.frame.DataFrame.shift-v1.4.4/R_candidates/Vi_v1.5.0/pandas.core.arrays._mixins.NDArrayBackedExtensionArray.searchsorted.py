    @doc(ExtensionArray.searchsorted)
    def searchsorted(
        self,
        value: NumpyValueArrayLike | ExtensionArray,
        side: Literal["left", "right"] = "left",
        sorter: NumpySorter = None,
    ) -> npt.NDArray[np.intp] | np.intp:
        # TODO(2.0): use _validate_setitem_value once dt64tz mismatched-timezone
        #  deprecation is enforced
        npvalue = self._validate_searchsorted_value(value)
        return self._ndarray.searchsorted(npvalue, side=side, sorter=sorter)
