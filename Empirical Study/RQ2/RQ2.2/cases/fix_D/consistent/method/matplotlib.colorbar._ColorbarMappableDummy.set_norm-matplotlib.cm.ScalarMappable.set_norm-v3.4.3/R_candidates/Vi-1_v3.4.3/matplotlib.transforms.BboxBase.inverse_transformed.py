    @_api.deprecated("3.3", alternative="transformed(transform.inverted())")
    def inverse_transformed(self, transform):
        """
        Construct a `Bbox` by statically transforming this one by the inverse
        of *transform*.
        """
        return self.transformed(transform.inverted())
