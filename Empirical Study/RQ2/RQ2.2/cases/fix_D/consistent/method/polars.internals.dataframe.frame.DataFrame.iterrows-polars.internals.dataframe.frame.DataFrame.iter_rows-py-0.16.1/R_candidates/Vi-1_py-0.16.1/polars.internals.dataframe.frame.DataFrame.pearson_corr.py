    @typing.no_type_check
    def pearson_corr(self, **kwargs: dict[str, Any]) -> DataFrame:
        """
        Return Pearson product-moment correlation coefficients.

        See numpy corrcoef for more information.

        Notes
        -----
        This functionality requires numpy to be installed.

        Parameters
        ----------
        kwargs
            keyword arguments are passed to numpy corrcoef

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3], "bar": [3, 2, 1], "ham": [7, 8, 9]})
        >>> df.pearson_corr()
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
        return DataFrame(
            np.corrcoef(self, **kwargs),
            schema=self.columns,
        )
