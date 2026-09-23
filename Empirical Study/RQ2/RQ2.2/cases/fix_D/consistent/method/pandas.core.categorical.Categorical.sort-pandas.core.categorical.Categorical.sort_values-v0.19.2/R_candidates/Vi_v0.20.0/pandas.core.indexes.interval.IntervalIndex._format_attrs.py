    def _format_attrs(self):
        attrs = [('closed', repr(self.closed))]
        if self.name is not None:
            attrs.append(('name', default_pprint(self.name)))
        attrs.append(('dtype', "'%s'" % self.dtype))
        return attrs
