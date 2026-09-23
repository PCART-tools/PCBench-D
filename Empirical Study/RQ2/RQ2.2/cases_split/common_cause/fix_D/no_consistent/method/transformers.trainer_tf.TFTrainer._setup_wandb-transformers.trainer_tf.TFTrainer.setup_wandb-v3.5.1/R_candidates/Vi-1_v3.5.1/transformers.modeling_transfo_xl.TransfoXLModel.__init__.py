    def __init__(self, config):
        super().__init__(config)

        self.n_token = config.vocab_size

        self.d_embed = config.d_embed
        self.d_model = config.d_model
        self.n_head = config.n_head
        self.d_head = config.d_head

        self.word_emb = AdaptiveEmbedding(
            config.vocab_size, config.d_embed, config.d_model, config.cutoffs, div_val=config.div_val
        )

        self.drop = nn.Dropout(config.dropout)

        self.n_layer = config.n_layer
        self.mem_len = config.mem_len
        self.attn_type = config.attn_type

        if not config.untie_r:
            self.r_w_bias = nn.Parameter(torch.FloatTensor(self.n_head, self.d_head))
            self.r_r_bias = nn.Parameter(torch.FloatTensor(self.n_head, self.d_head))

        self.layers = nn.ModuleList()
        if config.attn_type == 0:  # the default attention
            for i in range(config.n_layer):
                self.layers.append(
                    RelPartialLearnableDecoderLayer(
                        config.n_head,
                        config.d_model,
                        config.d_head,
                        config.d_inner,
                        config.dropout,
                        dropatt=config.dropatt,
                        pre_lnorm=config.pre_lnorm,
                        r_w_bias=None if config.untie_r else self.r_w_bias,
                        r_r_bias=None if config.untie_r else self.r_r_bias,
                        layer_norm_epsilon=config.layer_norm_epsilon,
                    )
                )
        else:  # learnable embeddings and absolute embeddings are not used in our pretrained checkpoints
            raise NotImplementedError  # Removed them to avoid maintaining dead code

        self.same_length = config.same_length
        self.clamp_len = config.clamp_len

        if self.attn_type == 0:  # default attention
            self.pos_emb = PositionalEmbedding(self.d_model)
        else:  # learnable embeddings and absolute embeddings
            raise NotImplementedError  # Removed these to avoid maintaining dead code - They are not used in our pretrained checkpoint

        self.init_weights()
