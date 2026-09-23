    def get_input_embeddings(self):
        return self.ctx_encoder.bert_model.get_input_embeddings()
