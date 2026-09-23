    @staticmethod
    def validate_ordered(ordered: OrderedType) -> None:
        """
        Validates that we have a valid ordered parameter. If
        it is not a boolean, a TypeError will be raised.

        Parameters
        ----------
        ordered : object
            The parameter to be verified.

        Raises
        ------
        TypeError
            If 'ordered' is not a boolean.
        """
        from pandas.core.dtypes.common import is_bool

        if not is_bool(ordered):
            raise TypeError("'ordered' must either be 'True' or 'False'")
