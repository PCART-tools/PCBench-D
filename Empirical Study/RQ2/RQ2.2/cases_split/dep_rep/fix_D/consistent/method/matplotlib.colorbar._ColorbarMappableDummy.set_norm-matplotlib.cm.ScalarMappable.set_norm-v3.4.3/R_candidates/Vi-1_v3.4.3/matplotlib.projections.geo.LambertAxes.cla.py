    def cla(self):
        super().cla()
        self.yaxis.set_major_formatter(NullFormatter())
