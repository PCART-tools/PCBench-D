    def forward(self, hidden_states, attention_mask, output_attentions):
        att = self.attention(hidden_states, attention_mask, output_attentions)
        attention_output = att["context_layer"]

        post_attention_output = self.post_attention(attention_output, hidden_states)
        intermediate_output = self.intermediate(post_attention_output)
        layer_output = self.output(intermediate_output, post_attention_output)

        output_dict = {"feature_map": layer_output}
        if output_attentions:
            output_dict["attention_score"] = att["attention_score"]

        return output_dict
