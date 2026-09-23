    def __init__(self, config: DPRConfig, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.config = config
        self.question_encoder = TFDPREncoder(config, name="question_encoder")
