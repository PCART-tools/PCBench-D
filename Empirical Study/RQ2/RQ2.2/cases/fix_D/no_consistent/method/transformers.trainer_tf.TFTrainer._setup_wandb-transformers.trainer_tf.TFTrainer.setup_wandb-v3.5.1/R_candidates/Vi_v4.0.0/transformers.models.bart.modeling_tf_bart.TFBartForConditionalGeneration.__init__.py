    def __init__(self, config: BartConfig, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.model = TFBartModel(config, name="model")
        self.use_cache = config.use_cache
        # final_bias_logits is registered as a buffer in pytorch, so not trainable for the the sake of consistency.
        self.final_logits_bias = self.add_weight(
            name="/final_logits_bias", shape=[1, config.vocab_size], initializer="zeros", trainable=False
        )
