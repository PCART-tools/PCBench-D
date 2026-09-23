    @property
    def type(self) -> Type[np.generic]:
        """
        The type object used to instantiate a scalar of this NumPy data-type.
        """
        return self._dtype.type
