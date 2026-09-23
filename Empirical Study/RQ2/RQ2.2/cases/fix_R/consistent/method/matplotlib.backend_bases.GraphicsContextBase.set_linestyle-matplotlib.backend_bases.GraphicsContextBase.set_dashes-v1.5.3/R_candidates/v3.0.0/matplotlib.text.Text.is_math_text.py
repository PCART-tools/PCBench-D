    @staticmethod
    def is_math_text(s, usetex=None):
        """
        Returns a cleaned string and a boolean flag.
        The flag indicates if the given string *s* contains any mathtext,
        determined by counting unescaped dollar signs. If no mathtext
        is present, the cleaned string has its dollar signs unescaped.
        If usetex is on, the flag always has the value "TeX".
        """
        # Did we find an even number of non-escaped dollar signs?
        # If so, treat is as math text.
        if usetex is None:
            usetex = rcParams['text.usetex']
        if usetex:
            if s == ' ':
                s = r'\ '
            return s, 'TeX'

        if cbook.is_math_text(s):
            return s, True
        else:
            return s.replace(r'\$', '$'), False
