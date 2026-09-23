    def set_linecap(self, linecap, store=True):
        if linecap != self.linecap:
            self._pswriter.write("%d setlinecap\n" % linecap)
            if store:
                self.linecap = linecap
