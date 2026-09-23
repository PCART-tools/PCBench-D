    def get_input_embeddings(self):
        return self.question_encoder.bert_model.get_input_embeddings()
