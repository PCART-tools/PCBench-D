    def forward(self, hidden_states, attention_mask):
        # 1st residual block
        attention_output, attn_weights = self.self_attn(
            hidden_states=hidden_states,
            attention_mask=attention_mask,
        )
        hidden_states = self.self_attn_layer_norm(attention_output + hidden_states)

        # 2nd residual block
        feed_forward_output = self.feed_forward(hidden_states)
        hidden_states = self.feed_forward_layer_norm(feed_forward_output + hidden_states)
        return hidden_states, attn_weights
