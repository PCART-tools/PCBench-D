    @Appender(_shared_docs['pct_change'] % _shared_doc_kwargs)
    def pct_change(self, periods=1, fill_method='pad', limit=None, freq=None,
                   **kwds):
        # TODO: Not sure if above is correct - need someone to confirm.
        axis = self._get_axis_number(kwds.pop('axis', self._stat_axis_name))
        if fill_method is None:
            data = self
        else:
            data = self.fillna(method=fill_method, limit=limit)

        rs = (data.div(data.shift(periods=periods, freq=freq,
                                  axis=axis, **kwds)) - 1)
        if freq is None:
            mask = com.isnull(_values_from_object(self))
            np.putmask(rs.values, mask, np.nan)
        return rs
