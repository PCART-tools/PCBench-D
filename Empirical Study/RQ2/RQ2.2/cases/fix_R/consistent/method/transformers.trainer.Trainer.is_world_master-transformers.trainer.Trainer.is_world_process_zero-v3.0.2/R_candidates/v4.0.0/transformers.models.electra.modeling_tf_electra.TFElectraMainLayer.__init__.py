    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.embeddings = TFElectraEmbeddings(config, name="embeddings")

        if config.embedding_size != config.hidden_size:
            self.embeddings_project = tf.keras.layers.Dense(config.hidden_size, name="embeddings_project")

        self.encoder = TFElectraEncoder(config, name="encoder")
        self.config = config
