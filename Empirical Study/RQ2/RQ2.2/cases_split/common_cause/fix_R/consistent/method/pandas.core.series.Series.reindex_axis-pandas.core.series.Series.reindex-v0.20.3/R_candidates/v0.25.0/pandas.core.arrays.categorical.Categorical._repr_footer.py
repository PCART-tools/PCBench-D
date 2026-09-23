    def _repr_footer(self):

        return "Length: {length}\n{info}".format(
            length=len(self), info=self._repr_categories_info()
        )
