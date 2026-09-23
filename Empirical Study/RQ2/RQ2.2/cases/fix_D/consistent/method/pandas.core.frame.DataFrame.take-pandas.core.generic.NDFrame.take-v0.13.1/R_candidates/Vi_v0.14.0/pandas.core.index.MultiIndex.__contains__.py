    def __contains__(self, key):
        hash(key)
        # work around some kind of odd cython bug
        try:
            self.get_loc(key)
            return True
        except KeyError:
            return False
