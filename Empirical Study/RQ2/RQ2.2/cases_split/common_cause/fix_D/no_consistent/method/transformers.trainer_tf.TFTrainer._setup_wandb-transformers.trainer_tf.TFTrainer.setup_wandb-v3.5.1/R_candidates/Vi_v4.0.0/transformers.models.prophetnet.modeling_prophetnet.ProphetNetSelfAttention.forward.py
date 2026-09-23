    def forward(
        self,
        hidden_states,
        key_value_states: Optional[Tensor] = None,
        attention_mask: Optional[Tensor] = None,
        layer_state: Optional[Dict[str, Optional[Tensor]]] = None,
    ) -> Tuple[Tensor, Optional[Tensor]]:

        sequence_length, batch_size, hidden_size = hidden_states.size()

        # if key_value_states are provided this layer is used as a cross-attention layer
        # for the decoder
        is_cross_attention = key_value_states is not None
        cache_key = "cross_attention" if is_cross_attention else "self"
        assert list(hidden_states.size()) == [
            sequence_length,
            batch_size,
            hidden_size,
        ], f"Size of hidden states should be {sequence_length, batch_size, hidden_size}, but is {hidden_states.size()}"

        # previous time steps are cached - no need to recompute key and value if they are static
        if layer_state is not None:
            saved_state = layer_state.get(cache_key, None)

        query_states = self.query_proj(hidden_states) / (self.head_dim ** 0.5)
        query_states = self._reshape(query_states, sequence_length, batch_size)

        if not is_cross_attention:
            # self-attention
            key_states = self.key_proj(hidden_states)
            key_states = self._reshape(key_states, -1, batch_size)
            value_states = self.value_proj(hidden_states)
            value_states = self._reshape(value_states, -1, batch_size)
        elif saved_state is None:
            # cross-attention without layer state
            key_states = self.key_proj(key_value_states)
            key_states = self._reshape(key_states, -1, batch_size)
            value_states = self.value_proj(key_value_states)
            value_states = self._reshape(value_states, -1, batch_size)
        else:
            key_states = saved_state["prev_key_states"].view(batch_size * self.num_attn_heads, -1, self.head_dim)
            value_states = saved_state["prev_value_states"].view(batch_size * self.num_attn_heads, -1, self.head_dim)

        # Update cache
        if is_cross_attention:
            layer_state[cache_key] = {
                "prev_key_states": key_states.view(batch_size, self.num_attn_heads, -1, self.head_dim),
                "prev_value_states": value_states.view(batch_size, self.num_attn_heads, -1, self.head_dim),
            }

        key_sequence_length = key_states.size(1)
        attn_weights = torch.bmm(query_states, key_states.transpose(1, 2))
        assert attn_weights.size() == (
            batch_size * self.num_attn_heads,
            sequence_length,
            key_sequence_length,
        ), f"`attn_weights` should be of size {batch_size * self.num_attn_heads, sequence_length, key_sequence_length}, but is of size {attn_weights.shape}"

        # This is part of a workaround to get around fork/join parallelism not supporting Optional types.
        if attention_mask is not None and attention_mask.dim() == 0:
            attention_mask = None
        assert attention_mask is None or attention_mask.size() == (
            self.num_attn_heads * batch_size,
            1,
            key_sequence_length,
        ), f"`attention_mask` should be `None` or of shape attention_mask.size() == {batch_size * self.num_attn_heads, 1, key_sequence_length}, but is {attention_mask.shape}"

        if attention_mask is not None:  # don't attend to padding symbols
            attn_weights = attn_weights + attention_mask

        attn_weights = F.softmax(attn_weights, dim=-1)
        attn_probs = F.dropout(
            attn_weights,
            p=self.attention_dropout,
            training=self.training,
        )

        attn_output = torch.bmm(attn_probs, value_states)
        assert attn_output.size() == (
            batch_size * self.num_attn_heads,
            sequence_length,
            self.head_dim,
        ), "`attn_output` should be of shape {batch_size * self.num_attn_heads, sequence_length, self.head_dim}, but is of shape {attn_output.size()}"
        attn_output = attn_output.transpose(0, 1).contiguous().view(sequence_length, batch_size, hidden_size)

        attn_output = self.out_proj(attn_output)

        attn_weights = attn_weights.view(batch_size, self.num_attn_heads, sequence_length, key_sequence_length)
        attn_output = F.dropout(attn_output, p=self.dropout, training=self.training)
        return attn_output, attn_weights
