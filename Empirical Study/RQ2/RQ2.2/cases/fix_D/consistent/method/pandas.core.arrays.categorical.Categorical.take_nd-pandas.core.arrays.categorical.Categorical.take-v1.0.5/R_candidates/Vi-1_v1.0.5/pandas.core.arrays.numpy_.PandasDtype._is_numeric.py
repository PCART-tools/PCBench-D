    @property
    def _is_numeric(self):
        # exclude object, str, unicode, void.
        return self.kind in set("biufc")
