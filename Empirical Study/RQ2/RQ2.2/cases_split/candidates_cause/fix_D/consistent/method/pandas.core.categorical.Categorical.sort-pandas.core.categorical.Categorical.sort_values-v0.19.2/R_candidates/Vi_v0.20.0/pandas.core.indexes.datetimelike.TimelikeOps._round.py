    def _round(self, freq, rounder):

        from pandas.tseries.frequencies import to_offset
        unit = to_offset(freq).nanos
        # round the local times
        values = _ensure_datetimelike_to_i8(self)
        if unit < 1000 and unit % 1000 != 0:
            # for nano rounding, work with the last 6 digits separately
            # due to float precision
            buff = 1000000
            result = (buff * (values // buff) + unit *
                      (rounder((values % buff) / float(unit))).astype('i8'))
        elif unit >= 1000 and unit % 1000 != 0:
            msg = 'Precision will be lost using frequency: {}'
            warnings.warn(msg.format(freq))
            result = (unit * rounder(values / float(unit)).astype('i8'))
        else:
            result = (unit * rounder(values / float(unit)).astype('i8'))
        result = self._maybe_mask_results(result, fill_value=NaT)

        attribs = self._get_attributes_dict()
        if 'freq' in attribs:
            attribs['freq'] = None
        if 'tz' in attribs:
            attribs['tz'] = None
        return self._ensure_localized(
            self._shallow_copy(result, **attribs))
