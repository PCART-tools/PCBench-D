    def suffix_fields(self, suffix: str) -> Expr:
        """
        Add a suffix to all fields name of a struct.

        Notes
        -----
        This only take effects for struct.

        Parameters
        ----------
        suffix
            Suffix to add to the filed name

        Examples
        --------
        >>> df = pl.DataFrame({"x": {"a": 1, "b": 2}})
        >>> df.select(pl.col("x").name.suffix_fields("_suffix")).schema
        OrderedDict({'x': Struct({'a_suffix': Int64, 'b_suffix': Int64})})
        """
        return self._from_pyexpr(self._pyexpr.name_suffix_fields(suffix))
