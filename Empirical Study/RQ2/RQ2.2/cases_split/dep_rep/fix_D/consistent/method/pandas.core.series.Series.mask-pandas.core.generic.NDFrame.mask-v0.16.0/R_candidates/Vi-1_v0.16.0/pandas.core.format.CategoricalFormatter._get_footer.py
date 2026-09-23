    def _get_footer(self):
        footer = ''

        if self.name:
            name = com.pprint_thing(self.categorical.name,
                                    escape_chars=('\t', '\r', '\n'))
            footer += ('Name: %s' % name if self.categorical.name is not None
                       else '')

        if self.length:
            if footer:
                footer += ', '
            footer += "Length: %d" % len(self.categorical)

        level_info = self.categorical._repr_categories_info()

        # Levels are added in a newline
        if footer:
            footer += '\n'
        footer += level_info

        return compat.text_type(footer)
