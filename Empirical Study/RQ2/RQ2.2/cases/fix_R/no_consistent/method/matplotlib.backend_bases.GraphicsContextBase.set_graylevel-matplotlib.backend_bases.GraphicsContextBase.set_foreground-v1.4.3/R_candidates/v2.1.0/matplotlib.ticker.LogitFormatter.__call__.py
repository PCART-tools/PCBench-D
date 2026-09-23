    def __call__(self, x, pos=None):
        s = ''
        if 0.01 <= x <= 0.99:
            s = '{:.2f}'.format(x)
        elif x < 0.01:
            if is_decade(x):
                s = '$10^{{{:.0f}}}$'.format(np.log10(x))
            else:
                s = '${:.5f}$'.format(x)
        else:  # x > 0.99
            if is_decade(1-x):
                s = '$1-10^{{{:.0f}}}$'.format(np.log10(1-x))
            else:
                s = '$1-{:.5f}$'.format(1-x)
        return s
