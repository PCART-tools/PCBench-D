    def getim(self):
        """
        Returns a capsule that points to the internal image memory.

        :returns: A capsule object.
        """

        self.load()
        return self.im.ptr
