    def __init__(self, config, lxmert_model_embedding_weights):
        super(LxmertLMPredictionHead, self).__init__()
        self.transform = LxmertPredictionHeadTransform(config)

        # The output weights are the same as the input embeddings, but there is
        # an output-only bias for each token.
        self.decoder = nn.Linear(
            lxmert_model_embedding_weights.size(1),
            lxmert_model_embedding_weights.size(0),
            bias=False,
        )
        self.decoder.weight = lxmert_model_embedding_weights
        self.bias = nn.Parameter(torch.zeros(lxmert_model_embedding_weights.size(0)))
