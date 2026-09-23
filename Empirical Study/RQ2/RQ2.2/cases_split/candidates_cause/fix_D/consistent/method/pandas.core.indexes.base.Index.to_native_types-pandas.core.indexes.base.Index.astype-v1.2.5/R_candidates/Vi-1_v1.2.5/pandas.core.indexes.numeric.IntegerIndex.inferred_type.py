    @property
    def inferred_type(self) -> str:
        """
        Always 'integer' for ``Int64Index`` and ``UInt64Index``
        """
        return "integer"
