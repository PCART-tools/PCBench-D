    def forward(
        self,
        hidden_states,
        attention_mask=None,
        head_mask=None,
        num_hashes=None,
        past_buckets_states=None,
        use_cache=False,
        orig_sequence_length=None,
        output_attentions=False,
        buckets=None,
    ):
        hidden_states = self.layer_norm(hidden_states)

        # make sure cached hidden states is set to None for backward pass
        if past_buckets_states is not None:
            past_buckets_states_layer = past_buckets_states[self.layer_id]
        else:
            past_buckets_states_layer = None

        # use cached buckets for backprob if buckets not None for LSHSelfAttention
        self_attention_outputs = self.self_attention(
            hidden_states=hidden_states,
            head_mask=head_mask,
            attention_mask=attention_mask,
            num_hashes=num_hashes,
            past_buckets_states=past_buckets_states_layer,
            use_cache=use_cache,
            output_attentions=output_attentions,
            buckets=buckets,
        )

        # add buckets if necessary
        if hasattr(self_attention_outputs, "buckets"):
            buckets = self_attention_outputs.buckets
        else:
            buckets = None

        # cache hidden states for future use
        if use_cache:
            if past_buckets_states[self.layer_id][0] is None:
                # padded input should not be cached
                past_buckets = (
                    buckets[:, :, :, :orig_sequence_length]
                    if (buckets is not None and orig_sequence_length > 1)
                    else buckets
                )
            else:
                past_buckets = torch.cat([past_buckets_states[self.layer_id][0], buckets], dim=-1)

            if past_buckets_states[self.layer_id][1] is None:
                # padded input should not be cached
                past_states = hidden_states[:, :orig_sequence_length]
            else:
                past_states = torch.cat([past_buckets_states[self.layer_id][1], hidden_states], dim=1)

            past_buckets_states[self.layer_id] = (past_buckets, past_states)
        # compute attention feed forward output
        attention_output = self.output(self_attention_outputs.hidden_states)

        return AttentionOutput(
            hidden_states=attention_output,
            attention_probs=self_attention_outputs.attention_probs,
            buckets=buckets,
        )
