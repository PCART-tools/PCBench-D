    def get_children(self):
        'return a list of child artists'
        children = []
        if self._legend_box:
            children.append(self._legend_box)
        children.append(self.get_frame())

        return children
