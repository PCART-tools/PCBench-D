    def __reduce__(self):
        """Necessary for making this object picklable"""
        d = dict(
            levels=[lev for lev in self.levels],
            codes=[level_codes for level_codes in self.codes],
            sortorder=self.sortorder,
            names=list(self.names),
        )
        return ibase._new_Index, (self.__class__, d), None
