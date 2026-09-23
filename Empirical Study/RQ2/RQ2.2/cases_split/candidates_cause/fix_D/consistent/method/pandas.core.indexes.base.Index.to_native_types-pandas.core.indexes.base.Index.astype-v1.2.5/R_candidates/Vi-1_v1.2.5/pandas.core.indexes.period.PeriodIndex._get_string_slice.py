    def _get_string_slice(self, key: str):
        parsed, reso = parse_time_string(key, self.freq)
        reso = Resolution.from_attrname(reso)
        try:
            return self._partial_date_slice(reso, parsed)
        except KeyError as err:
            raise KeyError(key) from err
