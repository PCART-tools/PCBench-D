    def _take_with_is_copy(self: NDFrameT, indices, axis: Axis = 0) -> NDFrameT:
        """
        Internal version of the `take` method that sets the `_is_copy`
        attribute to keep track of the parent dataframe (using in indexing
        for the SettingWithCopyWarning).

        See the docstring of `take` for full explanation of the parameters.
        """
        result = self._take(indices=indices, axis=axis)
        # Maybe set copy if we didn't actually change the index.
        if not result._get_axis(axis).equals(self._get_axis(axis)):
            result._set_is_copy(self)
        return result
