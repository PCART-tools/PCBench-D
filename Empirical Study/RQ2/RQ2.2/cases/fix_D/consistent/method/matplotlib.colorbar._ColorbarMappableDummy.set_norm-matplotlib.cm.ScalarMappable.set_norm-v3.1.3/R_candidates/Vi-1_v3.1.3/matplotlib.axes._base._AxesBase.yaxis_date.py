    def yaxis_date(self, tz=None):
        """
        Sets up y-axis ticks and labels that treat the y data as dates.

        Parameters
        ----------
        tz : string or `tzinfo` instance, optional
            Timezone.  Defaults to :rc:`timezone`.
        """
        self.yaxis.axis_date(tz)
