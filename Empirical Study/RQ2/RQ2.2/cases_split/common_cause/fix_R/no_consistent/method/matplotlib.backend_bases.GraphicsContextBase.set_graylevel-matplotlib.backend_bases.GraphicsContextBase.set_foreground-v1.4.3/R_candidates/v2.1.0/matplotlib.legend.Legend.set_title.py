    def set_title(self, title, prop=None):
        """
        set the legend title. Fontproperties can be optionally set
        with *prop* parameter.
        """
        self._legend_title_box._text.set_text(title)

        if prop is not None:
            if isinstance(prop, dict):
                prop = FontProperties(**prop)
            self._legend_title_box._text.set_fontproperties(prop)

        if title:
            self._legend_title_box.set_visible(True)
        else:
            self._legend_title_box.set_visible(False)
        self.stale = True
