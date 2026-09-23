    def _dir_additions(self):
        rv = set()
        # these accessors are mutually exclusive, so break loop when one exists
        for accessor in self._accessors:
            try:
                getattr(self, accessor)
                rv.add(accessor)
                break
            except AttributeError:
                pass
        return rv
