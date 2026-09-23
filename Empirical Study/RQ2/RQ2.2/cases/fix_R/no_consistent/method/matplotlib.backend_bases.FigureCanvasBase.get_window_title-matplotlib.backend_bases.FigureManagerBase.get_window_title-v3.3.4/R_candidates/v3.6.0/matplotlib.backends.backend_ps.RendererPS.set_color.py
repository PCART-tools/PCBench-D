    def set_color(self, r, g, b, store=True):
        if (r, g, b) != self.color:
            self._pswriter.write(f"{r:1.3f} setgray\n"
                                 if r == g == b else
                                 f"{r:1.3f} {g:1.3f} {b:1.3f} setrgbcolor\n")
            if store:
                self.color = (r, g, b)
