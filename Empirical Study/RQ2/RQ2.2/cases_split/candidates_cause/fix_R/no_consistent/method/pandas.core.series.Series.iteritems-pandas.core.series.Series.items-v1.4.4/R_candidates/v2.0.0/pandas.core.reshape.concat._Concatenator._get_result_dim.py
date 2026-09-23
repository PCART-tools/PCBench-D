    def _get_result_dim(self) -> int:
        if self._is_series and self.bm_axis == 1:
            return 2
        else:
            return self.objs[0].ndim
