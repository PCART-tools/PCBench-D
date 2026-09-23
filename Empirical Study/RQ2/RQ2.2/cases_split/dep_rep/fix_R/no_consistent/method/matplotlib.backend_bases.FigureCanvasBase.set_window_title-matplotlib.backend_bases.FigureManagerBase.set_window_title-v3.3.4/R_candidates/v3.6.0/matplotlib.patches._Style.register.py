    @classmethod
    def register(cls, name, style):
        """Register a new style."""
        if not issubclass(style, cls._Base):
            raise ValueError("%s must be a subclass of %s" % (style,
                                                              cls._Base))
        cls._style_list[name] = style
