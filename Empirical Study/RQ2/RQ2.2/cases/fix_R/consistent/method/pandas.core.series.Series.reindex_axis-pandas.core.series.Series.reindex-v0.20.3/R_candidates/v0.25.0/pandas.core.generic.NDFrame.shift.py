    @Appender(_shared_docs["shift"] % _shared_doc_kwargs)
    def shift(self, periods=1, freq=None, axis=0, fill_value=None):
        if periods == 0:
            return self.copy()

        block_axis = self._get_block_manager_axis(axis)
        if freq is None:
            new_data = self._data.shift(
                periods=periods, axis=block_axis, fill_value=fill_value
            )
        else:
            return self.tshift(periods, freq)

        return self._constructor(new_data).__finalize__(self)
