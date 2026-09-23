    def resize_token_embeddings(self, new_num_tokens: int) -> nn.Embedding:
        new_embeddings = super().resize_token_embeddings(new_num_tokens)
        self.model.encoder.embed_tokens = new_embeddings

        new_embeddings = super().resize_token_embeddings(new_num_tokens)
        self.model.decoder.embed_tokens = new_embeddings

        # XXX: this is not quite correct, as we have 2 different `new_embeddings`, and
        # only one return value is expected. Needs to be redesigned in the core to support dual dicts
        raise NotImplementedError("this method needs re-thinking for models with 2 separate dictionaries")

        return new_embeddings
