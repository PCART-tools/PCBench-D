    @final
    @doc(position="first", klass=_shared_doc_kwargs["klass"])
    def first_valid_index(self) -> Hashable | None:
        """
        Return index for {position} non-NA value or None, if no non-NA value is found.

        Returns
        -------
        scalar : type of index

        Notes
        -----
        If all elements are non-NA/null, returns None.
        Also returns None for empty {klass}.
        """
        return self._find_valid_index(how="first")
