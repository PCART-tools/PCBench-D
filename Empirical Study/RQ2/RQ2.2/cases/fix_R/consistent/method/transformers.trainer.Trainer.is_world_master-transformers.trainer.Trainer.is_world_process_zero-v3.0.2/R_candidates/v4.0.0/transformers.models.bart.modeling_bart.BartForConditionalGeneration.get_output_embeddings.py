    def get_output_embeddings(self):
        return _make_linear_from_emb(self.model.shared)  # make it on the fly
