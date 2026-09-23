    def has_validity(self) -> bool:
        """
        Return True if the Series has a validity bitmask.

        If there is no mask, it means that there are no `null` values.

        Notes
        -----
        While the *absence* of a validity bitmask guarantees that a Series does not
        have `null` values, the converse is not true, eg: the *presence* of a
        bitmask does not mean that there are null values, as every value of the
        bitmask could be `false`.

        To confirm that a column has `null` values use :func:`null_count`.
        """
        return self._s.has_validity()
