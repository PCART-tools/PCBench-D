    def __repr__(self):
        attrs_list = ["{}={!r}".format(attr_name, getattr(self, attr_name))
                      for attr_name in self._attributes
                      if getattr(self, attr_name) is not None]
        attrs = ", ".join(attrs_list)
        cls_name = self.__class__.__name__
        return "{}({})".format(cls_name, attrs)
