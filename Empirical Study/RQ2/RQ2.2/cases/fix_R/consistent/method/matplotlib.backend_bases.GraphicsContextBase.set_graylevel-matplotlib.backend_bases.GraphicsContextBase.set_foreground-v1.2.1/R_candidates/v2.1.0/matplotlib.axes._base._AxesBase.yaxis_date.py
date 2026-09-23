    def yaxis_date(self, tz=None):
        """
        Sets up y-axis ticks and labels that treat the y data as dates.

        Parameters
        ----------
        tz : string or :class:`tzinfo` instance, optional
            Timezone string or timezone. Defaults to rc value.
        """
        self.yaxis.axis_date(tz)
