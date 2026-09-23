    def _setup_textpos(self, x, y, angle, oldx=0, oldy=0, oldangle=0):
        if angle == oldangle == 0:
            self.file.output(x - oldx, y - oldy, Op.textpos)
        else:
            angle = angle / 180.0 * pi
            self.file.output(cos(angle), sin(angle),
                             -sin(angle), cos(angle),
                             x, y, Op.textmatrix)
            self.file.output(0, 0, Op.textpos)
