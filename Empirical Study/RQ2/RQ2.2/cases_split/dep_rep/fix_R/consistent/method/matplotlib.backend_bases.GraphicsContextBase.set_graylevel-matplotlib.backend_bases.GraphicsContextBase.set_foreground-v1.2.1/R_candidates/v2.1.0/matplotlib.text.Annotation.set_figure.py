    def set_figure(self, fig):

        if self.arrow is not None:
            self.arrow.set_figure(fig)
        if self.arrow_patch is not None:
            self.arrow_patch.set_figure(fig)
        Artist.set_figure(self, fig)
