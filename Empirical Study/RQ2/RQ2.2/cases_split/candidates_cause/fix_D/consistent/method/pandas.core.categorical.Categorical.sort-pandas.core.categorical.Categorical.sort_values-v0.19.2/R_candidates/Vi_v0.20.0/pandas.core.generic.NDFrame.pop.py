    def pop(self, item):
        """
        Return item and drop from frame. Raise KeyError if not found.
        """
        result = self[item]
        del self[item]
        try:
            result._reset_cacher()
        except AttributeError:
            pass

        return result
