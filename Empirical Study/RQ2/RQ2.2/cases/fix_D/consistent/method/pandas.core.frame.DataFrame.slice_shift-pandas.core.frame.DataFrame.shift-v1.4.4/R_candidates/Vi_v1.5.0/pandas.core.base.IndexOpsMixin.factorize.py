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
    def factorize(
        self,
        sort: bool = False,
        na_sentinel: int | lib.NoDefault = lib.no_default,
        use_na_sentinel: bool | lib.NoDefault = lib.no_default,
    ):
        return algorithms.factorize(
            self, sort=sort, na_sentinel=na_sentinel, use_na_sentinel=use_na_sentinel
        )
