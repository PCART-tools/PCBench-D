    def symmetric_difference(self, other, result_name=None, sort=None):
        # On equal symmetric_difference MultiIndexes the difference is empty.
        # Therefore, an empty MultiIndex is returned GH13490
        tups = Index.symmetric_difference(self, other, result_name, sort)
        if len(tups) == 0:
            return type(self)(
                levels=[[] for _ in range(self.nlevels)],
                codes=[[] for _ in range(self.nlevels)],
                names=tups.name,
            )
        return type(self).from_tuples(tups, names=tups.name)
