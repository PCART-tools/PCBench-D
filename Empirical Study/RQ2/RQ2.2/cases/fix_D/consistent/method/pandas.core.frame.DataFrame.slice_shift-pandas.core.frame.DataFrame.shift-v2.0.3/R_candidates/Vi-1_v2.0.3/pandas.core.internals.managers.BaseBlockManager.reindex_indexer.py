    def reindex_indexer(
        self: T,
        new_axis: Index,
        indexer: npt.NDArray[np.intp] | None,
        axis: AxisInt,
        fill_value=None,
        allow_dups: bool = False,
        copy: bool | None = True,
        only_slice: bool = False,
        *,
        use_na_proxy: bool = False,
    ) -> T:
        """
        Parameters
        ----------
        new_axis : Index
        indexer : ndarray[intp] or None
        axis : int
        fill_value : object, default None
        allow_dups : bool, default False
        copy : bool or None, default True
            If None, regard as False to get shallow copy.
        only_slice : bool, default False
            Whether to take views, not copies, along columns.
        use_na_proxy : bool, default False
            Whether to use a np.void ndarray for newly introduced columns.

        pandas-indexer with -1's only.
        """
        if copy is None:
            if using_copy_on_write():
                # use shallow copy
                copy = False
            else:
                # preserve deep copy for BlockManager with copy=None
                copy = True

        if indexer is None:
            if new_axis is self.axes[axis] and not copy:
                return self

            result = self.copy(deep=copy)
            result.axes = list(self.axes)
            result.axes[axis] = new_axis
            return result

        # Should be intp, but in some cases we get int64 on 32bit builds
        assert isinstance(indexer, np.ndarray)

        # some axes don't allow reindexing with dups
        if not allow_dups:
            self.axes[axis]._validate_can_reindex(indexer)

        if axis >= self.ndim:
            raise IndexError("Requested axis not found in manager")

        if axis == 0:
            new_blocks = self._slice_take_blocks_ax0(
                indexer,
                fill_value=fill_value,
                only_slice=only_slice,
                use_na_proxy=use_na_proxy,
            )
        else:
            new_blocks = [
                blk.take_nd(
                    indexer,
                    axis=1,
                    fill_value=(
                        fill_value if fill_value is not None else blk.fill_value
                    ),
                )
                for blk in self.blocks
            ]

        new_axes = list(self.axes)
        new_axes[axis] = new_axis

        new_mgr = type(self).from_blocks(new_blocks, new_axes)
        if axis == 1:
            # We can avoid the need to rebuild these
            new_mgr._blknos = self.blknos.copy()
            new_mgr._blklocs = self.blklocs.copy()
        return new_mgr
