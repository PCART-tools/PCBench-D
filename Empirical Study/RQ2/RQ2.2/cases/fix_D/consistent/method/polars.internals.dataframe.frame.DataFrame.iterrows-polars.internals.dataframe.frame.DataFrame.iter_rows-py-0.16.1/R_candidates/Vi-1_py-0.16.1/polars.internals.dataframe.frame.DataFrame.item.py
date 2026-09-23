    def item(self) -> Any:
        """
        Return the dataframe as a scalar.

        Equivalent to ``df[0,0]``, with a check that the shape is (1,1).

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> result = df.select((pl.col("a") * pl.col("b")).sum())
        >>> result
        shape: (1, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ i64 │
        ╞═════╡
        │ 32  │
        └─────┘
        >>> result.item()
        32

        """
        if self.shape != (1, 1):
            raise ValueError(
                f"Can only call .item() if the dataframe is of shape (1,1), "
                f"dataframe is of shape {self.shape}"
            )
        return self[0, 0]
