    @Substitution(
        values='', order='', size_hint='',
        sort=textwrap.dedent("""\
            sort : boolean, default False
                Sort `uniques` and shuffle `labels` to maintain the
                relationship.
            """))
    @Appender(algorithms._shared_docs['factorize'])
    def factorize(self, sort=False, na_sentinel=-1):
        return algorithms.factorize(self, sort=sort, na_sentinel=na_sentinel)
