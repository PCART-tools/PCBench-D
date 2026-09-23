    def to_list(self, *, use_pyarrow: bool | None = None) -> list[Any]:
        """
        Convert this Series to a Python List. This operation clones data.

        Parameters
        ----------
        use_pyarrow
            Use pyarrow for the conversion.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.to_list()
        [1, 2, 3]
        >>> type(s.to_list())
        <class 'list'>

        """
        if use_pyarrow is not None:
            issue_deprecation_warning(
                "The parameter `use_pyarrow` for `Series.to_list` is deprecated."
                " Call the method without `use_pyarrow` to silence this warning.",
                version="0.19.9",
            )
            if use_pyarrow:
                return self.to_arrow().to_pylist()

        return self._s.to_list()
