    def get_tightbbox(self, renderer=None):
        # docstring inherited
        if renderer is None:
            renderer = self.get_figure(root=True)._get_renderer()
        self.update_positions(renderer)
        return Bbox.union([child.get_tightbbox(renderer)
                           for child in self.get_children()])
