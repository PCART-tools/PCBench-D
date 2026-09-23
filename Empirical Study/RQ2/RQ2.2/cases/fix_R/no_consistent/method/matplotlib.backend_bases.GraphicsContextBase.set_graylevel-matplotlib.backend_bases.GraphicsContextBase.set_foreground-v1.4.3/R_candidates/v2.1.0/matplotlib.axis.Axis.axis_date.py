    def axis_date(self, tz=None):
        """
        Sets up x-axis ticks and labels that treat the x data as dates.
        *tz* is a :class:`tzinfo` instance or a timezone string.
        This timezone is used to create date labels.
        """
        # By providing a sample datetime instance with the desired
        # timezone, the registered converter can be selected,
        # and the "units" attribute, which is the timezone, can
        # be set.
        import datetime
        if isinstance(tz, six.string_types):
            import pytz
            tz = pytz.timezone(tz)
        self.update_units(datetime.datetime(2009, 1, 1, 0, 0, 0, 0, tz))
