    def _get_footer(self):
        footer = u('')

        if self.name:
            if getattr(self.series.index, 'freq', None):
                footer += 'Freq: %s' % self.series.index.freqstr

            if footer and self.series.name is not None:
                # categories have already a comma + linebreak
                if not com.is_categorical_dtype(self.series.dtype):
                    footer += ', '

            series_name = com.pprint_thing(self.series.name,
                                           escape_chars=('\t', '\r', '\n'))
            footer += ("Name: %s" %
                       series_name) if self.series.name is not None else ""

        if self.length:
            if footer:
                footer += ', '
            footer += 'Length: %d' % len(self.series)

        # TODO: in tidy_repr, with freq index, no dtype is shown -> also include a guard here?
        if self.dtype:
            name = getattr(self.series.dtype, 'name', None)
            if name:
                if footer:
                    footer += ', '
                footer += 'dtype: %s' % com.pprint_thing(name)

        # level infos are added to the end and in a new line, like it is done for Categoricals
        # Only added when we request a name
        if self.name and com.is_categorical_dtype(self.series.dtype):
            level_info = self.series.values._repr_categories_info()
            if footer:
                footer += "\n"
            footer += level_info

        return compat.text_type(footer)
