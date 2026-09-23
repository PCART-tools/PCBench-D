    @staticmethod
    def _calc_k(l, total_size):

        rs_sum, as_sum = 0., 0.

        for _rs, _as in l:
            rs_sum += _rs
            as_sum += _as

        if rs_sum != 0.:
            k = (total_size - as_sum) / rs_sum
            return k
        else:
            return 0.
