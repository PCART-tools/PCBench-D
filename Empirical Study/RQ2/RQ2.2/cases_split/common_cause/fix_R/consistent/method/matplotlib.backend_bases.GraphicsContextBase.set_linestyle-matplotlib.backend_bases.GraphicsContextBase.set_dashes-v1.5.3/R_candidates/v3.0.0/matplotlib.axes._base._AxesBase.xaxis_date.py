    def xaxis_date(self, tz=None):
        """
        Sets up x-axis ticks and labels that treat the x data as dates.

        Parameters
        ----------
        tz : string or :class:`tzinfo` instance, optional
            Timezone string or timezone. Defaults to rc value.
        """
        # should be enough to inform the unit conversion interface
        # dates are coming in
        self.xaxis.axis_date(tz)
