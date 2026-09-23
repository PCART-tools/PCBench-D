    @deprecate_renamed_function("gather", version="0.19.14")
    def take(
        self, indices: int | list[int] | Expr | Series | np.ndarray[Any, Any]
    ) -> Series:
        """
        Take values by index.

        .. deprecated:: 0.19.14
            This method has been renamed to :meth:`gather`.

        Parameters
        ----------
        indices
            Index location used for selection.
        """
        return self.gather(indices)
