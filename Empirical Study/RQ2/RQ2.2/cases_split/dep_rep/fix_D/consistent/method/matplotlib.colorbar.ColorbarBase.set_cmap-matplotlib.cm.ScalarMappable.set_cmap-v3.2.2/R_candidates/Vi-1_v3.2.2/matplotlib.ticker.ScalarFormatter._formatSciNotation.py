    def _formatSciNotation(self, s):
        # transform 1e+004 into 1e4, for example
        if self._useLocale:
            decimal_point = locale.localeconv()['decimal_point']
            positive_sign = locale.localeconv()['positive_sign']
        else:
            decimal_point = '.'
            positive_sign = '+'
        tup = s.split('e')
        try:
            significand = tup[0].rstrip('0').rstrip(decimal_point)
            sign = tup[1][0].replace(positive_sign, '')
            exponent = tup[1][1:].lstrip('0')
            if self._useMathText or self._usetex:
                if significand == '1' and exponent != '':
                    # reformat 1x10^y as 10^y
                    significand = ''
                if exponent:
                    exponent = '10^{%s%s}' % (sign, exponent)
                if significand and exponent:
                    return r'%s{\times}%s' % (significand, exponent)
                else:
                    return r'%s%s' % (significand, exponent)
            else:
                s = ('%se%s%s' % (significand, sign, exponent)).rstrip('e')
                return s
        except IndexError:
            return s
