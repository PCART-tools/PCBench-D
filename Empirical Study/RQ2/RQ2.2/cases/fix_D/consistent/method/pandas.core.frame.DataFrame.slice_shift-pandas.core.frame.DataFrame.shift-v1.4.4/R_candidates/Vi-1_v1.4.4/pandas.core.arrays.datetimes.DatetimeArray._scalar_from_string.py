    def _scalar_from_string(self, value) -> Timestamp | NaTType:
        return Timestamp(value, tz=self.tz)
