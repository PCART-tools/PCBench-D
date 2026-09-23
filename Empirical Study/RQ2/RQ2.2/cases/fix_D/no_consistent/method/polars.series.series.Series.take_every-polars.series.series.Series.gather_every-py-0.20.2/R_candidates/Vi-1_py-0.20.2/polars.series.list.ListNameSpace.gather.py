    def gather(
        self,
        indices: Series | list[int] | list[list[int]],
        *,
        null_on_oob: bool = False,
    ) -> Series:
        """
        Take sublists by multiple indices.

        The indices may be defined in a single column, or by sublists in another
        column of dtype `List`.

        Parameters
        ----------
        indices
            Indices to return per sublist
        null_on_oob
            Behavior if an index is out of bounds:
            True -> set as null
            False -> raise an error
            Note that defaulting to raising an error is much cheaper
        """
