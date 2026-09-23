    def __init__(self, config, layer_id=0):
        super().__init__()
        self.layer_id = layer_id
        self.attn_layers = config.attn_layers

        self.layer_norm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)

        if len(set(self.attn_layers)) == 1 and self.attn_layers[0] == "lsh":
            self.self_attention = LSHSelfAttention(config)
        elif len(set(self.attn_layers)) == 1 and self.attn_layers[0] == "local":
            self.self_attention = LocalSelfAttention(config)
        elif len(set(self.attn_layers)) == 2 and set(self.attn_layers) == set(["lsh", "local"]):
            # get correct attn layers
            if self.attn_layers[self.layer_id] == "lsh":
                self.self_attention = LSHSelfAttention(config)
            else:
                self.self_attention = LocalSelfAttention(config)
        else:
            raise NotImplementedError(
                "Only attn layer types 'lsh' and 'local' exist, but got `config.attn_layers`: {}. Select attn layer types from ['lsh', 'local'] only.".format(
                    self.attn_layers
                )
            )
        self.output = ReformerSelfOutput(config)
