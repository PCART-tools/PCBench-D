    def get_locator(self, dmin, dmax):
        'Pick the best locator based on a distance.'
        delta = relativedelta(dmax, dmin)
        tdelta = dmax - dmin

        # take absolute difference
        if dmin > dmax:
            delta = -delta
            tdelta = -tdelta

        # The following uses a mix of calls to relativedelta and timedelta
        # methods because there is incomplete overlap in the functionality of
        # these similar functions, and it's best to avoid doing our own math
        # whenever possible.
        numYears = float(delta.years)
        numMonths = numYears * MONTHS_PER_YEAR + delta.months
        numDays = tdelta.days   # Avoids estimates of days/month, days/year
        numHours = numDays * HOURS_PER_DAY + delta.hours
        numMinutes = numHours * MIN_PER_HOUR + delta.minutes
        numSeconds = np.floor(tdelta.total_seconds())
        numMicroseconds = np.floor(tdelta.total_seconds() * 1e6)

        nums = [numYears, numMonths, numDays, numHours, numMinutes,
                numSeconds, numMicroseconds]

        use_rrule_locator = [True] * 6 + [False]

        # Default setting of bymonth, etc. to pass to rrule
        # [unused (for year), bymonth, bymonthday, byhour, byminute,
        #  bysecond, unused (for microseconds)]
        byranges = [None, 1, 1, 0, 0, 0, None]

        # Loop over all the frequencies and try to find one that gives at
        # least a minticks tick positions.  Once this is found, look for
        # an interval from an list specific to that frequency that gives no
        # more than maxticks tick positions. Also, set up some ranges
        # (bymonth, etc.) as appropriate to be passed to rrulewrapper.
        for i, (freq, num) in enumerate(zip(self._freqs, nums)):
            # If this particular frequency doesn't give enough ticks, continue
            if num < self.minticks:
                # Since we're not using this particular frequency, set
                # the corresponding by_ to None so the rrule can act as
                # appropriate
                byranges[i] = None
                continue

            # Find the first available interval that doesn't give too many
            # ticks
            for interval in self.intervald[freq]:
                if num <= interval * (self.maxticks[freq] - 1):
                    break
            else:
                # We went through the whole loop without breaking, default to
                # the last interval in the list and raise a warning
                cbook._warn_external(
                    f"AutoDateLocator was unable to pick an appropriate "
                    f"interval for this date range. It may be necessary to "
                    f"add an interval value to the AutoDateLocator's "
                    f"intervald dictionary. Defaulting to {interval}.")

            # Set some parameters as appropriate
            self._freq = freq

            if self._byranges[i] and self.interval_multiples:
                byranges[i] = self._byranges[i][::interval]
                if i in (DAILY, WEEKLY):
                    if interval == 14:
                        # just make first and 15th.  Avoids 30th.
                        byranges[i] = [1, 15]
                    elif interval == 7:
                        byranges[i] = [1, 8, 15, 22]

                interval = 1
            else:
                byranges[i] = self._byranges[i]
            break
        else:
            raise ValueError('No sensible date limit could be found in the '
                             'AutoDateLocator.')

        if (freq == YEARLY) and self.interval_multiples:
            locator = YearLocator(interval, tz=self.tz)
        elif use_rrule_locator[i]:
            _, bymonth, bymonthday, byhour, byminute, bysecond, _ = byranges
            rrule = rrulewrapper(self._freq, interval=interval,
                                 dtstart=dmin, until=dmax,
                                 bymonth=bymonth, bymonthday=bymonthday,
                                 byhour=byhour, byminute=byminute,
                                 bysecond=bysecond)

            locator = RRuleLocator(rrule, self.tz)
        else:
            locator = MicrosecondLocator(interval, tz=self.tz)
            if dmin.year > 20 and interval < 1000:
                cbook._warn_external(
                    'Plotting microsecond time intervals is not well '
                    'supported; please see the MicrosecondLocator '
                    'documentation for details.')

        locator.set_axis(self.axis)

        if self.axis is not None:
            locator.set_view_interval(*self.axis.get_view_interval())
            locator.set_data_interval(*self.axis.get_data_interval())
        return locator
