    def format_data_short(self, value):
        return num2date(value, tz=self._tz).strftime('%Y-%m-%d %H:%M:%S')
