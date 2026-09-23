    @final
    def swapaxes(self, axis1: Axis, axis2: Axis, copy: bool_t | None = None) -> Self:
        """
        Interchange axes and swap values axes appropriately.

        .. deprecated:: 2.1.0
            ``swapaxes`` is deprecated and will be removed.
            Please use ``transpose`` instead.

        Returns
        -------
        same as input

        Examples
        --------
        Please see examples for :meth:`DataFrame.transpose`.
        """
        warnings.warn(
            # GH#51946
            f"'{type(self).__name__}.swapaxes' is deprecated and "
            "will be removed in a future version. "
            f"Please use '{type(self).__name__}.transpose' instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )

        i = self._get_axis_number(axis1)
        j = self._get_axis_number(axis2)

        if i == j:
            return self.copy(deep=copy and not using_copy_on_write())

        mapping = {i: j, j: i}

        new_axes = [self._get_axis(mapping.get(k, k)) for k in range(self._AXIS_LEN)]
        new_values = self._values.swapaxes(i, j)  # type: ignore[union-attr]
        if self._mgr.is_single_block and isinstance(self._mgr, BlockManager):
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
            if not using_copy_on_write() and copy is not False:
                new_mgr = new_mgr.copy(deep=True)

            return self._constructor(new_mgr).__finalize__(self, method="swapaxes")

        return self._constructor(
            new_values,
            *new_axes,
            # The no-copy case for CoW is handled above
            copy=False,
        ).__finalize__(self, method="swapaxes")
