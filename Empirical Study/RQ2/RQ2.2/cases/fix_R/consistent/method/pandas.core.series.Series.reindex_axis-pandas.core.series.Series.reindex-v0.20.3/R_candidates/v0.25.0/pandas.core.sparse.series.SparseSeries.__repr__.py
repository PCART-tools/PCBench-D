    def __repr__(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", "Sparse")
            series_rep = Series.__repr__(self)
            rep = "{series}\n{index!r}".format(series=series_rep, index=self.sp_index)
            return rep
