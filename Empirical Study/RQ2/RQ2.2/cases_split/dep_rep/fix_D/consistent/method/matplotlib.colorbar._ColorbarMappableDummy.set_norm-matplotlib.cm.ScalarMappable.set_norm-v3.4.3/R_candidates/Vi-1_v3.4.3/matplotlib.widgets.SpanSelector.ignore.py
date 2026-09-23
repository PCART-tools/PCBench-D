    def ignore(self, event):
        # docstring inherited
        return super().ignore(event) or not self.visible
