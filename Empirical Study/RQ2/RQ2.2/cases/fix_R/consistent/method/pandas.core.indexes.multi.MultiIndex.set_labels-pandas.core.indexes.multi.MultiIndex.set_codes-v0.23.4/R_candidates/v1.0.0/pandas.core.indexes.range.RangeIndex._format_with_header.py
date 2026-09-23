    def _format_with_header(self, header, na_rep="NaN", **kwargs):
        return header + list(map(pprint_thing, self._range))
