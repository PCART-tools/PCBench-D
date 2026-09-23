    def _compare_frame(self, other, func, str_rep):
        if not self._indexed_same(other):
            raise ValueError('Can only compare identically-labeled '
                             'DataFrame objects')
        return self._compare_frame_evaluate(other, func, str_rep)
