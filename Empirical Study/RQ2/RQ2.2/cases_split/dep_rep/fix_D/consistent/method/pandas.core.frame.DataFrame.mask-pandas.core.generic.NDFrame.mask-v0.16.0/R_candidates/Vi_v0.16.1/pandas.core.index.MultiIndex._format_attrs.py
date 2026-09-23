    def _format_attrs(self):
        """
        Return a list of tuples of the (attr,formatted_value)
        """
        attrs = [('levels', default_pprint(self._levels, max_seq_items=False)),
                 ('labels', default_pprint(self._labels, max_seq_items=False))]
        if not all(name is None for name in self.names):
            attrs.append(('names', default_pprint(self.names)))
        if self.sortorder is not None:
            attrs.append(('sortorder', default_pprint(self.sortorder)))
        return attrs
