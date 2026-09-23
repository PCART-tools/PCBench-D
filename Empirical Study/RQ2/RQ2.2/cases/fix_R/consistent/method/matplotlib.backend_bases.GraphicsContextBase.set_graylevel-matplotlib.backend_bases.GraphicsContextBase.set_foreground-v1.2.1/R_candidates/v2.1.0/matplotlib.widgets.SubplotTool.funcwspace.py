    def funcwspace(self, val):
        self.targetfig.subplots_adjust(wspace=val)
        if self.drawon:
            self.targetfig.canvas.draw()
