    def __init__(self, config: DPRConfig, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.encoder = TFDPREncoder(config, name="encoder")

        self.qa_outputs = Dense(2, kernel_initializer=get_initializer(config.initializer_range), name="qa_outputs")
        self.qa_classifier = Dense(
            1, kernel_initializer=get_initializer(config.initializer_range), name="qa_classifier"
        )
