    def forward(
        self, hidden_states, attention_mask=None, is_index_masked=None, is_index_global_attn=None, is_global_attn=None
    ):
        self_outputs = self.self(
            hidden_states,
            attention_mask=attention_mask,
            is_index_masked=is_index_masked,
            is_index_global_attn=is_index_global_attn,
            is_global_attn=is_global_attn,
        )
        attn_output = self.output(self_outputs[0], hidden_states)
        outputs = (attn_output,) + self_outputs[1:]
        return outputs
