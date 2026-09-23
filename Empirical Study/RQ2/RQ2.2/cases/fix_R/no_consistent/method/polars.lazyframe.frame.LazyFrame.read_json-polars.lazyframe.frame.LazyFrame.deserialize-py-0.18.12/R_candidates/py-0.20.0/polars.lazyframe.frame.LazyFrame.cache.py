    def cache(self) -> Self:
        """Cache the result once the execution of the physical plan hits this node."""
        return self._from_pyldf(self._ldf.cache())
