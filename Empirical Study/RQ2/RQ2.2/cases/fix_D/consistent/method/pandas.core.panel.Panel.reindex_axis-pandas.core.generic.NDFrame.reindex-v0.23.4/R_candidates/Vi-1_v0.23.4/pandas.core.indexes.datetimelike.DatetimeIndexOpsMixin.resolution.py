    @cache_readonly
    def resolution(self):
        """
        Returns day, hour, minute, second, millisecond or microsecond
        """
        return frequencies.Resolution.get_str(self._resolution)
