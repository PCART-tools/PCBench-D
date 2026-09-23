    def _format_attrs(self):
        """
        Return a list of tuples of the (attr, formatted_value)
        """
        attrs = self._get_data_as_items()
        if self.name is not None:
            attrs.append(("name", ibase.default_pprint(self.name)))
        return attrs
