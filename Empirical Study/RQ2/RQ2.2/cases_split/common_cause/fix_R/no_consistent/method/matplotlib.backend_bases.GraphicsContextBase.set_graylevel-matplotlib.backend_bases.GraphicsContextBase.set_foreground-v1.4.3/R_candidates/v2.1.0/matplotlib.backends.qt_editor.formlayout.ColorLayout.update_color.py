    def update_color(self):
        color = self.text()
        qcolor = to_qcolor(color)
        self.colorbtn.color = qcolor  # defaults to black if not qcolor.isValid()
