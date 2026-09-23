    def _non_decade_format(self, sign_string, base, fx, usetex):
        'Return string for non-decade locations'
        if usetex:
            return (r'$%s%s^{%.2f}$') % (sign_string, base, fx)
        else:
            return ('$%s$' % _mathdefault('%s%s^{%.2f}' %
                                          (sign_string, base, fx)))
