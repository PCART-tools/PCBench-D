    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.wi_0 = tf.keras.layers.Dense(config.d_ff, use_bias=False, name="wi_0")
        self.wi_1 = tf.keras.layers.Dense(config.d_ff, use_bias=False, name="wi_1")
        self.wo = tf.keras.layers.Dense(config.d_model, use_bias=False, name="wo")
        self.dropout = tf.keras.layers.Dropout(config.dropout_rate)
        self.act = get_tf_activation("gelu_new")
