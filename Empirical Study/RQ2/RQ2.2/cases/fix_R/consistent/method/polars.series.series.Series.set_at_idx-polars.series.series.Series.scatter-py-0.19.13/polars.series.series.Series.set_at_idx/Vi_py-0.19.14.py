    @deprecate_renamed_function("scatter", version="0.19.14")
    @deprecate_renamed_parameter("idx", "indices", version="0.19.14")
    @deprecate_renamed_parameter("value", "values", version="0.19.14")
    def set_at_idx(
        self,
        indices: Series | np.ndarray[Any, Any] | Sequence[int] | int,
        values: (
            int
            | float
            | str
            | bool
            | date
            | datetime
            | Sequence[int]
            | Sequence[float]
            | Sequence[bool]
            | Sequence[str]
            | Sequence[date]
            | Sequence[datetime]
            | Series
            | None
        ),
    ) -> Series:
        """
        Set values at the index locations.

        .. deprecated:: 0.19.14
            This method has been renamed to :meth:`scatter`.

        Parameters
        ----------
        indices
            Integers representing the index locations.
        values
            Replacement values.
        """
        return self.scatter(indices, values)
