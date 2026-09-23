    @Substitution(name='groupby')
    @Appender(_doc_template)
    def shift(self, periods=1, freq=None, axis=0):
        """
        Shift each group by periods observations

        Parameters
        ----------
        periods : integer, default 1
            number of periods to shift
        freq : frequency string
        axis : axis to shift, default 0
        """

        if freq is not None or axis != 0:
            return self.apply(lambda x: x.shift(periods, freq, axis))

        labels, _, ngroups = self.grouper.group_info

        # filled in by Cython
        indexer = np.zeros_like(labels)
        _algos.group_shift_indexer(indexer, labels, ngroups, periods)

        output = {}
        for name, obj in self._iterate_slices():
            output[name] = algos.take_nd(obj.values, indexer)

        return self._wrap_transformed_output(output)
