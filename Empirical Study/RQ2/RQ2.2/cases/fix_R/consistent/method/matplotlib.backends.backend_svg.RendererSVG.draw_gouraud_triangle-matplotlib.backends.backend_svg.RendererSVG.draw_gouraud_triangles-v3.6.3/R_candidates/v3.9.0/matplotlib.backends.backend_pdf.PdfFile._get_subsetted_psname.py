    def _get_subsetted_psname(self, ps_name, charmap):
        def toStr(n, base):
            if n < base:
                return string.ascii_uppercase[n]
            else:
                return (
                    toStr(n // base, base) + string.ascii_uppercase[n % base]
                )

        # encode to string using base 26
        hashed = hash(frozenset(charmap.keys())) % ((sys.maxsize + 1) * 2)
        prefix = toStr(hashed, 26)

        # get first 6 characters from prefix
        return prefix[:6] + "+" + ps_name
