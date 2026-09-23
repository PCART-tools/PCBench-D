    def _format_strings(self):
        if self.formatter is not None:
            fmt_values = [self.formatter(x) for x in self.values]
        else:
            fmt_str = '%% .%df' % (self.digits - 1)
            fmt_values = self._format_with(fmt_str)

            if len(fmt_values) > 0:
                maxlen = max(len(x) for x in fmt_values)
            else:
                maxlen = 0

            too_long = maxlen > self.digits + 5

            abs_vals = np.abs(self.values)

            # this is pretty arbitrary for now
            has_large_values = (abs_vals > 1e8).any()
            has_small_values = ((abs_vals < 10 ** (-self.digits)) &
                                (abs_vals > 0)).any()

            if too_long and has_large_values:
                fmt_str = '%% .%de' % (self.digits - 1)
                fmt_values = self._format_with(fmt_str)
            elif has_small_values:
                fmt_str = '%% .%de' % (self.digits - 1)
                fmt_values = self._format_with(fmt_str)

        return fmt_values
