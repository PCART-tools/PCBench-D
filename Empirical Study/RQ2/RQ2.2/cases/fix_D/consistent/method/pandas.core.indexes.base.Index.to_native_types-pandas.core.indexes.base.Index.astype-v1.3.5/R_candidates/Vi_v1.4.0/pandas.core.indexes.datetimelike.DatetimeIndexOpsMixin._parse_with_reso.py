    def _parse_with_reso(self, label: str):
        # overridden by TimedeltaIndex
        parsed, reso_str = parsing.parse_time_string(label, self.freq)
        reso = Resolution.from_attrname(reso_str)
        return parsed, reso
