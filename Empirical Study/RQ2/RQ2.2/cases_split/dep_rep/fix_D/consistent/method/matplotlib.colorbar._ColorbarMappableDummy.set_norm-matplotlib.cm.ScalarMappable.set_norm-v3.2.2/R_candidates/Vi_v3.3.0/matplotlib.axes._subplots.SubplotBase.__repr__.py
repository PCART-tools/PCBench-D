    def __repr__(self):
        fields = []
        if self.get_label():
            fields += [f"label={self.get_label()!r}"]
        titles = []
        for k in ["left", "center", "right"]:
            title = self.get_title(loc=k)
            if title:
                titles.append(f"{k!r}:{title!r}")
        if titles:
            fields += ["title={" + ",".join(titles) + "}"]
        if self.get_xlabel():
            fields += [f"xlabel={self.get_xlabel()!r}"]
        if self.get_ylabel():
            fields += [f"ylabel={self.get_ylabel()!r}"]
        return f"<{self.__class__.__name__}:" + ", ".join(fields) + ">"
