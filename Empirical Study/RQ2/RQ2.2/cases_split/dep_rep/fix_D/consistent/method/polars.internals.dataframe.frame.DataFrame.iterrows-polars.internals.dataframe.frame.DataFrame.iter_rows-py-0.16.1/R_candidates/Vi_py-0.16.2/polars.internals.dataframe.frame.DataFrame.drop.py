    def drop(self: DF, columns: str | Sequence[str]) -> DF:
        """
        Remove column from DataFrame and return as new.

        Parameters
        ----------
        columns
            Column(s) to drop.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> df.drop("ham")
        shape: (3, 2)
        ┌─────┬─────┐
        │ foo ┆ bar │
        │ --- ┆ --- │
        │ i64 ┆ f64 │
        ╞═════╪═════╡
        │ 1   ┆ 6.0 │
        │ 2   ┆ 7.0 │
        │ 3   ┆ 8.0 │
        └─────┴─────┘

        """
        if isinstance(columns, list):
            df = self.clone()

            for n in columns:
                df._df.drop_in_place(n)
            return df

        return self._from_pydf(self._df.drop(columns))
