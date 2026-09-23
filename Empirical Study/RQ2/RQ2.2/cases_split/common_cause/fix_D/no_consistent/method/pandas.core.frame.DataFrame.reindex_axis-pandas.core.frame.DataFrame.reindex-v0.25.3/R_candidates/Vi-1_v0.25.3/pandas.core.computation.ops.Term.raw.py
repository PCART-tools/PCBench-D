    @property
    def raw(self):
        return pprint_thing(
            "{0}(name={1!r}, type={2})"
            "".format(self.__class__.__name__, self.name, self.type)
        )
