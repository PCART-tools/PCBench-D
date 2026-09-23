    def _get_new_axes(self) -> list[Index]:
        ndim = self._get_result_dim()
        return [
            self._get_concat_axis if i == self.bm_axis else self._get_comb_axis(i)
            for i in range(ndim)
        ]
