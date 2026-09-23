    def _flex_compare_frame(self, other, func, str_rep, level):
        if not self._indexed_same(other):
            self, other = self.align(other, 'outer', level=level, copy=False)
        return self._compare_frame_evaluate(other, func, str_rep)
