@_api.deprecated("3.3")
class GlueSpec:
    """See `Glue`."""

    def __init__(self, width=0., stretch=0., stretch_order=0,
                 shrink=0., shrink_order=0):
        self.width         = width
        self.stretch       = stretch
        self.stretch_order = stretch_order
        self.shrink        = shrink
        self.shrink_order  = shrink_order

    def copy(self):
        return GlueSpec(
            self.width,
            self.stretch,
            self.stretch_order,
            self.shrink,
            self.shrink_order)

    @classmethod
    def factory(cls, glue_type):
        return cls._types[glue_type]
