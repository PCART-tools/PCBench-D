    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.dense = tf.keras.layers.Dense(config.hidden_size, name="dense")
        self.dense_prediction = tf.keras.layers.Dense(1, name="dense_prediction")
        self.config = config
