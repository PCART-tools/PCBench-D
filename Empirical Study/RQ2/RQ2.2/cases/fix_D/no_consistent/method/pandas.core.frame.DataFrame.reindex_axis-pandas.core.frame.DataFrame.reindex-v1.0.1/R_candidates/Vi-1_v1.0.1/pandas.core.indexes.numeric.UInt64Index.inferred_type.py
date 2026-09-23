    @property
    def inferred_type(self) -> str:
        """
        Always 'integer' for ``UInt64Index``
        """
        return "integer"
