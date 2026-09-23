    def _wrap_difference_result(self, other, result: MultiIndex) -> MultiIndex:
        _, result_names = self._convert_can_do_setop(other)

        if len(result) == 0:
            return result.remove_unused_levels().set_names(result_names)
        else:
            return result.set_names(result_names)
