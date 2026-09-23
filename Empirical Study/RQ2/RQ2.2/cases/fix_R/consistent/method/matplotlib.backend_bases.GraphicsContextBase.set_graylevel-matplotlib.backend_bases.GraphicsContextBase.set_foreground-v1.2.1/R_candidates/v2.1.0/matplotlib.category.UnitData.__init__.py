    def __init__(self, data):
        """Create mapping between unique categorical values
        and numerical identifier

        Parameters
        ----------
        data: iterable
            sequence of values
        """
        self.seq, self.locs = [], []
        self._set_seq_locs(data, 0)
