    @classmethod
    def _from_sequence(cls, scalars):
        """Construct a new ExtensionArray from a sequence of scalars.

        Parameters
        ----------
        scalars : Sequence
            Each element will be an instance of the scalar type for this
            array, ``cls.dtype.type``.
        Returns
        -------
        ExtensionArray
        """
        raise AbstractMethodError(cls)
