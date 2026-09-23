    def forward(
        self,
        hidden_states,
        layer_state=None,
        attention_mask=None,
        extended_predict_attention_mask=None,
        main_relative_position_buckets=None,
        predict_relative_position_buckets=None,
        position_ids=None,
    ):
        sequence_length, batch_size, hidden_size = hidden_states.size()

        assert list(hidden_states.size()) == [
            sequence_length,
            batch_size,
            hidden_size,
        ], f"`hidden_states` should be of shape {sequence_length, batch_size, hidden_size}, but is of shape {hidden_states.shape}"

        # key and value of previous time steps are cached
        saved_state = layer_state.get("self", None)

        # project
        query_states = self.query_proj(hidden_states)
        key_states = self.key_proj(hidden_states)
        value_states = self.value_proj(hidden_states)

        # normalize
        query_states = query_states / (self.head_dim ** 0.5)

        # reshape
        query_states = self._reshape(query_states, sequence_length, batch_size)
        key_states = self._reshape(key_states, -1, batch_size)
        value_states = self._reshape(value_states, -1, batch_size)

        # chunk into main stream and predict stream
        hidden_states_list = hidden_states.chunk(1 + self.ngram, dim=0)

        query_states_list = query_states.chunk(1 + self.ngram, dim=1)
        key_states_list = key_states.chunk(1 + self.ngram, dim=1)
        value_states_list = value_states.chunk(1 + self.ngram, dim=1)

        main_hidden_states, hidden_states_predict_list = hidden_states_list[0], hidden_states_list[1:]
        main_query_states, predict_query_states_list = query_states_list[0], query_states_list[1:]
        main_key_states, predict_key_states_list = key_states_list[0], key_states_list[1:]
        main_value_states, predict_value_states_list = value_states_list[0], value_states_list[1:]

        # saved states are stored with shape (batch_size, num_attn_heads, seq_len, head_dim)
        if saved_state is not None:
            prev_main_key_states = saved_state["prev_key_states"].view(
                batch_size * self.num_attn_heads, -1, self.head_dim
            )
            main_key_states = torch.cat((prev_main_key_states, main_key_states), dim=1)
            prev_main_value_states = saved_state["prev_value_states"].view(
                batch_size * self.num_attn_heads, -1, self.head_dim
            )
            main_value_states = torch.cat((prev_main_value_states, main_value_states), dim=1)

        # Update cache
        layer_state["self"] = {
            "prev_key_states": main_key_states.view(batch_size, self.num_attn_heads, -1, self.head_dim),
            "prev_value_states": main_value_states.view(batch_size, self.num_attn_heads, -1, self.head_dim),
        }

        # get seq_length of main stream only
        main_sequence_length = sequence_length // (1 + self.ngram)

        # MAIN-STREAM
        # main attn weights
        main_attn_weights = torch.bmm(main_query_states, main_key_states.transpose(1, 2))

        # retrieve relative position embeddings for each layer -> see paper for more details
        main_relative_pos_embeddings = self.get_main_relative_pos_embeddings(
            main_hidden_states, main_attn_weights, position_ids, main_relative_position_buckets
        )
        main_attn_weights = main_attn_weights + main_relative_pos_embeddings

        if attention_mask is not None:
            main_attn_weights = main_attn_weights + attention_mask

        main_attn_probs = softmax(
            main_attn_weights,
            dim=-1,
            onnx_trace=self.onnx_trace,
        ).type_as(main_attn_weights)

        main_attn_probs = F.dropout(main_attn_probs, p=self.attention_dropout, training=self.training)

        # project to attn_output
        main_attn_output = torch.bmm(main_attn_probs, main_value_states)
        main_attn_output = (
            main_attn_output.transpose(0, 1).contiguous().view(1, main_sequence_length, batch_size, hidden_size)
        )
        main_attn_output = self.out_proj(main_attn_output)

        # PREDICT-STREAM
        # [ngram, B*head, T, c]
        predict_query_states = torch.cat(predict_query_states_list, 0).view(
            self.ngram, -1, main_sequence_length, self.head_dim
        )
        # [ngram, B*head, 2*T, c]
        predict_key_states = torch.cat(
            [torch.cat([main_key_states, key], 1).unsqueeze(0) for key in predict_key_states_list], 0
        )

        # [ngram, T, B, C]
        predict_hidden_states = torch.cat(hidden_states_predict_list, 0).view(
            self.ngram, main_sequence_length, batch_size, hidden_size
        )

        # [ngram, B*head, 2*T, c]
        predict_value_states = torch.cat(
            [torch.cat([main_value_states, v_p], 1).unsqueeze(0) for v_p in predict_value_states_list], 0
        )
        # [ngram, B*head, T, 2*T]
        predict_attn_weights = torch.einsum("nbtc,nbsc->nbts", (predict_query_states, predict_key_states))

        # [ngram, B*head, T, S]
        # retrieve relative position embeddings for each layer -> see paper for more details
        predict_relative_pos_embeddings = self.get_predict_relative_pos_embeddings(
            predict_hidden_states, predict_attn_weights, position_ids, predict_relative_position_buckets
        )

        # [ngram, B*head, T, 2*T]
        predict_attn_weights = predict_attn_weights + predict_relative_pos_embeddings

        if extended_predict_attention_mask is not None:
            predict_attn_weights = predict_attn_weights + extended_predict_attention_mask

        predict_attn_probs = softmax(
            predict_attn_weights,
            dim=-1,
            onnx_trace=self.onnx_trace,
        ).type_as(predict_attn_weights)
        predict_attn_probs = F.dropout(predict_attn_probs, p=self.attention_dropout, training=self.training)

        # project to attention output
        # [ngram, B*head, T, c]
        predict_attn_output = torch.einsum("nbts,nbsc->nbtc", (predict_attn_probs, predict_value_states))
        # [ngram, T, B, C]
        predict_attn_output = (
            predict_attn_output.transpose(1, 2)
            .contiguous()
            .view(self.ngram, main_sequence_length, batch_size, hidden_size)
        )
        predict_attn_output = self.out_proj(predict_attn_output)

        # concat to single attn output
        # [1+ngram*T, B, C]
        attn_output = torch.cat([main_attn_output, predict_attn_output], 0).view(-1, batch_size, hidden_size)

        # reshape into better form for `config.output_attentions`
        main_attn_probs = main_attn_probs.view(batch_size, self.num_attn_heads, main_sequence_length, -1)
        predict_attn_probs = predict_attn_probs.view(
            self.ngram, batch_size, self.num_attn_heads, main_sequence_length, -1
        ).transpose(0, 1)

        attn_output = F.dropout(attn_output, p=self.dropout, training=self.training)
        return attn_output, main_attn_probs, predict_attn_probs
