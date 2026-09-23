    def n_chunks(self, strategy: str = "first") -> int | list[int]:
        """
        Get number of chunks used by the ChunkedArrays of this DataFrame.

        Parameters
        ----------
        strategy : {'first', 'all'}
            Return the number of chunks of the 'first' column,
            or 'all' columns in this DataFrame.


        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, 3, 4],
        ...         "b": [0.5, 4, 10, 13],
        ...         "c": [True, True, False, True],
        ...     }
        ... )
        >>> df.n_chunks()
        1
        >>> df.n_chunks(strategy="all")
        [1, 1, 1]

        """
        if strategy == "first":
            return self._df.n_chunks()
        elif strategy == "all":
            return [s.n_chunks() for s in self.__iter__()]
        else:
            raise ValueError(
                f"Strategy: '{strategy}' not understood. "
                f"Choose one of {{'first',  'all'}}"
            )
