    def contains(self, event):
        t, tinfo = self.offsetbox.contains(event)
        #if self.arrow_patch is not None:
        #    a,ainfo=self.arrow_patch.contains(event)
        #    t = t or a

        # self.arrow_patch is currently not checked as this can be a line - JJ

        return t, tinfo
