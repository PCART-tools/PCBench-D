    @activecolor.setter
    def activecolor(self, activecolor):
        colors._check_color_like(activecolor=activecolor)
        self._activecolor = activecolor
        self.set_radio_props({'facecolor': activecolor})
        # Make sure the deprecated version is updated.
        # Remove once circles is removed.
        labels = [label.get_text() for label in self.labels]
        with cbook._setattr_cm(self, eventson=False):
            self.set_active(labels.index(self.value_selected))
