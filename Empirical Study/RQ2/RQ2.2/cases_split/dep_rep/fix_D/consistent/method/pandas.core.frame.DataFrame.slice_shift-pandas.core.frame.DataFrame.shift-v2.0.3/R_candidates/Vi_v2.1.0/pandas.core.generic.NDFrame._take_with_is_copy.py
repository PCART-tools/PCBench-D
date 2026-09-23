    @final
    def _take_with_is_copy(self, indices, axis: Axis = 0) -> Self:
        """
        Internal version of the `take` method that sets the `_is_copy`
        attribute to keep track of the parent dataframe (using in indexing
        for the SettingWithCopyWarning).

        For Series this does the same as the public take (it never sets `_is_copy`).

        See the docstring of `take` for full explanation of the parameters.
        """
        result = self.take(indices=indices, axis=axis)
        # Maybe set copy if we didn't actually change the index.
        if self.ndim == 2 and not result._get_axis(axis).equals(self._get_axis(axis)):
            result._set_is_copy(self)
        return result
