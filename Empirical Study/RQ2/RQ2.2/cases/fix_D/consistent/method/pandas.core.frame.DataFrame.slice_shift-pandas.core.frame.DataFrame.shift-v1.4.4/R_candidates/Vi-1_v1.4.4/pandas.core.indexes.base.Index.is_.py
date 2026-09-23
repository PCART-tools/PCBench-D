    @final
    def is_(self, other) -> bool:
        """
        More flexible, faster check like ``is`` but that works through views.

        Note: this is *not* the same as ``Index.identical()``, which checks
        that metadata is also the same.

        Parameters
        ----------
        other : object
            Other object to compare against.

        Returns
        -------
        bool
            True if both have same underlying data, False otherwise.

        See Also
        --------
        Index.identical : Works like ``Index.is_`` but also checks metadata.
        """
        if self is other:
            return True
        elif not hasattr(other, "_id"):
            return False
        elif self._id is None or other._id is None:
            return False
        else:
            return self._id is other._id
