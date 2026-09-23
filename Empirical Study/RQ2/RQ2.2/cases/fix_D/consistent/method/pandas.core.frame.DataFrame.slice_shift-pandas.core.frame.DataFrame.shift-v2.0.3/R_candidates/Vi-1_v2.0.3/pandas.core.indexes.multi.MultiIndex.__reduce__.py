    def __reduce__(self):
        """Necessary for making this object picklable"""
        d = {
            "levels": list(self.levels),
            "codes": list(self.codes),
            "sortorder": self.sortorder,
            "names": list(self.names),
        }
        return ibase._new_Index, (type(self), d), None
