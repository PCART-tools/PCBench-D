    def call(self, pooled_output, training: bool):
        dropout_pooled_output = self.dropout(pooled_output, training=training)
        logits = self.classifier(dropout_pooled_output)
        return logits
