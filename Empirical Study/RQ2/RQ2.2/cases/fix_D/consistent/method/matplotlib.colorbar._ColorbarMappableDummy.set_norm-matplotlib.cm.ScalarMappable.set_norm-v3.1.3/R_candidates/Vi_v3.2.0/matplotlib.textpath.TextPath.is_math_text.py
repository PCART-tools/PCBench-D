    @cbook.deprecated("3.1")
    def is_math_text(self, s):
        """
        Returns True if the given string *s* contains any mathtext.
        """
        # copied from Text.is_math_text -JJL

        # Did we find an even number of non-escaped dollar signs?
        # If so, treat is as math text.
        dollar_count = s.count(r'$') - s.count(r'\$')
        even_dollars = (dollar_count > 0 and dollar_count % 2 == 0)

        if rcParams['text.usetex']:
            return s, 'TeX'

        if even_dollars:
            return s, True
        else:
            return s.replace(r'\$', '$'), False
