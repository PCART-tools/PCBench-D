    def _get_footer(self):
        name = self.series.name
        footer = u('')

        if getattr(self.series.index, 'freq', None) is not None:
            footer += 'Freq: %s' % self.series.index.freqstr

        if self.name is not False and name is not None:
            if footer:
                footer += ', '

            series_name = com.pprint_thing(name,
                                           escape_chars=('\t', '\r', '\n'))
            footer += ("Name: %s" %
                       series_name) if name is not None else ""

        if self.length:
            if footer:
                footer += ', '
            footer += 'Length: %d' % len(self.series)

        if self.dtype is not False and self.dtype is not None:
            name = getattr(self.tr_series.dtype, 'name', None)
            if name:
                if footer:
                    footer += ', '
                footer += 'dtype: %s' % com.pprint_thing(name)

        # level infos are added to the end and in a new line, like it is done for Categoricals
        # Only added when we request a name
        if name and com.is_categorical_dtype(self.tr_series.dtype):
            level_info = self.tr_series.values._repr_categories_info()
            if footer:
                footer += "\n"
            footer += level_info

        return compat.text_type(footer)
