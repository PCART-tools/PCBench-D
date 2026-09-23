    def inverse_transformed(self, transform):
        """
        Return a new :class:`Bbox` object, statically transformed by
        the inverse of the given transform.
        """
        return self.transformed(transform.inverted())
