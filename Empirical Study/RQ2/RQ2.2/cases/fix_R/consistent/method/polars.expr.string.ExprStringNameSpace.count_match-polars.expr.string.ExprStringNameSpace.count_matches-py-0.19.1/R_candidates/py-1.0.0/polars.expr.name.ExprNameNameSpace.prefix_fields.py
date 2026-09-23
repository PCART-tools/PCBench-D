    def prefix_fields(self, prefix: str) -> Expr:
        """
        Add a prefix to all fields name of a struct.

        Notes
        -----
        This only take effects for struct.

        Parameters
        ----------
        prefix
            Prefix to add to the filed name

        Examples
        --------
        >>> df = pl.DataFrame({"x": {"a": 1, "b": 2}})
        >>> df.select(pl.col("x").name.prefix_fields("prefix_")).schema
        Schema({'x': Struct({'prefix_a': Int64, 'prefix_b': Int64})})
        """
        return self._from_pyexpr(self._pyexpr.name_prefix_fields(prefix))
