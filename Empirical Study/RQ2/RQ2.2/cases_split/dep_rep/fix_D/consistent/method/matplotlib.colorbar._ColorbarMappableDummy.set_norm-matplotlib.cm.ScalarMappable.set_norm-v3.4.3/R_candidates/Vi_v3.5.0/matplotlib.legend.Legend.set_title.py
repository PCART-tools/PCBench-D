    def set_title(self, title, prop=None):
        """
        Set the legend title. Fontproperties can be optionally set
        with *prop* parameter.
        """
        self._legend_title_box._text.set_text(title)
        if title:
            self._legend_title_box._text.set_visible(True)
            self._legend_title_box.set_visible(True)
        else:
            self._legend_title_box._text.set_visible(False)
            self._legend_title_box.set_visible(False)

        if prop is not None:
            self._legend_title_box._text.set_fontproperties(prop)

        self.stale = True
