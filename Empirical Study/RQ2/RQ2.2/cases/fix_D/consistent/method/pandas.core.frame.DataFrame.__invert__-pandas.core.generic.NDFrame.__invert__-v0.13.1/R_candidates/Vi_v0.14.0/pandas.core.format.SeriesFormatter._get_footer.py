    def _get_footer(self):
        footer = u('')

        if self.name:
            if getattr(self.series.index, 'freq', None):
                footer += 'Freq: %s' % self.series.index.freqstr

            if footer and self.series.name is not None:
                footer += ', '

            series_name = com.pprint_thing(self.series.name,
                                           escape_chars=('\t', '\r', '\n'))
            footer += ("Name: %s" %
                       series_name) if self.series.name is not None else ""

        if self.length:
            if footer:
                footer += ', '
            footer += 'Length: %d' % len(self.series)

        if self.dtype:
            name = getattr(self.series.dtype, 'name', None)
            if name:
                if footer:
                    footer += ', '
                footer += 'dtype: %s' % com.pprint_thing(name)

        return compat.text_type(footer)
