    def cache(self) -> LazyFrame:
        """
        Cache the result once the execution of the physical plan hits this node.

        It is not recommended using this as the optimizer likely can do a better job.
        """
        return self._from_pyldf(self._ldf.cache())
