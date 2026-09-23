    def update_color(self):
        color = self.text()
        qcolor = to_qcolor(color)  # defaults to black if not qcolor.isValid()
        self.colorbtn.color = qcolor
