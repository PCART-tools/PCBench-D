    def _format_with(self, fmt_str):
        def _val(x, threshold):
            if notnull(x):
                if (threshold is None or
                        abs(x) > get_option("display.chop_threshold")):
                    return fmt_str % x
                else:
                    if fmt_str.endswith("e"):  # engineering format
                        return "0"
                    else:
                        return fmt_str % 0
            else:

                return self.na_rep

        threshold = get_option("display.chop_threshold")
        fmt_values = [_val(x, threshold) for x in self.values]
        return _trim_zeros(fmt_values, self.na_rep)
