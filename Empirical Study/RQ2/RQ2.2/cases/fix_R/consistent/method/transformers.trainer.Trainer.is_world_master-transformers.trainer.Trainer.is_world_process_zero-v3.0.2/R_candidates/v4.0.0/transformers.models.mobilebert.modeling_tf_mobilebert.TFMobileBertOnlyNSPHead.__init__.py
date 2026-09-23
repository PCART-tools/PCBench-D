    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.seq_relationship = tf.keras.layers.Dense(2, name="seq_relationship")
