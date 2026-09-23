    def _create_rrule(self, vmin, vmax):
        # set appropriate rrule dtstart and until and return
        # start and end
        delta = relativedelta(vmax, vmin)

        # We need to cap at the endpoints of valid datetime
        try:
            start = vmin - delta
        except (ValueError, OverflowError):
            # cap
            start = datetime.datetime(1, 1, 1, 0, 0, 0,
                                      tzinfo=datetime.timezone.utc)

        try:
            stop = vmax + delta
        except (ValueError, OverflowError):
            # cap
            stop = datetime.datetime(9999, 12, 31, 23, 59, 59,
                                     tzinfo=datetime.timezone.utc)

        self.rule.set(dtstart=start, until=stop)

        return vmin, vmax
