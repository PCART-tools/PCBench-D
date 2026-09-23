    def fix_minus(self, s):
        """
        Replace hyphens with a unicode minus.
        """
        if rcParams['text.usetex'] or not rcParams['axes.unicode_minus']:
            return s
        else:
            return s.replace('-', '\N{MINUS SIGN}')
