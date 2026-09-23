    def __init__(self,
                 glue_type: _GlueSpec | T.Literal["fil", "fill", "filll",
                                                  "neg_fil", "neg_fill", "neg_filll",
                                                  "empty", "ss"]):
        super().__init__()
        if isinstance(glue_type, str):
            glue_spec = _GlueSpec._named[glue_type]  # type: ignore[attr-defined]
        elif isinstance(glue_type, _GlueSpec):
            glue_spec = glue_type
        else:
            raise ValueError("glue_type must be a glue spec name or instance")
        self.glue_spec = glue_spec
