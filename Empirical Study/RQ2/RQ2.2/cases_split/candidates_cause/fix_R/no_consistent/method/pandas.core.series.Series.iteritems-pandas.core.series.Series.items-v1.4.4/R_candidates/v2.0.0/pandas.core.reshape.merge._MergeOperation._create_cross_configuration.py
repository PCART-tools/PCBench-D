    def _create_cross_configuration(
        self, left: DataFrame, right: DataFrame
    ) -> tuple[DataFrame, DataFrame, JoinHow, str]:
        """
        Creates the configuration to dispatch the cross operation to inner join,
        e.g. adding a join column and resetting parameters. Join column is added
        to a new object, no inplace modification

        Parameters
        ----------
        left : DataFrame
        right : DataFrame

        Returns
        -------
            a tuple (left, right, how, cross_col) representing the adjusted
            DataFrames with cross_col, the merge operation set to inner and the column
            to join over.
        """
        cross_col = f"_cross_{uuid.uuid4()}"
        how: JoinHow = "inner"
        return (
            left.assign(**{cross_col: 1}),
            right.assign(**{cross_col: 1}),
            how,
            cross_col,
        )
