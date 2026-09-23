    def __init__(self, config: BartConfig, embed_tokens: TFSharedEmbeddings, **kwargs):
        super().__init__(**kwargs)

        self.dropout = config.dropout
        self.layerdrop = config.encoder_layerdrop
        self.output_hidden_states = config.output_hidden_states
        self.output_attentions = config.output_attentions

        self.embed_scale = math.sqrt(config.d_model) if config.scale_embedding else 1.0
        self.padding_idx = config.pad_token_id
        self.max_source_positions = config.max_position_embeddings

        self.embed_tokens = embed_tokens
        if config.static_position_embeddings:
            self.embed_positions = TFSinusoidalPositionalEmbedding(
                config.max_position_embeddings,
                config.d_model,
                name="embed_positions",
            )
        else:
            self.embed_positions = TFLearnedPositionalEmbedding(
                config.max_position_embeddings,
                config.d_model,
                self.padding_idx,
                config.extra_pos_embeddings,
                name="embed_positions",
            )
        self.layers = [TFEncoderLayer(config, name=f"layers.{i}") for i in range(config.encoder_layers)]
        self.layernorm_embedding = (
            LayerNormalization(epsilon=1e-5, name="layernorm_embedding") if config.normalize_embedding else Layer()
        )
        self.layer_norm = LayerNormalization(epsilon=1e-5, name="layer_norm") if config.add_final_layer_norm else None
        self.return_dict = config.return_dict
