    def datalim_to_dt(self):
        """
        Convert axis data interval to datetime objects.
        """
        dmin, dmax = self.axis.get_data_interval()
        if dmin > dmax:
            dmin, dmax = dmax, dmin
        if dmin < 1:
            raise ValueError('datalim minimum {} is less than 1 and '
                             'is an invalid Matplotlib date value. This often '
                             'happens if you pass a non-datetime '
                             'value to an axis that has datetime units'
                             .format(dmin))
        return num2date(dmin, self.tz), num2date(dmax, self.tz)
