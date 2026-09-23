    @property
    def shape(self):
        """
        Return a tuple of the shape of the underlying data.
        """
        # overriding the base Index.shape definition to avoid materializing
        # the values (GH-27384, GH-27775)
        return (len(self),)
