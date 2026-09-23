    def __init__(self, d_model_size, dff, **kwargs):
        super().__init__(**kwargs)

        self.dense_0 = tf.keras.layers.Dense(dff, activation="relu", name="0")
        self.dense_2 = tf.keras.layers.Dense(d_model_size, name="2")
