    @staticmethod
    def _calc_offsets(l, k):
        offsets = [0.]
        for _rs, _as in l:
            offsets.append(offsets[-1] + _rs*k + _as)
        return offsets
