    def _non_decade_format(self, sign_string, base, fx, usetex):
        'Return string for non-decade locations'
        return r'$\mathdefault{%s%s^{%.2f}}$' % (sign_string, base, fx)
