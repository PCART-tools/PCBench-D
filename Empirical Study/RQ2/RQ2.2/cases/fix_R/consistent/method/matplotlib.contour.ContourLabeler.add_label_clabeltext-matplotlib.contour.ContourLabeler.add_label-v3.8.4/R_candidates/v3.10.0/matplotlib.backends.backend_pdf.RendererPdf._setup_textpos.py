    def _setup_textpos(self, x, y, angle, oldx=0, oldy=0, oldangle=0):
        if angle == oldangle == 0:
            self.file.output(x - oldx, y - oldy, Op.textpos)
        else:
            angle = math.radians(angle)
            self.file.output(math.cos(angle), math.sin(angle),
                             -math.sin(angle), math.cos(angle),
                             x, y, Op.textmatrix)
            self.file.output(0, 0, Op.textpos)
