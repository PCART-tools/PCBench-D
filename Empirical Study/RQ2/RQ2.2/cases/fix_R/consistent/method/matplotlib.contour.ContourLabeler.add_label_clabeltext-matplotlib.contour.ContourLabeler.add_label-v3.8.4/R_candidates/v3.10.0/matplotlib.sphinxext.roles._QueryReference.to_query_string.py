    def to_query_string(self):
        """Generate query string from node attributes."""
        return '&'.join(f'{name}={value}' for name, value in self.attlist())
