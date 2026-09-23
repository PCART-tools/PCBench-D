    def __repr__(self) -> str:
        attrs_list = (
            f"{attr_name}={repr(getattr(self, attr_name))}"
            for attr_name in self._attributes
            if getattr(self, attr_name) is not None
        )
        attrs = ", ".join(attrs_list)
        cls_name = type(self).__name__
        return f"{cls_name}({attrs})"
