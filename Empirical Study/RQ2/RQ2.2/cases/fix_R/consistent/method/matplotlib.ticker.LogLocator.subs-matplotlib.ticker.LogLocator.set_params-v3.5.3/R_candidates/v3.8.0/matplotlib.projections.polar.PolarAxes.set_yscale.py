    def set_yscale(self, *args, **kwargs):
        super().set_yscale(*args, **kwargs)
        self.yaxis.set_major_locator(
            self.RadialLocator(self.yaxis.get_major_locator(), self))
