    def __init__(self, d_model_size, num_heads, output_attentions=False, **kwargs):
        super().__init__(**kwargs)
        self.num_heads = num_heads
        self.d_model_size = d_model_size
        self.output_attentions = output_attentions

        self.depth = int(d_model_size / self.num_heads)

        self.Wq = tf.keras.layers.Dense(d_model_size, name="Wq")
        self.Wk = tf.keras.layers.Dense(d_model_size, name="Wk")
        self.Wv = tf.keras.layers.Dense(d_model_size, name="Wv")

        self.dense = tf.keras.layers.Dense(d_model_size, name="dense")
