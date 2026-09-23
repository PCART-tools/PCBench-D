    def _get_cacher(self):
        """return my cacher or None"""
        cacher = getattr(self, '_cacher', None)
        if cacher is not None:
            cacher = cacher[1]()
        return cacher
