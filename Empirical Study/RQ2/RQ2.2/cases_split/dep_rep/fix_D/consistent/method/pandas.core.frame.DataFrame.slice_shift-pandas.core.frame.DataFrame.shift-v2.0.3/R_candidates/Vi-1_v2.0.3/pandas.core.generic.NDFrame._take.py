    def _take(
        self: NDFrameT,
        indices,
        axis: Axis = 0,
        convert_indices: bool_t = True,
    ) -> NDFrameT:
        """
        Internal version of the `take` allowing specification of additional args.

        See the docstring of `take` for full explanation of the parameters.
        """
        if not isinstance(indices, slice):
            indices = np.asarray(indices, dtype=np.intp)
            if (
                axis == 0
                and indices.ndim == 1
                and using_copy_on_write()
                and is_range_indexer(indices, len(self))
            ):
                return self.copy(deep=None)

        new_data = self._mgr.take(
            indices,
            axis=self._get_block_manager_axis(axis),
            verify=True,
            convert_indices=convert_indices,
        )
        return self._constructor(new_data).__finalize__(self, method="take")
