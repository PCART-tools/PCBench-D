    def _get_indexer(
        self,
        target: Index,
        method: str | None = None,
        limit: int | None = None,
        tolerance=None,
    ) -> np.ndarray:
        # returned ndarray is np.intp

        # empty indexer
        if not len(target):
            return ensure_platform_int(np.array([]))

        if not isinstance(target, MultiIndex):
            try:
                target = MultiIndex.from_tuples(target)
            except (TypeError, ValueError):

                # let's instead try with a straight Index
                if method is None:
                    return Index(self._values).get_indexer(
                        target, method=method, limit=limit, tolerance=tolerance
                    )

                # TODO: explicitly raise here?  we only have one test that
                #  gets here, and it is checking that we raise with method="nearest"

        if method == "pad" or method == "backfill":
            # TODO: get_indexer_with_fill docstring says values must be _sorted_
            #  but that doesn't appear to be enforced
            indexer = self._engine.get_indexer_with_fill(
                target=target._values, values=self._values, method=method, limit=limit
            )
        else:
            indexer = self._engine.get_indexer(target._values)

        # Note: we only get here (in extant tests at least) with
        #  target.nlevels == self.nlevels
        return ensure_platform_int(indexer)
