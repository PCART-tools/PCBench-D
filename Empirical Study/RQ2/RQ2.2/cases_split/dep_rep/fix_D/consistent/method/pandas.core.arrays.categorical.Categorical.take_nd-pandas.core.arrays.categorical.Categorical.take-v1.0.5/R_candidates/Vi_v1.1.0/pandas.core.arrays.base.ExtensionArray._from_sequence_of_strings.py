    @classmethod
    def _from_sequence_of_strings(cls, strings, dtype=None, copy=False):
        """
        Construct a new ExtensionArray from a sequence of strings.

        .. versionadded:: 0.24.0

        Parameters
        ----------
        strings : Sequence
            Each element will be an instance of the scalar type for this
            array, ``cls.dtype.type``.
        dtype : dtype, optional
            Construct for this particular dtype. This should be a Dtype
            compatible with the ExtensionArray.
        copy : bool, default False
            If True, copy the underlying data.

        Returns
        -------
        ExtensionArray
        """
        raise AbstractMethodError(cls)
