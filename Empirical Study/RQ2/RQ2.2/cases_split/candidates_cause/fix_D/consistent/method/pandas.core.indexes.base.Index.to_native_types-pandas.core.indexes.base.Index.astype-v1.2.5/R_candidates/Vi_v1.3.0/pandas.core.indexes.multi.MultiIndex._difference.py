    def _difference(self, other, sort) -> MultiIndex:
        other, result_names = self._convert_can_do_setop(other)

        difference = super()._difference(other, sort)

        if len(difference) == 0:
            return MultiIndex(
                levels=[[]] * self.nlevels,
                codes=[[]] * self.nlevels,
                names=result_names,
                verify_integrity=False,
            )
        else:
            return MultiIndex.from_tuples(difference, sortorder=0, names=result_names)
