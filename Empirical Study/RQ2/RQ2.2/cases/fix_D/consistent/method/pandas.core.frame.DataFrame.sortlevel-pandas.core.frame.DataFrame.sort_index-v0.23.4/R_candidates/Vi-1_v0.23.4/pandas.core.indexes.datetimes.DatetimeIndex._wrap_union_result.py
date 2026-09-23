    def _wrap_union_result(self, other, result):
        name = self.name if self.name == other.name else None
        if not timezones.tz_compare(self.tz, other.tz):
            raise ValueError('Passed item and index have different timezone')
        return self._simple_new(result, name=name, freq=None, tz=self.tz)
