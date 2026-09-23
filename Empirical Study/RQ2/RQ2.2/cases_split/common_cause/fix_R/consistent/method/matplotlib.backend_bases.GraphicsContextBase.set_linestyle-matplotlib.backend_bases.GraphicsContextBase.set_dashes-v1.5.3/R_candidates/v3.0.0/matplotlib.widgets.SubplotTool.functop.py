    def functop(self, val):
        self.targetfig.subplots_adjust(top=val)
        if self.drawon:
            self.targetfig.canvas.draw()
