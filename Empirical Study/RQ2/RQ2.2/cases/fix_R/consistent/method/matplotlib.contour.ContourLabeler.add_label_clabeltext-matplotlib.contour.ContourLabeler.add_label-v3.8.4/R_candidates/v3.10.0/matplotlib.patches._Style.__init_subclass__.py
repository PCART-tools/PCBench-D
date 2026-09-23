    def __init_subclass__(cls):
        # Automatically perform docstring interpolation on the subclasses:
        # This allows listing the supported styles via
        # - %(BoxStyle:table)s
        # - %(ConnectionStyle:table)s
        # - %(ArrowStyle:table)s
        # and additionally adding .. ACCEPTS: blocks via
        # - %(BoxStyle:table_and_accepts)s
        # - %(ConnectionStyle:table_and_accepts)s
        # - %(ArrowStyle:table_and_accepts)s
        _docstring.interpd.register(**{
            f"{cls.__name__}:table": cls.pprint_styles(),
            f"{cls.__name__}:table_and_accepts": (
                cls.pprint_styles()
                + "\n\n    .. ACCEPTS: ["
                + "|".join(map(" '{}' ".format, cls._style_list))
                + "]")
        })
