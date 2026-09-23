    def get_locator(self, d):
        'pick the best locator based on a distance'
        d = abs(d)
        if d <= 0:
            locator = MultipleLocator(0.2)
        else:

            try:
                ld = math.log10(d)
            except OverflowError:
                raise RuntimeError('AutoLocator illegal data interval range')

            fld = math.floor(ld)
            base = 10 ** fld

            #if ld==fld:  base = 10**(fld-1)
            #else:        base = 10**fld

            if d >= 5 * base:
                ticksize = base
            elif d >= 2 * base:
                ticksize = base / 2.0
            else:
                ticksize = base / 5.0
            locator = MultipleLocator(ticksize)

        return locator
