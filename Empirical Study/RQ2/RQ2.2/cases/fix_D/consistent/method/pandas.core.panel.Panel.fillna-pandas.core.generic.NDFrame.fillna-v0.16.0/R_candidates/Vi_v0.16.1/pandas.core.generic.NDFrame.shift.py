    @Appender(_shared_docs['shift'] % _shared_doc_kwargs)
    def shift(self, periods=1, freq=None, axis=0, **kwargs):
        if periods == 0:
            return self

        block_axis = self._get_block_manager_axis(axis)
        if freq is None and not len(kwargs):
            new_data = self._data.shift(periods=periods, axis=block_axis)
        else:
            return self.tshift(periods, freq, **kwargs)

        return self._constructor(new_data).__finalize__(self)
