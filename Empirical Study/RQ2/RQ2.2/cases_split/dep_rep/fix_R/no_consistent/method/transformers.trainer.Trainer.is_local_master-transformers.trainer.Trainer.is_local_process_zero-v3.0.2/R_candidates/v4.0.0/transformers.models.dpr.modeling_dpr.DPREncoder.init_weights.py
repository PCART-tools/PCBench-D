    def init_weights(self):
        self.bert_model.init_weights()
        if self.projection_dim > 0:
            self.encode_proj.apply(self.bert_model._init_weights)
