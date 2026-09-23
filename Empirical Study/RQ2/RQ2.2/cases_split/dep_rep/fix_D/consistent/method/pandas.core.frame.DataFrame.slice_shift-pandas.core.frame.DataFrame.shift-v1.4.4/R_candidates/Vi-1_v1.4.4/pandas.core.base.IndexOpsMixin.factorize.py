    @doc(
        algorithms.factorize,
        values="",
        order="",
        size_hint="",
        sort=textwrap.dedent(
            """\
            sort : bool, default False
                Sort `uniques` and shuffle `codes` to maintain the
                relationship.
            """
        ),
    )
    def factorize(self, sort: bool = False, na_sentinel: int | None = -1):
        return algorithms.factorize(self, sort=sort, na_sentinel=na_sentinel)
