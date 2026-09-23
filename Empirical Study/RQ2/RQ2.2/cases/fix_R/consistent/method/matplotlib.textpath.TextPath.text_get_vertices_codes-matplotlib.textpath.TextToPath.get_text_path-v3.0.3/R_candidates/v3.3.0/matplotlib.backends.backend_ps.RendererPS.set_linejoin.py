    def set_linejoin(self, linejoin, store=True):
        if linejoin != self.linejoin:
            self._pswriter.write("%d setlinejoin\n" % linejoin)
            if store:
                self.linejoin = linejoin
