    def format(self, name=False, formatter=None, **kwargs):
        """
        Render a string representation of the Index
        """
        header = []
        if name:
            header.append(com.pprint_thing(self.name,
                                           escape_chars=('\t', '\r', '\n'))
                          if self.name is not None else '')

        if formatter is not None:
            return header + list(self.map(formatter))

        return self._format_with_header(header, **kwargs)
