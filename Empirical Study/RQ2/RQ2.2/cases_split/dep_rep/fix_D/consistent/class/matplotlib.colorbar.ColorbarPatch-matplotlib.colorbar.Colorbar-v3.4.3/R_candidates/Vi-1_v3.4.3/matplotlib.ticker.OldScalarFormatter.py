@_api.deprecated("3.3")
class OldScalarFormatter(Formatter):
    """
    Tick location is a plain old number.
    """

    def __call__(self, x, pos=None):
        """
        Return the format for tick val *x* based on the width of the axis.

        The position *pos* is ignored.
        """
        xmin, xmax = self.axis.get_view_interval()
        # If the number is not too big and it's an int, format it as an int.
        if abs(x) < 1e4 and x == int(x):
            return '%d' % x
        d = abs(xmax - xmin)
        fmt = ('%1.3e' if d < 1e-2 else
               '%1.3f' if d <= 1 else
               '%1.2f' if d <= 10 else
               '%1.1f' if d <= 1e5 else
               '%1.1e')
        s = fmt % x
        tup = s.split('e')
        if len(tup) == 2:
            mantissa = tup[0].rstrip('0').rstrip('.')
            sign = tup[1][0].replace('+', '')
            exponent = tup[1][1:].lstrip('0')
            s = '%se%s%s' % (mantissa, sign, exponent)
        else:
            s = s.rstrip('0').rstrip('.')
        return s
