    def get_kern_dist_from_name(self, name1, name2):
        """
        Return the kerning pair distance (possibly 0) for chars
        *name1* and *name2*.
        """
        return self._kern.get((name1, name2), 0)
