    def _fixup_dict(self, src_dict):
        # Helper function
        # returns a dict with any single item tuples/lists as individual values
        return {k: self._fixup(v) for k, v in src_dict.items()}
