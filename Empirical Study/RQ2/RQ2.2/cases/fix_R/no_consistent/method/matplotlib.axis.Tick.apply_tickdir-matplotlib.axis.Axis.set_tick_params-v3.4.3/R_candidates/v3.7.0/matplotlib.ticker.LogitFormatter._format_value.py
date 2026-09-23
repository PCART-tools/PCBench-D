    def _format_value(self, x, locs, sci_notation=True):
        if sci_notation:
            exponent = math.floor(np.log10(x))
            min_precision = 0
        else:
            exponent = 0
            min_precision = 1
        value = x * 10 ** (-exponent)
        if len(locs) < 2:
            precision = min_precision
        else:
            diff = np.sort(np.abs(locs - x))[1]
            precision = -np.log10(diff) + exponent
            precision = (
                int(np.round(precision))
                if _is_close_to_int(precision)
                else math.ceil(precision)
            )
            if precision < min_precision:
                precision = min_precision
        mantissa = r"%.*f" % (precision, value)
        if not sci_notation:
            return mantissa
        s = r"%s\cdot10^{%d}" % (mantissa, exponent)
        return s
