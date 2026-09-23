    def draw(self, renderer):
        orig_children_len = len(self._children)

        locator = self.get_axes_locator()
        if locator:
            pos = locator(self, renderer)
            self.set_position(pos, which="active")
            self.apply_aspect(pos)
        else:
            self.apply_aspect()

        rect = self.get_position()
        for ax in self.parasites:
            ax.apply_aspect(rect)
            self._children.extend(ax.get_children())

        super().draw(renderer)
        self._children = self._children[:orig_children_len]
