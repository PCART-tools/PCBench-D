    def viewlim_to_dt(self):
        """
        Converts the view interval to datetime objects.
        """
        vmin, vmax = self.axis.get_view_interval()
        if vmin > vmax:
            vmin, vmax = vmax, vmin
        if vmin < 1:
            raise ValueError('view limit minimum {} is less than 1 and '
                             'is an invalid Matplotlib date value. This '
                             'often happens if you pass a non-datetime '
                             'value to an axis that has datetime units'
                             .format(vmin))
        return num2date(vmin, self.tz), num2date(vmax, self.tz)
