    @final
    @property
    def shape(self) -> Shape:
        """
        Return a tuple of the shape of the underlying data.
        """
        # See GH#27775, GH#27384 for history/reasoning in how this is defined.
        return (len(self),)
