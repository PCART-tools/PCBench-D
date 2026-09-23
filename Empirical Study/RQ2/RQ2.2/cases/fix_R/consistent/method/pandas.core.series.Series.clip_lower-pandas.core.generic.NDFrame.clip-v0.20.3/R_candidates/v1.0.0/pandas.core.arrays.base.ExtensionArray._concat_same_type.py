    @classmethod
    def _concat_same_type(
        cls, to_concat: Sequence[ABCExtensionArray]
    ) -> ABCExtensionArray:
        """
        Concatenate multiple array.

        Parameters
        ----------
        to_concat : sequence of this type

        Returns
        -------
        ExtensionArray
        """
        raise AbstractMethodError(cls)
