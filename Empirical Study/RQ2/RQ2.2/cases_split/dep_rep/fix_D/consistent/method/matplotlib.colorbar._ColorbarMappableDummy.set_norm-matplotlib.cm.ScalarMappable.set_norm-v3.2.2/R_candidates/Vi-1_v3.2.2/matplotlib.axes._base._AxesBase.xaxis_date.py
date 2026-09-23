    def xaxis_date(self, tz=None):
        """
        Sets up x-axis ticks and labels that treat the x data as dates.

        Parameters
        ----------
        tz : str or `tzinfo` instance, optional
            Timezone.  Defaults to :rc:`timezone`.
        """
        # should be enough to inform the unit conversion interface
        # dates are coming in
        self.xaxis.axis_date(tz)
