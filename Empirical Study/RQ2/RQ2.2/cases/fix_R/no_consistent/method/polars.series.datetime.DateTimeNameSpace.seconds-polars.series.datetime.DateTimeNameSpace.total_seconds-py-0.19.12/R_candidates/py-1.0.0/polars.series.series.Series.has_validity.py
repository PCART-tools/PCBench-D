    @deprecate_function(
        "Use `has_nulls` instead to check for the presence of null values.",
        version="0.20.30",
    )
    def has_validity(self) -> bool:
        """
        Return True if the Series has a validity bitmask.

        .. deprecated:: 0.20.30
            Use :meth:`has_nulls` instead.

        If there is no mask, it means that there are no `null` values.

        Notes
        -----
        While the *absence* of a validity bitmask guarantees that a Series does not
        have `null` values, the converse is not true, eg: the *presence* of a
        bitmask does not mean that there are null values, as every value of the
        bitmask could be `false`.

        To confirm that a column has `null` values use :meth:`has_nulls`.
        """
        return self._s.has_validity()
