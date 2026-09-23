    def _can_union_without_object_cast(self, other) -> bool:
        """
        Check whether this and the other dtype are compatible with each other.
        Meaning a union can be formed between them without needing to be cast
        to dtype object.

        Parameters
        ----------
        other : Index or array-like

        Returns
        -------
        bool
        """
        return type(self) is type(other) and is_dtype_equal(self.dtype, other.dtype)
