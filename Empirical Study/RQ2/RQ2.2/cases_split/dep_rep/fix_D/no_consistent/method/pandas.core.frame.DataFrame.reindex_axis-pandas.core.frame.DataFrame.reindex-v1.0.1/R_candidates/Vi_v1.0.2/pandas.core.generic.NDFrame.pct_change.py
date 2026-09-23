    @Appender(_shared_docs["pct_change"] % _shared_doc_kwargs)
    def pct_change(
        self: FrameOrSeries,
        periods=1,
        fill_method="pad",
        limit=None,
        freq=None,
        **kwargs,
    ) -> FrameOrSeries:
        # TODO: Not sure if above is correct - need someone to confirm.
        axis = self._get_axis_number(kwargs.pop("axis", self._stat_axis_name))
        if fill_method is None:
            data = self
        else:
            _data = self.fillna(method=fill_method, axis=axis, limit=limit)
            assert _data is not None  # needed for mypy
            data = _data

        rs = data.div(data.shift(periods=periods, freq=freq, axis=axis, **kwargs)) - 1
        if freq is not None:
            # Shift method is implemented differently when freq is not None
            # We want to restore the original index
            rs = rs.loc[~rs.index.duplicated()]
            rs = rs.reindex_like(data)
        return rs
