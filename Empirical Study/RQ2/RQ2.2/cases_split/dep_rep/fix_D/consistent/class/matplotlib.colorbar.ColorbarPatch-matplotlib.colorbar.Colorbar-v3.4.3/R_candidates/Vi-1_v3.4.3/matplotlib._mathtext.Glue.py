class Glue(Node):
    """
    Most of the information in this object is stored in the underlying
    ``_GlueSpec`` class, which is shared between multiple glue objects.
    (This is a memory optimization which probably doesn't matter anymore, but
    it's easier to stick to what TeX does.)
    """

    glue_subtype = _api.deprecated("3.3")(property(lambda self: "normal"))

    @_api.delete_parameter("3.3", "copy")
    def __init__(self, glue_type, copy=False):
        super().__init__()
        if isinstance(glue_type, str):
            glue_spec = _GlueSpec._named[glue_type]
        elif isinstance(glue_type, _GlueSpec):
            glue_spec = glue_type
        else:
            raise ValueError("glue_type must be a glue spec name or instance")
        self.glue_spec = glue_spec

    def shrink(self):
        super().shrink()
        if self.size < NUM_SIZE_LEVELS:
            g = self.glue_spec
            self.glue_spec = g._replace(width=g.width * SHRINK_FACTOR)

    def grow(self):
        super().grow()
        g = self.glue_spec
        self.glue_spec = g._replace(width=g.width * GROW_FACTOR)
