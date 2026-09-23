    @property
    def inferred_type(self) -> str:
        """
        Always 'floating' for ``Float64Index``
        """
        return "floating"
