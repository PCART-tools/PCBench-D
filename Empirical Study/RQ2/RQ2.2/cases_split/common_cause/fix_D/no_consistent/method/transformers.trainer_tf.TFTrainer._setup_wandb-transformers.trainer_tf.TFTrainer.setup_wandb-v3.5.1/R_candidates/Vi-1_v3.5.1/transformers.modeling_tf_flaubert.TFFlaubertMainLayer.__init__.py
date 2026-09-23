    def __init__(self, config, *inputs, **kwargs):
        super().__init__(**kwargs)

        self.n_heads = config.n_heads
        self.n_langs = config.n_langs
        self.dim = config.emb_dim
        self.hidden_dim = self.dim * 4
        self.n_words = config.n_words
        self.pad_index = config.pad_index
        self.causal = config.causal
        self.n_layers = config.n_layers
        self.use_lang_emb = config.use_lang_emb
        self.layerdrop = getattr(config, "layerdrop", 0.0)
        self.pre_norm = getattr(config, "pre_norm", False)
        self.output_attentions = config.output_attentions
        self.output_hidden_states = config.output_hidden_states
        self.return_dict = config.use_return_dict
        self.dropout = tf.keras.layers.Dropout(config.dropout)
        self.position_embeddings = tf.keras.layers.Embedding(
            config.max_position_embeddings,
            self.dim,
            embeddings_initializer=get_initializer(config.embed_init_std),
            name="position_embeddings",
        )

        if config.n_langs > 1 and config.use_lang_emb:
            self.lang_embeddings = tf.keras.layers.Embedding(
                self.n_langs,
                self.dim,
                embeddings_initializer=get_initializer(config.embed_init_std),
                name="lang_embeddings",
            )

        self.embeddings = TFSharedEmbeddings(
            self.n_words, self.dim, initializer_range=config.embed_init_std, name="embeddings"
        )
        self.layer_norm_emb = tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_eps, name="layer_norm_emb")
        self.attentions = []
        self.layer_norm1 = []
        self.ffns = []
        self.layer_norm2 = []

        for i in range(self.n_layers):
            self.attentions.append(
                TFFlaubertMultiHeadAttention(self.n_heads, self.dim, config=config, name="attentions_._{}".format(i))
            )
            self.layer_norm1.append(
                tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_eps, name="layer_norm1_._{}".format(i))
            )
            # if self.is_decoder:
            #     self.layer_norm15.append(nn.LayerNorm(self.dim, eps=config.layer_norm_eps))
            #     self.encoder_attn.append(MultiHeadAttention(self.n_heads, self.dim, dropout=self.attention_dropout))
            self.ffns.append(
                TFFlaubertTransformerFFN(
                    self.dim, self.hidden_dim, self.dim, config=config, name="ffns_._{}".format(i)
                )
            )
            self.layer_norm2.append(
                tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_eps, name="layer_norm2_._{}".format(i))
            )
