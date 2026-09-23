    def _scalar_from_string(self, value):
        return Timestamp(value, tz=self.tz)
