    @final
    def swapaxes(
        self: NDFrameT, axis1: Axis, axis2: Axis, copy: bool_t | None = None
    ) -> NDFrameT:
        """
        Interchange axes and swap values axes appropriately.

        Returns
        -------
        same as input
        """
        i = self._get_axis_number(axis1)
        j = self._get_axis_number(axis2)

        if i == j:
            return self.copy(deep=copy and not using_copy_on_write())

        mapping = {i: j, j: i}

        new_axes = [self._get_axis(mapping.get(k, k)) for k in range(self._AXIS_LEN)]
        new_values = self._values.swapaxes(i, j)  # type: ignore[union-attr]
        if (
            using_copy_on_write()
            and self._mgr.is_single_block
            and isinstance(self._mgr, BlockManager)
        ):
            # This should only get hit in case of having a single block, otherwise a
            # copy is made, we don't have to set up references.
            new_mgr = ndarray_to_mgr(
                new_values,
                new_axes[0],
                new_axes[1],
                dtype=None,
                copy=False,
                typ="block",
            )
            assert isinstance(new_mgr, BlockManager)
            assert isinstance(self._mgr, BlockManager)
            new_mgr.blocks[0].refs = self._mgr.blocks[0].refs
            new_mgr.blocks[0].refs.add_reference(
                new_mgr.blocks[0]  # type: ignore[arg-type]
            )
            return self._constructor(new_mgr).__finalize__(self, method="swapaxes")

        elif (copy or copy is None) and self._mgr.is_single_block:
            new_values = new_values.copy()

        return self._constructor(
            new_values,
            *new_axes,
            # The no-copy case for CoW is handled above
            copy=False,
        ).__finalize__(self, method="swapaxes")
