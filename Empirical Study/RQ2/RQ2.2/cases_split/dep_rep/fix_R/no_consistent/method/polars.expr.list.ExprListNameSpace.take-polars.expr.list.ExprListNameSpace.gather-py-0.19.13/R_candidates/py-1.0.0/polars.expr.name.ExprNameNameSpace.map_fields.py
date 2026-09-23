    def map_fields(self, function: Callable[[str], str]) -> Expr:
        """
        Rename fields of a struct by mapping a function over the field name.

        Notes
        -----
        This only take effects for struct.

        Parameters
        ----------
        function
            Function that maps a field name to a new name.

        Examples
        --------
        >>> df = pl.DataFrame({"x": {"a": 1, "b": 2}})
        >>> df.select(pl.col("x").name.map_fields(lambda x: x.upper())).schema
        Schema({'x': Struct({'A': Int64, 'B': Int64})})
        """
        return self._from_pyexpr(self._pyexpr.name_map_fields(function))
