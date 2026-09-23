    def format_data_short(self, value):
        # docstring inherited
        if isinstance(value, np.ma.MaskedArray) and value.mask:
            return ""
        if isinstance(value, Integral):
            fmt = "%d"
        else:
            if getattr(self.axis, "__name__", "") in ["xaxis", "yaxis"]:
                if self.axis.__name__ == "xaxis":
                    axis_trf = self.axis.axes.get_xaxis_transform()
                    axis_inv_trf = axis_trf.inverted()
                    screen_xy = axis_trf.transform((value, 0))
                    neighbor_values = axis_inv_trf.transform(
                        screen_xy + [[-1, 0], [+1, 0]])[:, 0]
                else:  # yaxis:
                    axis_trf = self.axis.axes.get_yaxis_transform()
                    axis_inv_trf = axis_trf.inverted()
                    screen_xy = axis_trf.transform((0, value))
                    neighbor_values = axis_inv_trf.transform(
                        screen_xy + [[0, -1], [0, +1]])[:, 1]
                delta = abs(neighbor_values - value).max()
            else:
                # Rough approximation: no more than 1e4 divisions.
                delta = np.diff(self.axis.get_view_interval()) / 1e4
            # If e.g. value = 45.67 and delta = 0.02, then we want to round to
            # 2 digits after the decimal point (floor(log10(0.02)) = -2);
            # 45.67 contributes 2 digits before the decimal point
            # (floor(log10(45.67)) + 1 = 2): the total is 4 significant digits.
            # A value of 0 contributes 1 "digit" before the decimal point.
            sig_digits = max(
                0,
                (math.floor(math.log10(abs(value))) + 1 if value else 1)
                - math.floor(math.log10(delta)))
            fmt = f"%-#.{sig_digits}g"
        return (
            self.fix_minus(
                locale.format_string(fmt, (value,)) if self._useLocale else
                fmt % value))
