    @classmethod
    def deserialize(cls, source: str | Path | IOBase) -> Self:
        """
        Read a serialized expression from a file.

        Parameters
        ----------
        source
            Path to a file or a file-like object (by file-like object, we refer to
            objects that have a `read()` method, such as a file handler (e.g.
            via builtin `open` function) or `BytesIO`).

        Warnings
        --------
        This function uses :mod:`pickle` when the logical plan contains Python UDFs,
        and as such inherits the security implications. Deserializing can execute
        arbitrary code, so it should only be attempted on trusted data.

        See Also
        --------
        Expr.meta.serialize

        Examples
        --------
        >>> from io import StringIO
        >>> expr = pl.col("foo").sum().over("bar")
        >>> json = expr.meta.serialize()
        >>> pl.Expr.deserialize(StringIO(json))  # doctest: +ELLIPSIS
        <Expr ['col("foo").sum().over([col("ba…'] at ...>
        """
        if isinstance(source, StringIO):
            source = BytesIO(source.getvalue().encode())
        elif isinstance(source, (str, Path)):
            source = normalize_filepath(source)

        expr = cls.__new__(cls)
        expr._pyexpr = PyExpr.deserialize(source)
        return expr
