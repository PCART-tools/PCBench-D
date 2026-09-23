    @property
    def _is_homogeneous_type(self):
        """
        Whether the object has a single dtype.

        By definition, Series and Index are always considered homogeneous.
        A MultiIndex may or may not be homogeneous, depending on the
        dtypes of the levels.

        See Also
        --------
        DataFrame._is_homogeneous_type
        MultiIndex._is_homogeneous_type
        """
        return True
