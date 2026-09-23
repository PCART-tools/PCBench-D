    def _validate_fill_value(self, fill_value):
        """
        Convert a user-facing fill_value to a representation to use with our
        underlying ndarray, raising ValueError if this is not possible.

        Parameters
        ----------
        fill_value : object

        Returns
        -------
        fill_value : int

        Raises
        ------
        ValueError
        """

        if isna(fill_value):
            fill_value = -1
        elif fill_value in self.categories:
            fill_value = self.categories.get_loc(fill_value)
        else:
            raise ValueError(
                f"'fill_value={fill_value}' is not present "
                "in this Categorical's categories"
            )
        return fill_value
