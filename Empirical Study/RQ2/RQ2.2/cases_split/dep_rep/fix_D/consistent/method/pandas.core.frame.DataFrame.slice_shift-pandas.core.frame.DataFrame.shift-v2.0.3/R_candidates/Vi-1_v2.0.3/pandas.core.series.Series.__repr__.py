    def __repr__(self) -> str:
        """
        Return a string representation for a particular Series.
        """
        # pylint: disable=invalid-repr-returned
        repr_params = fmt.get_series_repr_params()
        return self.to_string(**repr_params)
