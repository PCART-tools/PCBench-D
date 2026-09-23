    def profile(
        self,
        *,
        type_coercion: bool = True,
        predicate_pushdown: bool = True,
        projection_pushdown: bool = True,
        simplify_expression: bool = True,
        no_optimization: bool = False,
        slice_pushdown: bool = True,
        comm_subplan_elim: bool = True,
        comm_subexpr_elim: bool = True,
        show_plot: bool = False,
        truncate_nodes: int = 0,
        figsize: tuple[int, int] = (18, 8),
        streaming: bool = False,
    ) -> tuple[DataFrame, DataFrame]:
        """
        Profile a LazyFrame.

        This will run the query and return a tuple
        containing the materialized DataFrame and a DataFrame that
        contains profiling information of each node that is executed.

        The units of the timings are microseconds.

        Parameters
        ----------
        type_coercion
            Do type coercion optimization.
        predicate_pushdown
            Do predicate pushdown optimization.
        projection_pushdown
            Do projection pushdown optimization.
        simplify_expression
            Run simplify expressions optimization.
        no_optimization
            Turn off (certain) optimizations.
        slice_pushdown
            Slice pushdown optimization.
        comm_subplan_elim
            Will try to cache branching subplans that occur on self-joins or unions.
        comm_subexpr_elim
            Common subexpressions will be cached and reused.
        show_plot
            Show a gantt chart of the profiling result
        truncate_nodes
            Truncate the label lengths in the gantt chart to this number of
            characters.
        figsize
            matplotlib figsize of the profiling plot
        streaming
            Run parts of the query in a streaming fashion (this is in an alpha state)

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": ["a", "b", "a", "b", "b", "c"],
        ...         "b": [1, 2, 3, 4, 5, 6],
        ...         "c": [6, 5, 4, 3, 2, 1],
        ...     }
        ... )
        >>> lf.group_by("a", maintain_order=True).agg(pl.all().sum()).sort(
        ...     "a"
        ... ).profile()  # doctest: +SKIP
        (shape: (3, 3)
         ┌─────┬─────┬─────┐
         │ a   ┆ b   ┆ c   │
         │ --- ┆ --- ┆ --- │
         │ str ┆ i64 ┆ i64 │
         ╞═════╪═════╪═════╡
         │ a   ┆ 4   ┆ 10  │
         │ b   ┆ 11  ┆ 10  │
         │ c   ┆ 6   ┆ 1   │
         └─────┴─────┴─────┘,
         shape: (3, 3)
         ┌─────────────────────────┬───────┬──────┐
         │ node                    ┆ start ┆ end  │
         │ ---                     ┆ ---   ┆ ---  │
         │ str                     ┆ u64   ┆ u64  │
         ╞═════════════════════════╪═══════╪══════╡
         │ optimization            ┆ 0     ┆ 5    │
         │ group_by_partitioned(a) ┆ 5     ┆ 470  │
         │ sort(a)                 ┆ 475   ┆ 1964 │
         └─────────────────────────┴───────┴──────┘)

        """
        if no_optimization:
            predicate_pushdown = False
            projection_pushdown = False
            comm_subplan_elim = False
            comm_subexpr_elim = False

        ldf = self._ldf.optimization_toggle(
            type_coercion,
            predicate_pushdown,
            projection_pushdown,
            simplify_expression,
            slice_pushdown,
            comm_subplan_elim,
            comm_subexpr_elim,
            streaming,
            _eager=False,
        )
        df, timings = ldf.profile()
        (df, timings) = wrap_df(df), wrap_df(timings)

        if show_plot:
            try:
                import matplotlib.pyplot as plt

                fig, ax = plt.subplots(1, figsize=figsize)

                max_val = timings["end"][-1]
                timings_ = timings.reverse()

                if max_val > 1e9:
                    unit = "s"
                    timings_ = timings_.with_columns(
                        F.col(["start", "end"]) / 1_000_000
                    )
                elif max_val > 1e6:
                    unit = "ms"
                    timings_ = timings_.with_columns(F.col(["start", "end"]) / 1000)
                else:
                    unit = "us"
                if truncate_nodes > 0:
                    timings_ = timings_.with_columns(
                        F.col("node").str.slice(0, truncate_nodes) + "..."
                    )

                max_in_unit = timings_["end"][0]
                ax.barh(
                    timings_["node"],
                    width=timings_["end"] - timings_["start"],
                    left=timings_["start"],
                )

                plt.title("Profiling result")
                ax.set_xlabel(f"node duration in [{unit}], total {max_in_unit}{unit}")
                ax.set_ylabel("nodes")
                plt.show()

            except ImportError:
                raise ModuleNotFoundError(
                    "matplotlib should be installed to show profiling plot"
                ) from None

        return df, timings
