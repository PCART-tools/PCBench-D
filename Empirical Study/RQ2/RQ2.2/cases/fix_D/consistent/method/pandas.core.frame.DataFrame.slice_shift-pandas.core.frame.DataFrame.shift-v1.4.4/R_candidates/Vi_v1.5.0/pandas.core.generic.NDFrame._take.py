    def _take(
        self: NDFrameT,
        indices,
        axis=0,
        convert_indices: bool_t = True,
    ) -> NDFrameT:
        """
        Internal version of the `take` allowing specification of additional args.

        See the docstring of `take` for full explanation of the parameters.
        """
        self._consolidate_inplace()

        new_data = self._mgr.take(
            indices,
            axis=self._get_block_manager_axis(axis),
            verify=True,
            convert_indices=convert_indices,
        )
        return self._constructor(new_data).__finalize__(self, method="take")
