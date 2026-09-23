    @deprecate_renamed_function("gather", version="0.19.14")
    @deprecate_renamed_parameter("index", "indices", version="0.19.14")
    def take(
        self,
        indices: Series | list[int] | list[list[int]],
        *,
        null_on_oob: bool = False,
    ) -> Series:
        """
        Take sublists by multiple indices.

        .. deprecated:: 0.19.14
            This method has been renamed to :func:`gather`.

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
