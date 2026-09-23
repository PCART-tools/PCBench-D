    def get_gc(self):
        """
        Fetch the locally cached gc.
        """
        # This is a dirty hack to allow anything with access to a renderer to
        # access the current graphics context
        assert self.gc is not None, "gc must be defined"
        return self.gc
