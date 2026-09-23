    def _convert_obj(self, obj):
        obj = super(PeriodIndexResampler, self)._convert_obj(obj)

        offset = to_offset(self.freq)
        if offset.n > 1:
            if self.kind == 'period':  # pragma: no cover
                print('Warning: multiple of frequency -> timestamps')

            # Cannot have multiple of periods, convert to timestamp
            self.kind = 'timestamp'

        # convert to timestamp
        if not (self.kind is None or self.kind == 'period'):
            if self._from_selection:
                # see GH 14008, GH 12871
                msg = ("Resampling from level= or on= selection"
                       " with a PeriodIndex is not currently supported,"
                       " use .set_index(...) to explicitly set index")
                raise NotImplementedError(msg)
            else:
                obj = obj.to_timestamp(how=self.convention)

        return obj
