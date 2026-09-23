    def set_figure(self, fig):
        if self.arrow_patch is not None:
            self.arrow_patch.set_figure(fig)
        self.offsetbox.set_figure(fig)
        martist.Artist.set_figure(self, fig)
