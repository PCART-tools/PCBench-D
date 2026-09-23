    def output(self, attrs=None, header="Set-Cookie:", sep="\015\012"):
        """Return a string suitable for HTTP."""
        result = []
        items = sorted(self.items())
        for key, value in items:
            result.append(value.output(attrs, header))
        return sep.join(result)
