    def __init__(self, config):
        super().__init__()

        assert config.embedding_size == config.hidden_size, (
            "If you want embedding_size != intermediate hidden_size,"
            "please insert a Conv1d layer to adjust the number of channels "
            "before the first SqueezeBertModule."
        )

        self.layers = nn.ModuleList(SqueezeBertModule(config) for _ in range(config.num_hidden_layers))
