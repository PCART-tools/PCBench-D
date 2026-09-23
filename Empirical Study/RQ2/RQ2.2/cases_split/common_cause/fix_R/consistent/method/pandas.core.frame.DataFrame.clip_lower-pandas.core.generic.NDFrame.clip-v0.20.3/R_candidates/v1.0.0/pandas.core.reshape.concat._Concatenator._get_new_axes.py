    def _get_new_axes(self) -> List[Index]:
        ndim = self._get_result_dim()
        return [
            self._get_concat_axis() if i == self.axis else self._get_comb_axis(i)
            for i in range(ndim)
        ]
