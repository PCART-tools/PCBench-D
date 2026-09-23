    def _reindex_indexer(
        self,
        new_axis,
        indexer: npt.NDArray[np.intp] | None,
        axis: AxisInt,
        fill_value=None,
        allow_dups: bool = False,
        copy: bool | None = True,
        use_na_proxy: bool = False,
    ) -> Self:
        """
        Parameters
        ----------
        new_axis : Index
        indexer : ndarray[intp] or None
        axis : int
        fill_value : object, default None
        allow_dups : bool, default False
        copy : bool, default True


        pandas-indexer with -1's only.
        """
        if copy is None:
            # ArrayManager does not yet support CoW, so deep=None always means
            # deep=True for now
            copy = True

        if indexer is None:
            if new_axis is self._axes[axis] and not copy:
                return self

            result = self.copy(deep=copy)
            result._axes = list(self._axes)
            result._axes[axis] = new_axis
            return result

        # some axes don't allow reindexing with dups
        if not allow_dups:
            self._axes[axis]._validate_can_reindex(indexer)

        if axis >= self.ndim:
            raise IndexError("Requested axis not found in manager")

        if axis == 1:
            new_arrays = []
            for i in indexer:
                if i == -1:
                    arr = self._make_na_array(
                        fill_value=fill_value, use_na_proxy=use_na_proxy
                    )
                else:
                    arr = self.arrays[i]
                    if copy:
                        arr = arr.copy()
                new_arrays.append(arr)

        else:
            validate_indices(indexer, len(self._axes[0]))
            indexer = ensure_platform_int(indexer)
            mask = indexer == -1
            needs_masking = mask.any()
            new_arrays = [
                take_1d(
                    arr,
                    indexer,
                    allow_fill=needs_masking,
                    fill_value=fill_value,
                    mask=mask,
                    # if fill_value is not None else blk.fill_value
                )
                for arr in self.arrays
            ]

        new_axes = list(self._axes)
        new_axes[axis] = new_axis

        return type(self)(new_arrays, new_axes, verify_integrity=False)
