    def _format_attrs(self):
        """
        Return a list of tuples of the (attr,formatted_value)
        """
        attrs = []
        attrs.append(('dtype', "'%s'" % self.dtype))
        if self.name is not None:
            attrs.append(('name', default_pprint(self.name)))
        max_seq_items = get_option('display.max_seq_items') or len(self)
        if len(self) > max_seq_items:
            attrs.append(('length', len(self)))
        return attrs
