    def get_fullname(self):
        """Return the font full name, e.g., 'Times-Roman'."""
        name = self._header.get(b'FullName')
        if name is None:  # use FontName as a substitute
            name = self._header[b'FontName']
        return name
