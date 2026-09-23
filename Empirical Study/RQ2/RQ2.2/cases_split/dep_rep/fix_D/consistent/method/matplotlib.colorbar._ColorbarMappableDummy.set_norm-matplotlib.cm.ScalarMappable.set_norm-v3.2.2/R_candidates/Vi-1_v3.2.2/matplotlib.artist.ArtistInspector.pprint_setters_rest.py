    def pprint_setters_rest(self, prop=None, leadingspace=4):
        """
        If *prop* is *None*, return a list of strings of all settable
        properties and their valid values.  Format the output for ReST

        If *prop* is not *None*, it is a valid property name and that
        property will be returned as a string of property : valid
        values.
        """
        if leadingspace:
            pad = ' ' * leadingspace
        else:
            pad = ''
        if prop is not None:
            accepts = self.get_valid_values(prop)
            return '%s%s: %s' % (pad, prop, accepts)

        attrs = sorted(self._get_setters_and_targets())

        names = [self.aliased_name_rest(prop, target).replace(
            '_base._AxesBase', 'Axes').replace(
            '_axes.Axes', 'Axes')
                 for prop, target in attrs]
        accepts = [self.get_valid_values(prop) for prop, target in attrs]

        col0_len = max(len(n) for n in names)
        col1_len = max(len(a) for a in accepts)
        table_formatstr = pad + '   ' + '=' * col0_len + '   ' + '=' * col1_len

        return [
            '',
            pad + '.. table::',
            pad + '   :class: property-table',
            '',
            table_formatstr,
            pad + '   ' + 'Property'.ljust(col0_len)
            + '   ' + 'Description'.ljust(col1_len),
            table_formatstr,
            *[pad + '   ' + n.ljust(col0_len) + '   ' + a.ljust(col1_len)
              for n, a in zip(names, accepts)],
            table_formatstr,
            '',
        ]
