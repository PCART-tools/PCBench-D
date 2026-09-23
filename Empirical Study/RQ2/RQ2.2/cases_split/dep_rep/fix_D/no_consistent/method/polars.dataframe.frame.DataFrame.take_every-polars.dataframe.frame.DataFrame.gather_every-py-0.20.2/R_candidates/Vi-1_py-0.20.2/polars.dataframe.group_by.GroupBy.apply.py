    @deprecate_renamed_function("map_groups", version="0.19.0")
    def apply(self, function: Callable[[DataFrame], DataFrame]) -> DataFrame:
        """
        Apply a custom/user-defined function (UDF) over the groups as a sub-DataFrame.

        .. deprecated:: 0.19.0
            This method has been renamed to :func:`GroupBy.map_groups`.

        Parameters
        ----------
        function
            Custom function.

        """
        return self.map_groups(function)
