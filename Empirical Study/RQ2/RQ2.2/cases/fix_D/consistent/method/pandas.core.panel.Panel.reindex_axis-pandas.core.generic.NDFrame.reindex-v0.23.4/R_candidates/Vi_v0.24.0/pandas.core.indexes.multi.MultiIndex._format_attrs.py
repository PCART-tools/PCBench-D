    def _format_attrs(self):
        """
        Return a list of tuples of the (attr,formatted_value)
        """
        attrs = [
            ('levels', ibase.default_pprint(self._levels,
                                            max_seq_items=False)),
            ('codes', ibase.default_pprint(self._codes,
                                           max_seq_items=False))]
        if com._any_not_none(*self.names):
            attrs.append(('names', ibase.default_pprint(self.names)))
        if self.sortorder is not None:
            attrs.append(('sortorder', ibase.default_pprint(self.sortorder)))
        return attrs
