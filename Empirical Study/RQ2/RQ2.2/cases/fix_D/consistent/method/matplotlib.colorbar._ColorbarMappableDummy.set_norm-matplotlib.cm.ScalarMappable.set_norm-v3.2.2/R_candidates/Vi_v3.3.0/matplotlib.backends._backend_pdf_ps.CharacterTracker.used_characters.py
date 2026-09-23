    @mpl.cbook.deprecated("3.3")
    @property
    def used_characters(self):
        d = {}
        for fname, chars in self.used.items():
            realpath, stat_key = mpl.cbook.get_realpath_and_stat(fname)
            d[stat_key] = (realpath, chars)
        return d
