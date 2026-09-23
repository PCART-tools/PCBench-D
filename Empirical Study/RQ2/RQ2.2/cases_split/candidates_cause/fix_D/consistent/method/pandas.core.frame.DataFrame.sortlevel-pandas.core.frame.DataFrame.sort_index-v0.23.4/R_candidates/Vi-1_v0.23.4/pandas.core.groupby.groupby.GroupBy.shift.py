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

        return self._get_cythonized_result('group_shift_indexer',
                                           self.grouper, cython_dtype=np.int64,
                                           needs_ngroups=True,
                                           result_is_index=True,
                                           periods=periods)
