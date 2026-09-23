    def _resize_token_embeddings(self, new_num_tokens):
        # get_input_embeddings and set_input_embeddings need to be implemented in base layer.
        base_model = getattr(self, self.base_model_prefix, self)
        old_embeddings = base_model.get_input_embeddings()
        new_embeddings = self._get_resized_embeddings(old_embeddings, new_num_tokens)
        base_model.set_input_embeddings(new_embeddings)
        # Update base model and current model config
        self.config.vocab_size = new_num_tokens
        base_model.vocab_size = new_num_tokens
        return base_model.get_input_embeddings()
