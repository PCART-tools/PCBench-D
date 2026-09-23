    def call(self, input_tensor, attention_mask, output_attentions, training=False):
        # Self attention attends to itself, thus keys and querys are the same (input_tensor).
        self_output = self.self(input_tensor, input_tensor, attention_mask, output_attentions)
        if output_attentions:
            attention_probs = self_output[1]
        attention_output = self.attention_output(self_output[0], input_tensor)
        return (attention_output, attention_probs) if output_attentions else (attention_output,)
