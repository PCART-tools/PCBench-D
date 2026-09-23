    def iter_columns(self) -> Iterator[Series]:
        """
        Returns an iterator over the DataFrame's columns.

        Notes
        -----
        Consider whether you can use :func:`all` instead.
        If you can, it will be more efficient.

        Returns
        -------
        Iterator of Series.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 3, 5],
        ...         "b": [2, 4, 6],
        ...     }
        ... )
        >>> [s.name for s in df.iter_columns()]
        ['a', 'b']

        If you're using this to modify a dataframe's columns, e.g.

        >>> # Do NOT do this
        >>> pl.DataFrame(column * 2 for column in df.iter_columns())
        shape: (3, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 2   ┆ 4   │
        │ 6   ┆ 8   │
        │ 10  ┆ 12  │
        └─────┴─────┘

        then consider whether you can use :func:`all` instead:

        >>> df.select(pl.all() * 2)
        shape: (3, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 2   ┆ 4   │
        │ 6   ┆ 8   │
        │ 10  ┆ 12  │
        └─────┴─────┘

        """
        return (wrap_s(s) for s in self._df.get_columns())
