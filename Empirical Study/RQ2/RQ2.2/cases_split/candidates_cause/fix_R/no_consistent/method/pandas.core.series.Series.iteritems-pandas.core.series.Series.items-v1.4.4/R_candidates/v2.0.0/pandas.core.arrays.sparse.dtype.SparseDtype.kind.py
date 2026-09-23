    @property
    def kind(self) -> str:
        """
        The sparse kind. Either 'integer', or 'block'.
        """
        return self.subtype.kind
