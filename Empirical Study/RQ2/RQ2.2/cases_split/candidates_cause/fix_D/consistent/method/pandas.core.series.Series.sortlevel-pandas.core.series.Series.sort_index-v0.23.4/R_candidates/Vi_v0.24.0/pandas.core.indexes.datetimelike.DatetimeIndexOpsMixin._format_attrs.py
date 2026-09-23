    def _format_attrs(self):
        """
        Return a list of tuples of the (attr,formatted_value).
        """
        attrs = super(DatetimeIndexOpsMixin, self)._format_attrs()
        for attrib in self._attributes:
            if attrib == 'freq':
                freq = self.freqstr
                if freq is not None:
                    freq = "'%s'" % freq
                attrs.append(('freq', freq))
        return attrs
