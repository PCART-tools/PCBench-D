    @property
    def full_scope(self) -> DeepChainMap:
        """
        Return the full scope for use with passing to engines transparently
        as a mapping.

        Returns
        -------
        vars : DeepChainMap
            All variables in this scope.
        """
        # error: Unsupported operand types for + ("List[Dict[Any, Any]]" and
        # "List[Mapping[Any, Any]]")
        # error: Unsupported operand types for + ("List[Dict[Any, Any]]" and
        # "List[Mapping[str, Any]]")
        maps = (
            [self.temps]
            + self.resolvers.maps  # type: ignore[operator]
            + self.scope.maps  # type: ignore[operator]
        )
        return DeepChainMap(*maps)
