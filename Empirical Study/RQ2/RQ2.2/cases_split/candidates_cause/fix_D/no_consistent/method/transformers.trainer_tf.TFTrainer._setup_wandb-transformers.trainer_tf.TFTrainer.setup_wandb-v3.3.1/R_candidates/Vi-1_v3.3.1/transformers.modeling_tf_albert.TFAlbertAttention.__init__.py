    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        self.hidden_size = config.hidden_size
        self.output_attentions = config.output_attentions
        self.num_attention_heads = config.num_attention_heads
        assert config.hidden_size % config.num_attention_heads == 0
        self.attention_head_size = int(config.hidden_size / config.num_attention_heads)
        self.all_head_size = self.num_attention_heads * self.attention_head_size
        self.query = tf.keras.layers.Dense(
            self.all_head_size, kernel_initializer=get_initializer(config.initializer_range), name="query"
        )
        self.key = tf.keras.layers.Dense(
            self.all_head_size, kernel_initializer=get_initializer(config.initializer_range), name="key"
        )
        self.value = tf.keras.layers.Dense(
            self.all_head_size, kernel_initializer=get_initializer(config.initializer_range), name="value"
        )
        self.dense = tf.keras.layers.Dense(
            config.hidden_size, kernel_initializer=get_initializer(config.initializer_range), name="dense"
        )
        self.LayerNorm = tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_eps, name="LayerNorm")
        self.pruned_heads = set()
        # Two different dropout probabilities; see https://github.com/google-research/albert/blob/master/modeling.py#L971-L993
        self.attention_dropout = tf.keras.layers.Dropout(config.attention_probs_dropout_prob)
        self.output_dropout = tf.keras.layers.Dropout(config.hidden_dropout_prob)
