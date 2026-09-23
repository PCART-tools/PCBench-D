    def corr(self, **kwargs: Any) -> DataFrame:
        """
        Return pairwise Pearson product-moment correlation coefficients between columns.

        See numpy `corrcoef` for more information:
        https://numpy.org/doc/stable/reference/generated/numpy.corrcoef.html

        Notes
        -----
        This functionality requires numpy to be installed.

        Parameters
        ----------
        **kwargs
            Keyword arguments are passed to numpy `corrcoef`.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3], "bar": [3, 2, 1], "ham": [7, 8, 9]})
        >>> df.corr()
        shape: (3, 3)
        ┌──────┬──────┬──────┐
        │ foo  ┆ bar  ┆ ham  │
        │ ---  ┆ ---  ┆ ---  │
        │ f64  ┆ f64  ┆ f64  │
        ╞══════╪══════╪══════╡
        │ 1.0  ┆ -1.0 ┆ 1.0  │
        │ -1.0 ┆ 1.0  ┆ -1.0 │
        │ 1.0  ┆ -1.0 ┆ 1.0  │
        └──────┴──────┴──────┘

        """
        return DataFrame(np.corrcoef(self.to_numpy().T, **kwargs), schema=self.columns)
