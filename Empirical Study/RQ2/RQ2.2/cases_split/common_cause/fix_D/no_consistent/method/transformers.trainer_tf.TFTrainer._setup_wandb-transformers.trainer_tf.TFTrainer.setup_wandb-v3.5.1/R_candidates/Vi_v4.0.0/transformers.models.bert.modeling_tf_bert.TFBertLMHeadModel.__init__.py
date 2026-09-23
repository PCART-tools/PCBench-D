    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)

        if not config.is_decoder:
            logger.warning("If you want to use `TFBertLMHeadModel` as a standalone, add `is_decoder=True.`")

        self.bert = TFBertMainLayer(config, name="bert")
        self.mlm = TFBertMLMHead(config, self.bert.embeddings, name="mlm___cls")
