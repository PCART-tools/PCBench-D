    @property
    def is_leap_year(self):
        """
        Logical indicating if the date belongs to a leap year
        """
        return isleapyear_arr(np.asarray(self.year))
