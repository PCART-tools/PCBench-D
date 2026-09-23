    @cbook.deprecated("3.0")
    def strftime_pre_1900(self, dt, fmt=None):
        """Call time.strftime for years before 1900 by rolling
        forward a multiple of 28 years.

        *fmt* is a :func:`strftime` format string.

        Dalke: I hope I did this math right.  Every 28 years the
        calendar repeats, except through century leap years excepting
        the 400 year leap years.  But only if you're using the Gregorian
        calendar.
        """
        if fmt is None:
            fmt = self.fmt

        # Since python's time module's strftime implementation does not
        # support %f microsecond (but the datetime module does), use a
        # regular expression substitution to replace instances of %f.
        # Note that this can be useful since python's floating-point
        # precision representation for datetime causes precision to be
        # more accurate closer to year 0 (around the year 2000, precision
        # can be at 10s of microseconds).
        fmt = re.sub(r'((^|[^%])(%%)*)%f',
                     r'\g<1>{0:06d}'.format(dt.microsecond), fmt)

        year = dt.year
        # For every non-leap year century, advance by
        # 6 years to get into the 28-year repeat cycle
        delta = 2000 - year
        off = 6 * (delta // 100 + delta // 400)
        year = year + off

        # Move to between the years 1973 and 2000
        year1 = year + ((2000 - year) // 28) * 28
        year2 = year1 + 28
        timetuple = dt.timetuple()
        # Generate timestamp string for year and year+28
        s1 = time.strftime(fmt, (year1,) + timetuple[1:])
        s2 = time.strftime(fmt, (year2,) + timetuple[1:])

        # Replace instances of respective years (both 2-digit and 4-digit)
        # that are located at the same indexes of s1, s2 with dt's year.
        # Note that C++'s strftime implementation does not use padded
        # zeros or padded whitespace for %y or %Y for years before 100, but
        # uses padded zeros for %x. (For example, try the runnable examples
        # with .tm_year in the interval [-1900, -1800] on
        # http://en.cppreference.com/w/c/chrono/strftime.) For ease of
        # implementation, we always use padded zeros for %y, %Y, and %x.
        s1, s2 = self._replace_common_substr(s1, s2,
                                             "{0:04d}".format(year1),
                                             "{0:04d}".format(year2),
                                             "{0:04d}".format(dt.year))
        s1, s2 = self._replace_common_substr(s1, s2,
                                             "{0:02d}".format(year1 % 100),
                                             "{0:02d}".format(year2 % 100),
                                             "{0:02d}".format(dt.year % 100))
        return cbook.unicode_safe(s1)
