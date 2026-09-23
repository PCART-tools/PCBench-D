    @cbook._delete_parameter("3.3", "copy")
    def __init__(self, glue_type, copy=False):
        Node.__init__(self)
        if isinstance(glue_type, str):
            glue_spec = _GlueSpec._named[glue_type]
        elif isinstance(glue_type, _GlueSpec):
            glue_spec = glue_type
        else:
            raise ValueError("glue_type must be a glue spec name or instance")
        self.glue_spec = glue_spec
