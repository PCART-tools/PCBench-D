    def set_color(self, r, g, b, store=True):
        if (r, g, b) != self.color:
            if r == g and r == b:
                self._pswriter.write("%1.3f setgray\n" % r)
            else:
                self._pswriter.write(
                    "%1.3f %1.3f %1.3f setrgbcolor\n" % (r, g, b))
            if store:
                self.color = (r, g, b)
