    def pprint_val(self, x, d):
        #if the number is not too big and it's an int, format it as an
        #int
        if abs(x) < 1e4 and x == int(x):
            return '%d' % x

        if d < 1e-2:
            fmt = '%1.3e'
        elif d < 1e-1:
            fmt = '%1.3f'
        elif d > 1e5:
            fmt = '%1.1e'
        elif d > 10:
            fmt = '%1.1f'
        elif d > 1:
            fmt = '%1.2f'
        else:
            fmt = '%1.3f'
        s = fmt % x

        tup = s.split('e')
        if len(tup) == 2:
            mantissa = tup[0].rstrip('0').rstrip('.')
            exponent = int(tup[1])
            if exponent:
                s = '%se%d' % (mantissa, exponent)
            else:
                s = mantissa
        else:
            s = s.rstrip('0').rstrip('.')
        return s
