    def _wrap_intersection_result(self, other, result):
        other, result_names = self._convert_can_do_setop(other)

        if len(result) == 0:
            return MultiIndex(
                levels=self.levels,
                codes=[[]] * self.nlevels,
                names=result_names,
                verify_integrity=False,
            )
        else:
            return MultiIndex.from_arrays(zip(*result), sortorder=0, names=result_names)
