    def rechunk(self, *, in_place: bool = False) -> Self:
        """
        Create a single chunk of memory for this Series.

        Parameters
        ----------
        in_place
            In place or not.
        """
        opt_s = self._s.rechunk(in_place)
        return self if in_place else self._from_pyseries(opt_s)
