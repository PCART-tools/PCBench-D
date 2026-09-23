    def funcright(self, val):
        self.targetfig.subplots_adjust(right=val)
        if self.drawon:
            self.targetfig.canvas.draw()
