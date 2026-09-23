    def contains(self, mouseevent):
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info
        t, tinfo = self.offsetbox.contains(mouseevent)
        #if self.arrow_patch is not None:
        #    a, ainfo=self.arrow_patch.contains(event)
        #    t = t or a

        # self.arrow_patch is currently not checked as this can be a line - JJ

        return t, tinfo
