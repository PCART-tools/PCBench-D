    @classmethod
    def register(klass, name, style):
        """
        Register a new style.
        """

        if not issubclass(style, klass._Base):
            raise ValueError("%s must be a subclass of %s" % (style,
                                                              klass._Base))
        klass._style_list[name] = style
