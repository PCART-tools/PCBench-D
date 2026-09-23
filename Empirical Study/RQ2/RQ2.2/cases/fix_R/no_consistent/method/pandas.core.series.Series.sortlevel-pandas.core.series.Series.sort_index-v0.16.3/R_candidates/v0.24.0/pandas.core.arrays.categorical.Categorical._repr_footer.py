    def _repr_footer(self):

        return u('Length: {length}\n{info}').format(
            length=len(self), info=self._repr_categories_info())
