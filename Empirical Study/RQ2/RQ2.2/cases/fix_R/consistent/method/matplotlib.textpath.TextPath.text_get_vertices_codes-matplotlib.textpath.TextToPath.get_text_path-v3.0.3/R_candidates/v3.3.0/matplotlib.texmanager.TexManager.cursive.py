    @cbook.deprecated("3.3")
    @property
    def cursive(self):
        return self._fonts.get("cursive", ('pzc', r'\usepackage{chancery}'))
