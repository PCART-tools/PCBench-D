    def _repr_footer(self):

        namestr = u("Name: %s, ") % com.pprint_thing(
            self.name) if self.name is not None else ""

        # time series
        if self.is_time_series:
            if self.index.freq is not None:
                freqstr = u('Freq: %s, ') % self.index.freqstr
            else:
                freqstr = u('')

            return u('%s%sLength: %d') % (freqstr, namestr, len(self))

        # Categorical
        if com.is_categorical_dtype(self.dtype):
            level_info = self.values._repr_categories_info()
            return u('%sLength: %d, dtype: %s\n%s') % (namestr,
                                                       len(self),
                                                       str(self.dtype.name),
                                                       level_info)

        # reg series
        return u('%sLength: %d, dtype: %s') % (namestr,
                                               len(self),
                                               str(self.dtype.name))
