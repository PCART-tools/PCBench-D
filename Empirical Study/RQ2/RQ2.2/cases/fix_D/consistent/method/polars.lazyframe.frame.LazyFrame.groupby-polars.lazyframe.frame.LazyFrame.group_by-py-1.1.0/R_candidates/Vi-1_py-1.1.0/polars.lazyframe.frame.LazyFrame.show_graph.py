    def show_graph(
        self,
        *,
        optimized: bool = True,
        show: bool = True,
        output_path: str | Path | None = None,
        raw_output: bool = False,
        figsize: tuple[float, float] = (16.0, 12.0),
        type_coercion: bool = True,
        predicate_pushdown: bool = True,
        projection_pushdown: bool = True,
        simplify_expression: bool = True,
        slice_pushdown: bool = True,
        comm_subplan_elim: bool = True,
        comm_subexpr_elim: bool = True,
        cluster_with_columns: bool = True,
        streaming: bool = False,
    ) -> str | None:
        """
        Show a plot of the query plan.

        Note that graphviz must be installed to render the visualization (if not
        already present you can download it here: <https://graphviz.org/download>`_).

        Parameters
        ----------
        optimized
            Optimize the query plan.
        show
            Show the figure.
        output_path
            Write the figure to disk.
        raw_output
            Return dot syntax. This cannot be combined with `show` and/or `output_path`.
        figsize
            Passed to matplotlib if `show` == True.
        type_coercion
            Do type coercion optimization.
        predicate_pushdown
            Do predicate pushdown optimization.
        projection_pushdown
            Do projection pushdown optimization.
        simplify_expression
            Run simplify expressions optimization.
        slice_pushdown
            Slice pushdown optimization.
        comm_subplan_elim
            Will try to cache branching subplans that occur on self-joins or unions.
        comm_subexpr_elim
            Common subexpressions will be cached and reused.
        cluster_with_columns
            Combine sequential independent calls to with_columns
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
        ... ).show_graph()  # doctest: +SKIP
        """
        _ldf = self._ldf.optimization_toggle(
            type_coercion,
            predicate_pushdown,
            projection_pushdown,
            simplify_expression,
            slice_pushdown,
            comm_subplan_elim,
            comm_subexpr_elim,
            cluster_with_columns,
            streaming,
            _eager=False,
            new_streaming=False,
        )

        dot = _ldf.to_dot(optimized)

        if raw_output:
            # we do not show a graph, nor save a graph to disk
            return dot

        output_type = "svg" if _in_notebook() else "png"

        try:
            graph = subprocess.check_output(
                ["dot", "-Nshape=box", "-T" + output_type], input=f"{dot}".encode()
            )
        except (ImportError, FileNotFoundError):
            msg = (
                "The graphviz `dot` binary should be on your PATH."
                "(If not installed you can download here: https://graphviz.org/download/)"
            )
            raise ImportError(msg) from None

        if output_path:
            Path(output_path).write_bytes(graph)

        if not show:
            return None

        if _in_notebook():
            from IPython.display import SVG, display

            return display(SVG(graph))
        else:
            import_optional(
                "matplotlib",
                err_prefix="",
                err_suffix="should be installed to show graphs",
            )
            import matplotlib.image as mpimg
            import matplotlib.pyplot as plt

            plt.figure(figsize=figsize)
            img = mpimg.imread(BytesIO(graph))
            plt.imshow(img)
            plt.show()
            return None
