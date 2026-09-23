    @property
    def kind(self):
        """
        The sparse kind. Either 'integer', or 'block'.
        """
        return self.subtype.kind
