    @Appender(
        _interval_shared_docs["to_tuples"] % dict(return_type="ndarray", examples="")
    )
    def to_tuples(self, na_tuple=True):
        tuples = com.asarray_tuplesafe(zip(self.left, self.right))
        if not na_tuple:
            # GH 18756
            tuples = np.where(~self.isna(), tuples, np.nan)
        return tuples
