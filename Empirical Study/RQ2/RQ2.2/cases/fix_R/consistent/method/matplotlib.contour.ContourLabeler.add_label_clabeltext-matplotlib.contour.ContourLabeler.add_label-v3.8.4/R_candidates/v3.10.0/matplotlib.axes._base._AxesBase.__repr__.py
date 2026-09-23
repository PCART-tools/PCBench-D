    def __repr__(self):
        fields = []
        if self.get_label():
            fields += [f"label={self.get_label()!r}"]
        if hasattr(self, "get_title"):
            titles = {}
            for k in ["left", "center", "right"]:
                title = self.get_title(loc=k)
                if title:
                    titles[k] = title
            if titles:
                fields += [f"title={titles}"]
        for name, axis in self._axis_map.items():
            if axis.label and axis.label.get_text():
                fields += [f"{name}label={axis.label.get_text()!r}"]
        return f"<{self.__class__.__name__}: " + ", ".join(fields) + ">"
