    @property
    def asobject(self):
        """Return object Index which contains boxed values.

        .. deprecated:: 0.23.0
            Use ``astype(object)`` instead.

        *this is an internal non-public method*
        """
        warnings.warn("'asobject' is deprecated. Use 'astype(object)'"
                      " instead", FutureWarning, stacklevel=2)
        return self.astype(object)
