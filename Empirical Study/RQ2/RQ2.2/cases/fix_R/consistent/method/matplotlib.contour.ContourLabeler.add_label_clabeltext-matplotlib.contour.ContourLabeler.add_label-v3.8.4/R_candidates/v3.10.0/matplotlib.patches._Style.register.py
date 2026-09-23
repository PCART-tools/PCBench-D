    @classmethod
    @_api.deprecated(
        '3.10.0',
        message="This method is never used internally.",
        alternative="No replacement.  Please open an issue if you use this."
    )
    def register(cls, name, style):
        """Register a new style."""
        if not issubclass(style, cls._Base):
            raise ValueError(f"{style} must be a subclass of {cls._Base}")
        cls._style_list[name] = style
