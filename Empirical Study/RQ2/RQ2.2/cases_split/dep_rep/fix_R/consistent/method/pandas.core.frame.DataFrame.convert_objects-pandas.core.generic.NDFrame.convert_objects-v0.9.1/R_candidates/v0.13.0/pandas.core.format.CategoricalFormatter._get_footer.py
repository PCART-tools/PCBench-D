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

        levheader = 'Levels (%d): ' % len(self.categorical.levels)

        # TODO: should max_line_width respect a setting?
        levstring = np.array_repr(self.categorical.levels, max_line_width=60)
        indent = ' ' * (levstring.find('[') + len(levheader) + 1)
        lines = levstring.split('\n')
        levstring = '\n'.join([lines[0]] +
                              [indent + x.lstrip() for x in lines[1:]])
        if footer:
            footer += ', '
        footer += levheader + levstring

        return compat.text_type(footer)
