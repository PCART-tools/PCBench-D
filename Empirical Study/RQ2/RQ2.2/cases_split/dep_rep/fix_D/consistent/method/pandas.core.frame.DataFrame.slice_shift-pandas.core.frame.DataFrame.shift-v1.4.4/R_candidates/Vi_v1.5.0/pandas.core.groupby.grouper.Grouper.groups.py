    @final
    @property
    def groups(self):
        # error: "None" has no attribute "groups"
        return self.grouper.groups  # type: ignore[attr-defined]
