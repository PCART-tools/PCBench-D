    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.output_hidden_states = config.output_hidden_states
        self.output_attentions = config.output_attentions
        self.return_dict = config.use_return_dict

        # encoder / decoder, output layer
        self.is_encoder = config.is_encoder
        self.is_decoder = not config.is_encoder

        if self.is_decoder:
            raise NotImplementedError("Currently XLM can only be used as an encoder")

        # self.with_output = with_output
        self.causal = config.causal

        # dictionary / languages
        self.n_langs = config.n_langs
        self.use_lang_emb = config.use_lang_emb
        self.n_words = config.n_words
        self.eos_index = config.eos_index
        self.pad_index = config.pad_index
        # self.dico = dico
        # self.id2lang = config.id2lang
        # self.lang2id = config.lang2id
        # assert len(self.dico) == self.n_words
        # assert len(self.id2lang) == len(self.lang2id) == self.n_langs

        # model parameters
        self.dim = config.emb_dim  # 512 by default
        self.hidden_dim = self.dim * 4  # 2048 by default
        self.n_heads = config.n_heads  # 8 by default
        self.n_layers = config.n_layers
        assert self.dim % self.n_heads == 0, "transformer dim must be a multiple of n_heads"

        # embeddings
        self.dropout = tf.keras.layers.Dropout(config.dropout)
        self.attention_dropout = tf.keras.layers.Dropout(config.attention_dropout)
        self.position_embeddings = tf.keras.layers.Embedding(
            config.max_position_embeddings,
            self.dim,
            embeddings_initializer=get_initializer(config.embed_init_std),
            name="position_embeddings",
        )

        if config.sinusoidal_embeddings:
            raise NotImplementedError
            # create_sinusoidal_embeddings(config.max_position_embeddings, self.dim, out=self.position_embeddings.weight)

        if config.n_langs > 1 and config.use_lang_emb:
            self.lang_embeddings = tf.keras.layers.Embedding(
                self.n_langs,
                self.dim,
                embeddings_initializer=get_initializer(config.embed_init_std),
                name="lang_embeddings",
            )

        self.embeddings = TFSharedEmbeddings(
            self.n_words, self.dim, initializer_range=config.embed_init_std, name="embeddings"
        )  # padding_idx=self.pad_index)
        self.layer_norm_emb = tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_eps, name="layer_norm_emb")

        # transformer layers
        self.attentions = []
        self.layer_norm1 = []
        self.ffns = []
        self.layer_norm2 = []
        # if self.is_decoder:
        #     self.layer_norm15 = []
        #     self.encoder_attn = []

        for i in range(self.n_layers):
            self.attentions.append(
                TFXLMMultiHeadAttention(self.n_heads, self.dim, config=config, name="attentions_._{}".format(i))
            )
            self.layer_norm1.append(
                tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_eps, name="layer_norm1_._{}".format(i))
            )
            # if self.is_decoder:
            #     self.layer_norm15.append(nn.LayerNorm(self.dim, eps=config.layer_norm_eps))
            #     self.encoder_attn.append(MultiHeadAttention(self.n_heads, self.dim, dropout=self.attention_dropout))
            self.ffns.append(
                TFXLMTransformerFFN(self.dim, self.hidden_dim, self.dim, config=config, name="ffns_._{}".format(i))
            )
            self.layer_norm2.append(
                tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_eps, name="layer_norm2_._{}".format(i))
            )

        if hasattr(config, "pruned_heads"):
            pruned_heads = config.pruned_heads.copy().items()
            config.pruned_heads = {}

            for layer, heads in pruned_heads:
                if self.attentions[int(layer)].n_heads == config.n_heads:
                    self.prune_heads({int(layer): list(map(int, heads))})
