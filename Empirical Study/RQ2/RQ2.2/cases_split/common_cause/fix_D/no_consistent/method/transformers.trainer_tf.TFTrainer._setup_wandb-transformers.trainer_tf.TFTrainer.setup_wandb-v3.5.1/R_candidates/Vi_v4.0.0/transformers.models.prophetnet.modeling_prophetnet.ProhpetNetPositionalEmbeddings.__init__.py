    def __init__(self, config: ProphetNetConfig):
        super().__init__(config.max_position_embeddings, config.hidden_size, config.pad_token_id)
