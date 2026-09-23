    def draw(self, renderer):
        # docstring inherited
        if not self.get_visible() or not self._check_xy(renderer):
            return
        renderer.open_group(self.__class__.__name__, gid=self.get_gid())
        self.update_positions(renderer)
        if self.arrow_patch is not None:
            if (self.arrow_patch.get_figure(root=False) is None and
                    (fig := self.get_figure(root=False)) is not None):
                self.arrow_patch.set_figure(fig)
            self.arrow_patch.draw(renderer)
        self.patch.draw(renderer)
        self.offsetbox.draw(renderer)
        renderer.close_group(self.__class__.__name__)
        self.stale = False
