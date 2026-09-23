    def _wrap_intersection_result(self, other, result) -> MultiIndex:
        _, result_names = self._convert_can_do_setop(other)
        return result.set_names(result_names)
