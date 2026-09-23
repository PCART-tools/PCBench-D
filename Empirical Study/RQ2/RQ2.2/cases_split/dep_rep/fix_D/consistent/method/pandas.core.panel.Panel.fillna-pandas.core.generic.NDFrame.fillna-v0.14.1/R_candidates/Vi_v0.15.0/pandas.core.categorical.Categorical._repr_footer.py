    def _repr_footer(self):

        namestr = "Name: %s, " % self.name if self.name is not None else ""
        return u('%sLength: %d\n%s') % (namestr,
                                       len(self), self._repr_categories_info())
