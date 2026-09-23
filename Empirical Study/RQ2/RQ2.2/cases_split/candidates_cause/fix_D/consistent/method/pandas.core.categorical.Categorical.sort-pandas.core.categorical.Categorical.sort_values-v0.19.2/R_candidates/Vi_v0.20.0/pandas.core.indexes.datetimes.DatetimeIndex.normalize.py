    def normalize(self):
        """
        Return DatetimeIndex with times to midnight. Length is unaltered

        Returns
        -------
        normalized : DatetimeIndex
        """
        new_values = libts.date_normalize(self.asi8, self.tz)
        return DatetimeIndex(new_values, freq='infer', name=self.name,
                             tz=self.tz)
