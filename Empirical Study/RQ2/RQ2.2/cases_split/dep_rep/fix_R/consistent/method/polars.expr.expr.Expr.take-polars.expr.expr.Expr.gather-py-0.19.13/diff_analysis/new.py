    @deprecate_renamed_function("gather", version="0.19.14")
    def take(
        self, indices: int | list[int] | Expr | Series | np.ndarray[Any, Any]
    ) -> Self:
        """
        Take values by index.

        .. deprecated:: 0.19.14
            This method has been renamed to :meth:`gather`.

        Parameters
        ----------
        indices
            An expression that leads to a UInt32 dtyped Series.
        """
        return self.gather(indices)
