    def funchspace(self, val):
        self.targetfig.subplots_adjust(hspace=val)
        if self.drawon:
            self.targetfig.canvas.draw()
