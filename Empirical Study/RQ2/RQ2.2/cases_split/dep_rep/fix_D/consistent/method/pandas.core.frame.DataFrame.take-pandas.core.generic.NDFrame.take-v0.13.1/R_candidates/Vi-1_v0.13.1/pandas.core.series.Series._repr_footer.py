    def _repr_footer(self):

        # time series
        if self.is_time_series:
            if self.index.freq is not None:
                freqstr = u('Freq: %s, ') % self.index.freqstr
            else:
                freqstr = u('')

            namestr = u("Name: %s, ") % com.pprint_thing(
                self.name) if self.name is not None else ""
            return u('%s%sLength: %d') % (freqstr, namestr, len(self))

        # reg series
        namestr = u("Name: %s, ") % com.pprint_thing(
            self.name) if self.name is not None else ""
        return u('%sLength: %d, dtype: %s') % (namestr,
                                               len(self),
                                               str(self.dtype.name))
