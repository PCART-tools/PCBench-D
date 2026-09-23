    def clear(self):
        super().clear()
        martist.setp(self.get_children(), visible=False)
        self._get_lines = self._parent_axes._get_lines
