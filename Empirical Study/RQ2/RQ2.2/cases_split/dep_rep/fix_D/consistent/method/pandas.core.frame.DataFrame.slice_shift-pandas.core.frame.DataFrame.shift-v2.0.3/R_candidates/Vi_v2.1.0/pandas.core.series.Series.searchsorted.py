    @doc(base.IndexOpsMixin.searchsorted, klass="Series")
    # Signature of "searchsorted" incompatible with supertype "IndexOpsMixin"
    def searchsorted(  # type: ignore[override]
        self,
        value: NumpyValueArrayLike | ExtensionArray,
        side: Literal["left", "right"] = "left",
        sorter: NumpySorter | None = None,
    ) -> npt.NDArray[np.intp] | np.intp:
        return base.IndexOpsMixin.searchsorted(self, value, side=side, sorter=sorter)
