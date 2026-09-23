    def __init__(self, config):  # , dico, is_encoder, with_output):
        super().__init__(config)
        self.layerdrop = getattr(config, "layerdrop", 0.0)
        self.pre_norm = getattr(config, "pre_norm", False)
