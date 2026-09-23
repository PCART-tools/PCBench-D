    def sql(self, query: str, *, table_name: str = "self") -> DataFrame:
        """
        Execute a SQL query against the DataFrame.

        .. versionadded:: 0.20.24

        .. warning::
            This functionality is considered **unstable**, although it is close to
            being considered stable. It may be changed at any point without it being
            considered a breaking change.

        Parameters
        ----------
        query
            SQL query to execute.
        table_name
            Optionally provide an explicit name for the table that represents the
            calling frame (defaults to "self").

        Notes
        -----
        * The calling frame is automatically registered as a table in the SQL context
          under the name "self". If you want access to the DataFrames and LazyFrames
          found in the current globals, use the top-level :meth:`pl.sql <polars.sql>`.
        * More control over registration and execution behaviour is available by
          using the :class:`SQLContext` object.
        * The SQL query executes in lazy mode before being collected and returned
          as a DataFrame.

        See Also
        --------
        SQLContext

        Examples
        --------
        >>> from datetime import date
        >>> df1 = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, 3],
        ...         "b": ["zz", "yy", "xx"],
        ...         "c": [date(1999, 12, 31), date(2010, 10, 10), date(2077, 8, 8)],
        ...     }
        ... )

        Query the DataFrame using SQL:

        >>> df1.sql("SELECT c, b FROM self WHERE a > 1")
        shape: (2, 2)
        ┌────────────┬─────┐
        │ c          ┆ b   │
        │ ---        ┆ --- │
        │ date       ┆ str │
        ╞════════════╪═════╡
        │ 2010-10-10 ┆ yy  │
        │ 2077-08-08 ┆ xx  │
        └────────────┴─────┘

        Apply transformations to a DataFrame using SQL, aliasing "self" to "frame".

        >>> df1.sql(
        ...     query='''
        ...         SELECT
        ...             a,
        ...             (a % 2 == 0) AS a_is_even,
        ...             CONCAT_WS(':', b, b) AS b_b,
        ...             EXTRACT(year FROM c) AS year,
        ...             0::float4 AS "zero",
        ...         FROM frame
        ...     ''',
        ...     table_name="frame",
        ... )
        shape: (3, 5)
        ┌─────┬───────────┬───────┬──────┬──────┐
        │ a   ┆ a_is_even ┆ b_b   ┆ year ┆ zero │
        │ --- ┆ ---       ┆ ---   ┆ ---  ┆ ---  │
        │ i64 ┆ bool      ┆ str   ┆ i32  ┆ f32  │
        ╞═════╪═══════════╪═══════╪══════╪══════╡
        │ 1   ┆ false     ┆ zz:zz ┆ 1999 ┆ 0.0  │
        │ 2   ┆ true      ┆ yy:yy ┆ 2010 ┆ 0.0  │
        │ 3   ┆ false     ┆ xx:xx ┆ 2077 ┆ 0.0  │
        └─────┴───────────┴───────┴──────┴──────┘
        """
        from polars.sql import SQLContext

        issue_unstable_warning(
            "`sql` is considered **unstable** (although it is close to being considered stable)."
        )
        with SQLContext(register_globals=False, eager=True) as ctx:
            name = table_name if table_name else "self"
            ctx.register(name=name, frame=self)
            return ctx.execute(query)
