    def get_tightbbox(self, renderer=None):
        # docstring inherited
        return Bbox.union([child.get_tightbbox(renderer)
                           for child in self.get_children()])
